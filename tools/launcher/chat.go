package main

// Chat with CubeMind through a local Ollama model; replies are spoken with Windows' built-in voices (System.Speech,
// nothing downloaded). Empty input = speak your message (Windows speech recognition). Commands: /voice, /quiet, /exit.
import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os/exec"
	"strings"
	"time"
)

const persona = `You are CubeMind, Danny's local AI partner. Be warm, direct and brief (2-5 sentences unless asked for more).
Follow the AEGIS method: separate what you know from what you guess; label claims as derived, literature, estimate or
guess; say "I don't know" when you don't; never invent sources, numbers or quotes; if asked to compute, show the steps
so they can be checked. Your replies are read aloud, so avoid tables, code blocks and long lists unless asked.`

type msg struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

func ollamaChat(model string, hist []msg) (string, error) {
	body, _ := json.Marshal(map[string]any{"model": model, "messages": hist, "stream": false,
		"options": map[string]any{"temperature": 0.4}})
	cl := &http.Client{Timeout: 10 * time.Minute}
	r, err := cl.Post("http://127.0.0.1:11434/api/chat", "application/json", bytes.NewReader(body))
	if err != nil {
		return "", err
	}
	defer r.Body.Close()
	var out struct {
		Message msg    `json:"message"`
		Error   string `json:"error"`
	}
	if err := json.NewDecoder(r.Body).Decode(&out); err != nil {
		return "", err
	}
	if out.Error != "" {
		return "", fmt.Errorf("%s", out.Error)
	}
	return out.Message.Content, nil
}

func psRun(script string, stdin string) (string, error) {
	c := exec.Command("powershell", "-NoProfile", "-Command", script)
	c.Stdin = strings.NewReader(stdin)
	out, err := c.Output()
	return strings.TrimSpace(string(out)), err
}

func voices() []string {
	out, err := psRun(`Add-Type -AssemblyName System.Speech; $s=New-Object System.Speech.Synthesis.SpeechSynthesizer; $s.GetInstalledVoices() | % { $_.VoiceInfo.Name }`, "")
	if err != nil || out == "" {
		return nil
	}
	return strings.Split(strings.ReplaceAll(out, "\r", ""), "\n")
}

func speak(text, voice string, rate int) {
	clean := strings.NewReplacer("*", "", "#", "", "`", "", "_", " ").Replace(text)
	script := fmt.Sprintf(`Add-Type -AssemblyName System.Speech; $s=New-Object System.Speech.Synthesis.SpeechSynthesizer; `+
		`try { if ('%s' -ne '') { $s.SelectVoice('%s') } } catch {}; $s.Rate=%d; $t=[Console]::In.ReadToEnd(); $s.Speak($t)`,
		strings.ReplaceAll(voice, "'", ""), strings.ReplaceAll(voice, "'", ""), rate)
	psRun(script, clean)
}

func listen() string {
	fmt.Println("(listening... speak now, up to 15 seconds)")
	out, err := psRun(`Add-Type -AssemblyName System.Speech; $r=New-Object System.Speech.Recognition.SpeechRecognitionEngine; `+
		`$r.LoadGrammar((New-Object System.Speech.Recognition.DictationGrammar)); $r.SetInputToDefaultAudioDevice(); `+
		`$res=$r.Recognize([TimeSpan]::FromSeconds(15)); if ($res) { $res.Text }`, "")
	if err != nil {
		fmt.Println("(speech recognition unavailable: " + err.Error() + ")")
		return ""
	}
	return out
}

func chatMode() {
	if !have("ollama") {
		logln("Ollama is not installed.")
		return
	}
	run("ollama", "list")
	model := ask("Model to chat with (a NAME from the list): ")
	if model == "" {
		return
	}
	vs := voices()
	voice := ""
	if len(vs) > 0 {
		fmt.Println("Voices on this PC:")
		for i, v := range vs {
			fmt.Printf("  %d) %s\n", i+1, v)
		}
		if c := ask("Pick a voice number (Enter = first): "); c != "" {
			var i int
			fmt.Sscanf(c, "%d", &i)
			if i >= 1 && i <= len(vs) {
				voice = vs[i-1]
			}
		} else {
			voice = vs[0]
		}
	}
	rate, quiet := 0, false
	hist := []msg{{"system", persona + toolGuide}}
	fmt.Println("\nChat with CubeMind. Type a message, or press Enter on an empty line to talk.")
	fmt.Println("Commands: /voice (change voice), /faster, /slower, /quiet (text only), /exit")
	for {
		t := ask("\nYou: ")
		switch t {
		case "/exit":
			return
		case "/quiet":
			quiet = !quiet
			fmt.Println("(voice", map[bool]string{true: "off", false: "on"}[quiet]+")")
			continue
		case "/faster":
			rate += 2
			continue
		case "/slower":
			rate -= 2
			continue
		case "/voice":
			for i, v := range vs {
				fmt.Printf("  %d) %s\n", i+1, v)
			}
			var i int
			fmt.Sscanf(ask("Voice number: "), "%d", &i)
			if i >= 1 && i <= len(vs) {
				voice = vs[i-1]
			}
			continue
		case "":
			t = listen()
			if t == "" {
				fmt.Println("(didn't catch that)")
				continue
			}
			fmt.Println("You (spoken): " + t)
		}
		hist = append(hist, msg{"user", t})
		logln("chat> " + t)
		reply, err := ollamaChat(model, hist)
		if err != nil {
			fmt.Println("(model error: " + err.Error() + ")")
			hist = hist[:len(hist)-1]
			continue
		}
		for steps := 0; steps < 3; steps++ { // let CubeMind use up to 3 tools before it answers
			res, used := handleTool(reply)
			if !used {
				break
			}
			fmt.Println("(" + strings.SplitN(res, "\n", 2)[0] + ")")
			hist = append(hist, msg{"assistant", reply}, msg{"user", res + "\n\nNow answer Danny's last message."})
			if reply, err = ollamaChat(model, hist); err != nil {
				break
			}
		}
		if err != nil {
			fmt.Println("(model error: " + err.Error() + ")")
			continue
		}
		hist = append(hist, msg{"assistant", reply})
		if len(hist) > 41 { // keep the persona plus the last 40 turns
			hist = append([]msg{hist[0]}, hist[len(hist)-40:]...)
		}
		fmt.Println("\nCubeMind: " + reply)
		logln("cubemind> " + reply)
		if !quiet {
			speak(reply, voice, rate)
		}
	}
}

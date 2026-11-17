// AEGIS + CubeMind launcher for Windows. Build: GOOS=windows GOARCH=amd64 go build -o AEGIS_Launcher.exe
// Runs only Danny's own tools: WSL Ubuntu (AEGIS calc queue), Git, Python, Ollama (models already installed; nothing
// is pulled). Every action is logged to %USERPROFILE%\AEGIS_launcher.log.
package main

import (
	"bufio"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"
)

var in = bufio.NewReader(os.Stdin)
var logf *os.File

func logln(s string) {
	line := time.Now().Format("2006-01-02 15:04:05") + "  " + s
	fmt.Println(s)
	if logf != nil {
		logf.WriteString(line + "\r\n")
	}
}
func ask(prompt string) string {
	fmt.Print(prompt)
	s, _ := in.ReadString('\n')
	return strings.TrimSpace(s)
}
func run(name string, args ...string) error {
	logln("> " + name + " " + strings.Join(args, " "))
	c := exec.Command(name, args...)
	c.Stdout, c.Stderr, c.Stdin = os.Stdout, os.Stderr, os.Stdin
	err := c.Run()
	if err != nil {
		logln("  ! " + err.Error())
	}
	return err
}
func runIn(dir, name string, args ...string) error {
	logln("> (" + dir + ") " + name + " " + strings.Join(args, " "))
	c := exec.Command(name, args...)
	c.Dir = dir
	c.Stdout, c.Stderr, c.Stdin = os.Stdout, os.Stderr, os.Stdin
	err := c.Run()
	if err != nil {
		logln("  ! " + err.Error())
	}
	return err
}
func have(tool string) bool { _, err := exec.LookPath(tool); return err == nil }

func ubuntuName() string {
	out, err := exec.Command("wsl", "-l", "-q").Output()
	if err == nil {
		clean := strings.ReplaceAll(string(out), "\x00", "")
		for _, l := range strings.Split(clean, "\n") {
			l = strings.TrimSpace(l)
			if strings.HasPrefix(strings.ToLower(l), "ubuntu") {
				return l
			}
		}
	}
	return "Ubuntu"
}

const aegisScript = `set -e; if [ ! -d ~/aegis_calc ]; then git clone -b unify-bg https://github.com/dannyeldridge54/AEGIS.git ~/aegis_calc; fi; cd ~/aegis_calc; git pull -q || true; python3 -m pip install -q --user numpy scipy sympy mpmath 2>/dev/null || python3 -m pip install -q --user --break-system-packages numpy scipy sympy mpmath; python3 -m tools.serapis_calc.selftest; mkdir -p /mnt/c/Users/$WINUSER/Desktop/AEGIS_calc_results; ( while true; do git pull -q || true; cp -u field_tests/results/* /mnt/c/Users/$WINUSER/Desktop/AEGIS_calc_results/ 2>/dev/null; cp -u tools/calcq/status_pc.txt /mnt/c/Users/$WINUSER/Desktop/AEGIS_calc_results/ 2>/dev/null; sleep 300; done ) & QUEUE=tools/calcq/queue_pc.txt STATUS=tools/calcq/status_pc.txt MAXJOBS=$(nproc) IDLE_MAX=14400 bash tools/calcq/runner.sh`

func checkAll() {
	logln("Checking tools:")
	for _, t := range []string{"wsl", "git", "python", "ollama"} {
		st := "missing"
		if have(t) {
			st = "ok"
		}
		logln(fmt.Sprintf("  %-7s %s", t, st))
	}
	if have("wsl") {
		logln("  WSL distro: " + ubuntuName())
	}
}
func aegisQueue() {
	if !have("wsl") {
		logln("WSL is not installed; cannot start the AEGIS queue.")
		return
	}
	user := os.Getenv("USERNAME")
	script := strings.ReplaceAll(aegisScript, "$WINUSER", user)
	logln("Starting the AEGIS calculation queue in " + ubuntuName() + " (separate copy ~/aegis_calc; your AEGIS repo is not touched).")
	logln("Leave this window open while it works. Results: Desktop\\AEGIS_calc_results")
	run("wsl", "-d", ubuntuName(), "--", "bash", "-lc", script)
}
func janusDir() string { return filepath.Join(os.Getenv("USERPROFILE"), "CubeMind_janus") }
func janusPrep() bool {
	if !have("git") || !have("python") {
		logln("Git and Python are needed for CubeMind.")
		return false
	}
	d := janusDir()
	if _, err := os.Stat(d); os.IsNotExist(err) {
		if run("git", "clone", "-b", "janus-pair", "https://github.com/dannyeldridge54/CubeMind.git", d) != nil {
			return false
		}
	} else {
		runIn(d, "git", "pull", "-q")
	}
	if runIn(d, "python", "-m", "janus.selftest") != nil {
		logln("CubeMind selftest failed - not starting.")
		return false
	}
	return true
}
func pickModels() (string, string) {
	if !have("ollama") {
		logln("Ollama is not installed.")
		return "", ""
	}
	run("ollama", "list")
	a := ask("Model for Janus-A (a NAME from the list): ")
	b := ask("Model for Janus-B (another NAME, or the same): ")
	return a, b
}
func janusLoop() {
	if !janusPrep() {
		return
	}
	a, b := pickModels()
	if a == "" || b == "" {
		return
	}
	r := ask("Rounds (Enter = 6): ")
	if r == "" {
		r = "6"
	}
	runIn(janusDir(), "python", "-m", "janus.loop", "--model-a", a, "--model-b", b, "--rounds", r, "--exam-every", "3")
	logln("Ledger: " + filepath.Join(janusDir(), "janus", "data", "ledger.jsonl"))
}
func janusImprove() {
	if !janusPrep() {
		return
	}
	fmt.Println("Experiments: 1) work_then_answer  2) reverse_check  3) self_consistency3  4) janus_sync (two models settle)")
	ch := ask("Choose 1-4: ")
	hyp := ask("Hypothesis in one line (locked before the run): ")
	if ch == "4" {
		a, b := pickModels()
		if a == "" || b == "" {
			return
		}
		code := fmt.Sprintf("from janus.improve import sync_experiment; from janus.backends import Ollama; import json; print(json.dumps(sync_experiment(Ollama(%q), Ollama(%q), %q), indent=1))", a, b, hyp)
		runIn(janusDir(), "python", "-c", code)
		return
	}
	cand := map[string]string{"1": "work_then_answer", "2": "reverse_check", "3": "self_consistency3"}[ch]
	if cand == "" {
		return
	}
	run("ollama", "list")
	m := ask("Model name: ")
	runIn(janusDir(), "python", "-m", "janus.improve", "--model", m, "--candidate", cand, "--hypothesis", hyp)
}
func selftests() {
	if have("wsl") {
		run("wsl", "-d", ubuntuName(), "--", "bash", "-lc", "cd ~/aegis_calc 2>/dev/null && git pull -q; python3 -m tools.serapis_calc.selftest || echo 'AEGIS copy not set up yet: use option 2 first'")
	}
	if janusPrep() {
		logln("CubeMind selftest passed.")
	}
}
func openFolders() {
	for _, p := range []string{filepath.Join(os.Getenv("USERPROFILE"), "Desktop", "AEGIS_calc_results"), filepath.Join(janusDir(), "janus", "data")} {
		if _, err := os.Stat(p); err == nil {
			exec.Command("explorer", p).Start()
			logln("Opened " + p)
		} else {
			logln("Not created yet: " + p)
		}
	}
}
func main() {
	lp := filepath.Join(os.Getenv("USERPROFILE"), "AEGIS_launcher.log")
	logf, _ = os.OpenFile(lp, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	defer func() {
		if logf != nil {
			logf.Close()
		}
	}()
	for {
		fmt.Println("\n=== AEGIS + CubeMind launcher ===")
		fmt.Println("1) Check installed tools")
		fmt.Println("2) Start the AEGIS calculation queue (Ubuntu, all cores)")
		fmt.Println("3) Start CubeMind Janus learning loop (two Ollama models)")
		fmt.Println("4) Run a CubeMind self-improvement / sync experiment")
		fmt.Println("5) Run all selftests")
		fmt.Println("6) Open results folders")
		fmt.Println("0) Quit")
		switch ask("Choose: ") {
		case "1":
			checkAll()
		case "2":
			aegisQueue()
		case "3":
			janusLoop()
		case "4":
			janusImprove()
		case "5":
			selftests()
		case "6":
			openFolders()
		case "0":
			return
		}
	}
}

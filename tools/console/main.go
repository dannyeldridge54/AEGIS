// CubeMind Nuclear Console: a local display for CubeMind and the AEGIS reactor work.
// Serves an embedded page on 127.0.0.1 and reads CubeMind's live files from disk (read-only).
package main

import (
	"bufio"
	_ "embed"
	"encoding/json"
	"fmt"
	"net"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
	"time"
)

//go:embed index.html
var indexHTML []byte

//go:embed results.json
var resultsJSON []byte

var cmDir string

func findCubeMind() string {
	cands := []string{}
	if len(os.Args) > 1 {
		cands = append(cands, os.Args[1])
	}
	if exe, err := os.Executable(); err == nil {
		d := filepath.Dir(exe)
		cands = append(cands, d, filepath.Join(d, "CubeMind_janus"))
	}
	if h, err := os.UserHomeDir(); err == nil {
		cands = append(cands, filepath.Join(h, "CubeMind_janus"), filepath.Join(h, "Desktop", "CubeMind_janus"))
	}
	for _, c := range cands {
		if _, err := os.Stat(filepath.Join(c, "learn_log.jsonl")); err == nil {
			return c
		}
	}
	return ""
}

// tailLines returns the last n lines of a file without reading it all.
func tailLines(path string, n int) []string {
	f, err := os.Open(path)
	if err != nil {
		return nil
	}
	defer f.Close()
	st, _ := f.Stat()
	size := st.Size()
	var chunk int64 = 256 * 1024
	if chunk > size {
		chunk = size
	}
	buf := make([]byte, chunk)
	f.ReadAt(buf, size-chunk)
	lines := strings.Split(strings.TrimRight(string(buf), "\n"), "\n")
	if int64(len(buf)) < size && len(lines) > 0 {
		lines = lines[1:]
	}
	if len(lines) > n {
		lines = lines[len(lines)-n:]
	}
	return lines
}

func countLines(path string) int {
	f, err := os.Open(path)
	if err != nil {
		return -1
	}
	defer f.Close()
	sc := bufio.NewScanner(f)
	sc.Buffer(make([]byte, 1024*1024), 64*1024*1024)
	c := 0
	for sc.Scan() {
		c++
	}
	return c
}

var memCount struct {
	n    int
	at   time.Time
	size int64
}

func live(w http.ResponseWriter, r *http.Request) {
	out := map[string]any{"found": cmDir != "", "dir": cmDir, "now": time.Now().UTC().Format(time.RFC3339)}
	if cmDir != "" {
		var entries []json.RawMessage
		for _, l := range tailLines(filepath.Join(cmDir, "learn_log.jsonl"), 25) {
			if json.Valid([]byte(l)) {
				entries = append(entries, json.RawMessage(l))
			}
		}
		out["learn"] = entries
		mp := filepath.Join(cmDir, "cubemind_memory.jsonl")
		if st, err := os.Stat(mp); err == nil {
			if st.Size() != memCount.size || time.Since(memCount.at) > 5*time.Minute {
				memCount.n, memCount.size, memCount.at = countLines(mp), st.Size(), time.Now()
			}
			out["memory_records"] = memCount.n
			out["memory_mtime"] = st.ModTime().UTC().Format(time.RFC3339)
			var mem []string
			for _, l := range tailLines(mp, 6) {
				var m map[string]any
				if json.Unmarshal([]byte(l), &m) == nil {
					if t, ok := m["text"].(string); ok {
						if len(t) > 400 {
							t = t[:400] + "…"
						}
						mem = append(mem, t)
					}
				}
			}
			out["memory_tail"] = mem
		}
		files := map[string]string{}
		for _, fn := range []string{"learn_log.jsonl", "DERIVATION_LOG.md", "CM_RESULTS.md", "REACTOR_LOOP_TASK.md", "CUBEMIND_NUCLEAR_BRIEF_2026-11-23.md"} {
			if st, err := os.Stat(filepath.Join(cmDir, fn)); err == nil {
				files[fn] = st.ModTime().UTC().Format(time.RFC3339)
			}
		}
		out["files"] = files
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(out)
}

func nuclides(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	if cmDir == "" {
		w.Write([]byte(`{"rows":[]}`))
		return
	}
	b, err := os.ReadFile(filepath.Join(cmDir, "weave_data", "nuclide_catalog.json"))
	if err != nil {
		w.Write([]byte(`{"rows":[]}`))
		return
	}
	var cat struct {
		Rows []struct {
			Z, A   int
			Iso    int     `json:"iso"`
			Name   string  `json:"name"`
			Me     float64 `json:"me_keV"`
			T12    *float64 `json:"t12_s"`
			Stable bool    `json:"stable"`
			Modes  string  `json:"modes"`
		} `json:"rows"`
	}
	json.Unmarshal(b, &cat)
	rows := [][]any{}
	for _, x := range cat.Rows {
		if x.Iso != 0 {
			continue
		}
		var t any
		if x.T12 != nil {
			t = *x.T12
		}
		rows = append(rows, []any{x.Z, x.A, x.Name, x.Me, t, x.Stable, x.Modes})
	}
	json.NewEncoder(w).Encode(map[string]any{"rows": rows})
}

func elements(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	if cmDir == "" {
		w.Write([]byte(`{}`))
		return
	}
	b, err := os.ReadFile(filepath.Join(cmDir, "weave_data", "element_catalog.json"))
	if err != nil {
		w.Write([]byte(`{}`))
		return
	}
	var cat struct {
		Elements map[string]struct {
			Z     int `json:"Z"`
			Table map[string][]struct {
				T     float64 `json:"T_keV"`
				Lline float64 `json:"L_line"`
				Lrb   float64 `json:"L_rb"`
			} `json:"table"`
		} `json:"elements"`
	}
	json.Unmarshal(b, &cat)
	out := map[string]any{}
	for k, e := range cat.Elements {
		pts := [][2]float64{}
		for _, p := range e.Table["1e+20"] {
			pts = append(pts, [2]float64{p.T, p.Lline + p.Lrb})
		}
		out[k] = map[string]any{"Z": e.Z, "L": pts}
	}
	json.NewEncoder(w).Encode(out)
}

func openWindow(url string) {
	if runtime.GOOS != "windows" {
		fmt.Println("Open", url)
		return
	}
	// Prefer an app-style window (no browser toolbars); fall back to the default browser.
	for _, p := range []string{
		os.Getenv("ProgramFiles(x86)") + `\Microsoft\Edge\Application\msedge.exe`,
		os.Getenv("ProgramFiles") + `\Microsoft\Edge\Application\msedge.exe`,
		os.Getenv("ProgramFiles") + `\Google\Chrome\Application\chrome.exe`,
		os.Getenv("LocalAppData") + `\Google\Chrome\Application\chrome.exe`,
	} {
		if _, err := os.Stat(p); err == nil {
			if exec.Command(p, "--app="+url, "--window-size=1440,920").Start() == nil {
				return
			}
		}
	}
	exec.Command("rundll32", "url.dll,FileProtocolHandler", url).Start()
}

func main() {
	cmDir = findCubeMind()
	mux := http.NewServeMux()
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/html; charset=utf-8")
		w.Write(indexHTML)
	})
	mux.HandleFunc("/api/results", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Write(resultsJSON)
	})
	mux.HandleFunc("/api/live", live)
	mux.HandleFunc("/api/nuclides", nuclides)
	mux.HandleFunc("/api/elements", elements)
	ln, err := net.Listen("tcp", "127.0.0.1:8765")
	if err != nil {
		ln, err = net.Listen("tcp", "127.0.0.1:0")
		if err != nil {
			fmt.Println("cannot start:", err)
			return
		}
	}
	url := "http://" + ln.Addr().String() + "/"
	fmt.Println("CubeMind Nuclear Console running at", url)
	fmt.Println("CubeMind folder:", cmDir)
	fmt.Println("Close this window to stop the console.")
	openWindow(url)
	http.Serve(ln, mux)
}

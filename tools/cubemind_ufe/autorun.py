"""CubeMind autonomous run (Danny 21 Nov 2026): no timer, no check-ins. It runs rounds back to back as fast as the models answer.
Phase 1 LEARN: lessons and held-out exams on every track (core + the UFE-lens tracks astro, compress, ufe, place), self-graded mechanically.
Phase 2 MISSION: once a face has mastered every track, it attacks the targets in janus/mission.py, keeps grading itself with a refresher
exam every 10 mission steps, and drops back to LEARN if any track falls below mastery.
Guards: local models only (Ollama); nothing is downloaded, published, sent or deleted; every proposal is locked (sha256) before it is scored."""
import json, os, time, argparse
from . import loop, mission
def all_mastered(m):
    faces = set(n for v in m.values() for n in v)
    return [f for f in faces if all(v.get(f) for v in m.values())]
def main():
    a = argparse.ArgumentParser(); a.add_argument('--model-a', required=True); a.add_argument('--model-b', required=True)
    a.add_argument('--allow-code', action='store_true'); a.add_argument('--max-steps', type=int, default=10 ** 9)
    g = a.parse_args()
    from .backends import Ollama
    faces = {'Janus-A': Ollama(g.model_a), 'Janus-B': Ollama(g.model_b)}
    phase, steps = 'LEARN', 0
    while steps < g.max_steps:
        steps += 1
        if phase == 'LEARN':
            st, sc = loop.one_round(faces, g.allow_code, exam=False); print('LEARN round', st['round'], json.dumps(sc), flush=True)
            if st['round'] % 3 == 0:
                st, sc = loop.one_round(faces, g.allow_code, exam=True); m = loop.mastery(st, list(faces)); ready = all_mastered(m)
                print('EXAM', json.dumps(sc), 'mastered by', ready, flush=True)
                if ready: phase = 'MISSION'; print('*** solid base reached: entering MISSION with', ready, flush=True)
        else:
            rec = mission.step(faces, steps); print('MISSION', json.dumps(rec)[:400], flush=True)
            if steps % 10 == 0:
                st, sc = loop.one_round(faces, g.allow_code, exam=True); m = loop.mastery(st, list(faces))
                if not all_mastered(m): phase = 'LEARN'; print('refresher exam dropped below mastery: back to LEARN', flush=True)
if __name__ == '__main__':
    main()

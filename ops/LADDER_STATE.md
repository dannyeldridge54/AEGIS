# Twin-ladder loop state (Danny 16:12 CT 14 Nov: "PP loops every 5 minutes … until you start hitting walls, then 30 minutes, then an hour")
interval_min: 5
consecutive_walls: 0
cycle: 0
rules:
- A WALL = a cycle that ends with no new confirmed or scored result (blocked on data/PC/Danny, or a research dead end with nothing recorded beyond "nothing new").
- 2 consecutive walls at 5 min → switch to 30 min; 2 consecutive walls at 30 min → 60 min; 3 consecutive walls at 60 min → stop the loop and report to Danny.
- Any real result resets consecutive_walls to 0 (interval stays where it is).
- Each cycle: one twin-ladder cycle (skill), then update this file, then schedule the next with send_later.
log:

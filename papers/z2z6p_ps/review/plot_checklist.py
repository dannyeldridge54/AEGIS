import json, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
rows = json.load(open('expert_checklist.json'))
col = {'PASS': '#2e7d32', 'FAIL': '#c62828', 'TENSION': '#e65100', 'OBSTRUCTED': '#ad1457', 'CONDITIONAL': '#f9a825', 'PARTIAL': '#9e9d24', 'TODO': '#1565c0', 'OPEN': '#757575'}
key = lambda s: s.split(' ')[0]
fig, ax = plt.subplots(figsize=(11, 8.2)); ax.set_xlim(0, 10); ax.set_ylim(0, len(rows) + 1.6); ax.axis('off')
ax.text(0, len(rows) + 1.1, 'Global Pati-Salam on Z2xZ6\' : the 20 things experts will check', fontsize=14, weight='bold')
for i, (n, item, cat, st, ref) in enumerate(rows):
    y = len(rows) - i
    ax.text(0, y, n, fontsize=10, va='center'); ax.text(0.4, y, item, fontsize=10, va='center')
    ax.text(5.9, y, cat, fontsize=9, va='center', color='#555')
    ax.add_patch(plt.Rectangle((7.2, y - 0.38), 1.45, 0.76, color=col[key(st)]))
    ax.text(7.925, y, st, fontsize=8.5, va='center', ha='center', color='white', weight='bold')
    ax.text(8.8, y, ref, fontsize=8, va='center', color='#333')
from collections import Counter
c = Counter(key(r[3]) for r in rows)
ax.text(0, 0.2, '   '.join('%s %d' % (k, v) for k, v in c.items()), fontsize=10, weight='bold')
plt.tight_layout(); plt.savefig('expert_checklist.png', dpi=130)

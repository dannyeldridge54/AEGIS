# AEGIS Optimizer — Standalone Installer Package

## What's Inside

```
aegis-installer/
├── install.bat        ← Double-click to install
├── uninstall.bat      ← Remove AEGIS from your PC
├── README.md          ← This file
└── engine/            ← The optimizer engine
    ├── app.js         ← Desktop app (GUI dashboard)
    ├── dist/          ← AEGIS engine (compiled)
    ├── seeker/dist/   ← Seeker engine (compiled)
    ├── sdk/           ← SDK + CLI + TypeScript types
    ├── saas/          ← REST API server
    ├── package.json   ← Dependencies
    └── LICENSE        ← Commercial license
```

## Installation

### Prerequisites
- **Node.js 18+** — Download from [nodejs.org](https://nodejs.org)
- **Windows 10/11**

### Install
1. Double-click `install.bat`
2. Follow the prompts
3. A desktop shortcut "AEGIS Optimizer" will be created

### What Gets Installed
- Engine files → `%LOCALAPPDATA%\AEGIS-Optimizer\`
- Desktop shortcut → `AEGIS Optimizer`
- Start Menu → `AEGIS Optimizer` folder
- PATH entry → `aegis` command available in any terminal

## Usage

### Desktop App
Double-click the "AEGIS Optimizer" shortcut. Opens a GUI dashboard in your browser with:
- Quick optimization form
- Real-time status monitoring
- API server management
- Built-in documentation

### CLI
```bash
# Single engine optimization
aegis optimize --config my-problem.json

# Dual engine with cross-pollination
aegis dual --config my-problem.json

# Run benchmarks
aegis benchmark

# Start API server
aegis serve --port 3000
```

### Config File Format
```json
{
  "objective": "(p) => (p.x - 3)**2 + (p.y + 2)**2",
  "parameters": [
    { "name": "x", "min": -10, "max": 10 },
    { "name": "y", "min": -10, "max": 10 }
  ],
  "maxEvals": 1000
}
```

### SDK (for developers)
```javascript
const { optimize, dualOptimize } = require('@aegis/optimizer');

const result = await optimize({
  objective: (p) => yourCostFunction(p),
  parameters: [
    { name: 'x', min: 0, max: 100 },
    { name: 'y', min: -50, max: 50 },
  ],
});

console.log(result.best); // { params: { x: 42.7, y: -3.1 }, score: 0.0001 }
```

## Uninstall
Double-click `uninstall.bat` or delete `%LOCALAPPDATA%\AEGIS-Optimizer\`

## License
Copyright © 2012-2026 Danny Lee Eldridge. All rights reserved.
Commercial license — see LICENSE file for terms.

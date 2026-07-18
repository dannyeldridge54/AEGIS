"use strict";
/**
 * AEGIS — Auto-Documentation Generator
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Automatically generates README, API docs, and usage examples
 * from source code analysis (no LLM needed for basic docs).
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.generateDocs = generateDocs;
exports.writeDocs = writeDocs;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
/** Extract exports from TypeScript source files */
function extractExports(sourceDir) {
    const symbols = [];
    const files = getAllTsFiles(sourceDir);
    for (const file of files) {
        const content = fs.readFileSync(file, 'utf-8');
        const lines = content.split('\n');
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            // Exported function
            const fnMatch = line.match(/^export\s+(?:async\s+)?function\s+(\w+)\s*[\(<]/);
            if (fnMatch) {
                const description = getJSDocComment(lines, i);
                symbols.push({
                    name: fnMatch[1],
                    type: 'function',
                    description,
                    file: path.relative(sourceDir, file),
                });
            }
            // Exported class
            const classMatch = line.match(/^export\s+class\s+(\w+)/);
            if (classMatch) {
                symbols.push({
                    name: classMatch[1],
                    type: 'class',
                    description: getJSDocComment(lines, i),
                    file: path.relative(sourceDir, file),
                });
            }
            // Exported interface
            const ifaceMatch = line.match(/^export\s+interface\s+(\w+)/);
            if (ifaceMatch) {
                symbols.push({
                    name: ifaceMatch[1],
                    type: 'interface',
                    description: getJSDocComment(lines, i),
                    file: path.relative(sourceDir, file),
                });
            }
            // Exported const
            const constMatch = line.match(/^export\s+const\s+(\w+)/);
            if (constMatch) {
                symbols.push({
                    name: constMatch[1],
                    type: 'const',
                    description: getJSDocComment(lines, i),
                    file: path.relative(sourceDir, file),
                });
            }
        }
    }
    return symbols;
}
function getJSDocComment(lines, lineIdx) {
    // Look backwards for /** ... */ comment
    let description = '';
    for (let i = lineIdx - 1; i >= 0; i--) {
        const l = lines[i].trim();
        if (l.startsWith('*/'))
            continue;
        if (l.startsWith('*')) {
            const text = l.replace(/^\*\s*/, '').trim();
            if (text && !text.startsWith('@'))
                description = text + (description ? ' ' + description : '');
        }
        if (l.startsWith('/**'))
            break;
        if (!l.startsWith('*') && !l.startsWith('/**') && !l.startsWith('*/') && l !== '')
            break;
    }
    return description;
}
function getAllTsFiles(dir) {
    const results = [];
    if (!fs.existsSync(dir))
        return results;
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory() && entry.name !== 'node_modules' && entry.name !== 'dist') {
            results.push(...getAllTsFiles(fullPath));
        }
        else if (entry.isFile() && entry.name.endsWith('.ts') && !entry.name.endsWith('.test.ts')) {
            results.push(fullPath);
        }
    }
    return results;
}
/** Generate complete API documentation */
function generateDocs(config) {
    const sourceDir = config.sourceDir || './src';
    const symbols = extractExports(sourceDir);
    const classes = symbols.filter(s => s.type === 'class');
    const functions = symbols.filter(s => s.type === 'function');
    const interfaces = symbols.filter(s => s.type === 'interface');
    const constants = symbols.filter(s => s.type === 'const');
    let doc = `# ${config.projectName} — API Reference\n\n`;
    doc += `> ${config.description}\n\n`;
    doc += `---\n\n`;
    // Summary
    doc += `## Overview\n\n`;
    doc += `| Type | Count |\n|------|-------|\n`;
    doc += `| Classes | ${classes.length} |\n`;
    doc += `| Functions | ${functions.length} |\n`;
    doc += `| Interfaces | ${interfaces.length} |\n`;
    doc += `| Constants | ${constants.length} |\n\n`;
    // Classes
    if (classes.length > 0) {
        doc += `## Classes\n\n`;
        for (const cls of classes) {
            doc += `### \`${cls.name}\`\n`;
            if (cls.description)
                doc += `${cls.description}\n`;
            doc += `*Defined in:* \`${cls.file}\`\n\n`;
        }
    }
    // Functions
    if (functions.length > 0) {
        doc += `## Functions\n\n`;
        for (const fn of functions) {
            doc += `### \`${fn.name}()\`\n`;
            if (fn.description)
                doc += `${fn.description}\n`;
            doc += `*Defined in:* \`${fn.file}\`\n\n`;
        }
    }
    // Interfaces
    if (interfaces.length > 0) {
        doc += `## Interfaces\n\n`;
        for (const iface of interfaces) {
            doc += `- **\`${iface.name}\`** — ${iface.description || '*(no description)*'} (\`${iface.file}\`)\n`;
        }
        doc += '\n';
    }
    // Constants
    if (constants.length > 0) {
        doc += `## Constants\n\n`;
        for (const c of constants) {
            doc += `- **\`${c.name}\`** — ${c.description || '*(no description)*'} (\`${c.file}\`)\n`;
        }
        doc += '\n';
    }
    doc += `---\n*Generated by AEGIS Auto-Documentation*\n`;
    return doc;
}
/** Generate and write docs to file */
function writeDocs(config) {
    const doc = generateDocs(config);
    const outputDir = config.outputDir || './docs';
    if (!fs.existsSync(outputDir))
        fs.mkdirSync(outputDir, { recursive: true });
    const outputPath = path.join(outputDir, 'API.md');
    fs.writeFileSync(outputPath, doc);
    return outputPath;
}
//# sourceMappingURL=auto-docs.js.map
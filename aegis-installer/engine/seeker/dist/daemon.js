"use strict";
/**
 * Seeker — Daemon Mode
 * Persistent background daemon: schedules jobs, tracks UFE per job,
 * learns across runs, serves results via HTTP API.
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
exports.SeekerDaemon = void 0;
exports.startDaemon = startDaemon;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const http = __importStar(require("http"));
const agent_1 = require("./agent");
const memory_1 = require("./memory");
class SeekerDaemon {
    constructor(config) {
        this.jobs = new Map();
        this.jobStates = new Map();
        this.running = false;
        this.startTime = 0;
        this.server = null;
        this.intervals = [];
        this.activeAgents = new Map();
        this.logStream = null;
        this.config = {
            name: config?.name || 'Seeker Daemon',
            workDir: config?.workDir || path.join(process.cwd(), '.seeker-daemon'),
            apiPort: config?.apiPort ?? 4444,
            webhookUrl: config?.webhookUrl || '',
            maxConcurrent: config?.maxConcurrent || 4,
            saveInterval: config?.saveInterval || 60,
            language: config?.language || 'en',
            logFile: config?.logFile || '',
            enableMemory: config?.enableMemory !== false,
        };
        if (!fs.existsSync(this.config.workDir))
            fs.mkdirSync(this.config.workDir, { recursive: true });
        this.memory = new memory_1.Memory(path.join(this.config.workDir, 'memory.json'));
        if (this.config.logFile) {
            const logDir = path.dirname(this.config.logFile);
            if (!fs.existsSync(logDir))
                fs.mkdirSync(logDir, { recursive: true });
            this.logStream = fs.createWriteStream(this.config.logFile, { flags: 'a' });
        }
        this.loadState();
    }
    addJob(job) {
        this.jobs.set(job.id, job);
        if (!this.jobStates.has(job.id)) {
            this.jobStates.set(job.id, {
                id: job.id, status: 'queued', runs: 0, totalEvals: 0,
                best: null, lastRun: 0, nextRun: Date.now(), errors: [],
                ufeRatio: 0, discoveries: 0, history: [],
            });
        }
        this.log(`Job added: ${job.name} [${job.id}] schedule=${job.schedule}`);
    }
    removeJob(id) {
        const agent = this.activeAgents.get(id);
        if (agent)
            agent.stop('Job removed');
        this.activeAgents.delete(id);
        this.jobs.delete(id);
        this.jobStates.delete(id);
        return true;
    }
    pauseJob(id) {
        const state = this.jobStates.get(id);
        if (!state)
            return;
        state.status = 'paused';
        const agent = this.activeAgents.get(id);
        if (agent) {
            agent.stop('Paused');
            this.activeAgents.delete(id);
        }
    }
    resumeJob(id) {
        const state = this.jobStates.get(id);
        if (state && state.status === 'paused') {
            state.status = 'queued';
            state.nextRun = Date.now();
        }
    }
    getJobStates() { return [...this.jobStates.values()]; }
    async start() {
        this.running = true;
        this.startTime = Date.now();
        this.printBanner();
        this.log(`Starting with ${this.jobs.size} jobs, max ${this.config.maxConcurrent} concurrent`);
        if (this.config.apiPort > 0)
            this.startAPI();
        const saveTimer = setInterval(() => this.saveState(), this.config.saveInterval * 1000);
        this.intervals.push(saveTimer);
        const loopTimer = setInterval(() => this.tick(), 1000);
        this.intervals.push(loopTimer);
        this.log('Daemon running. Press Ctrl+C to stop.');
    }
    stop() {
        this.running = false;
        this.log('Shutting down...');
        for (const [, agent] of this.activeAgents)
            agent.stop('Daemon shutdown');
        for (const timer of this.intervals)
            clearInterval(timer);
        this.intervals = [];
        this.server?.close();
        this.saveState();
        this.memory.save();
        this.log('Daemon stopped.');
        this.logStream?.end();
    }
    async tick() {
        if (!this.running)
            return;
        const now = Date.now();
        const activeCount = [...this.jobStates.values()].filter(s => s.status === 'running').length;
        if (activeCount >= this.config.maxConcurrent)
            return;
        const ready = [...this.jobStates.entries()]
            .filter(([_, state]) => state.status === 'queued' && state.nextRun <= now)
            .sort((a, b) => {
            const jobA = this.jobs.get(a[0]);
            const jobB = this.jobs.get(b[0]);
            return (jobB?.priority || 0) - (jobA?.priority || 0);
        });
        if (ready.length === 0)
            return;
        this.runJob(ready[0][0]);
    }
    async runJob(jobId) {
        const job = this.jobs.get(jobId);
        const state = this.jobStates.get(jobId);
        if (!job || !state)
            return;
        state.status = 'running';
        state.lastRun = Date.now();
        this.log(`Running: ${job.name}`);
        if (this.config.enableMemory) {
            const suggested = this.memory.recallStrategy(job.name, job.task.parameters.length);
            if (suggested)
                this.log(`  Memory suggests: ${suggested} strategy`);
        }
        const agent = new agent_1.SeekerAgent(job.task, {
            maxEvals: job.config?.maxEvals || 3000,
            verbosity: 'silent',
            reportInterval: 10,
            language: this.config.language,
            ...job.config,
        });
        this.activeAgents.set(jobId, agent);
        agent.on((event) => {
            if (event.type === 'new_best') {
                if (!state.best || event.result.score < state.best.score) {
                    state.best = event.result;
                }
                if (event.improvement > 10) {
                    this.alert(`[${job.name}] Major improvement: ${event.improvement.toFixed(4)}`);
                }
            }
            if (event.type === 'discovery') {
                state.discoveries++;
            }
        });
        try {
            const result = await agent.run();
            const currentState = this.jobStates.get(jobId);
            if (!currentState || currentState.status === 'paused') {
                this.activeAgents.delete(jobId);
                return;
            }
            currentState.status = 'completed';
            currentState.runs++;
            currentState.totalEvals += result.totalEvals;
            currentState.ufeRatio = result.ufe.ufeRatio;
            if (result.best && (!currentState.best || result.best.score < currentState.best.score)) {
                currentState.best = result.best;
            }
            currentState.history.push({
                timestamp: Date.now(), score: result.best?.score || Infinity,
                evals: result.totalEvals, ufeRatio: result.ufe.ufeRatio,
            });
            if (currentState.history.length > 100)
                currentState.history = currentState.history.slice(-50);
            this.log(`  Done: ${job.name} → score=${result.best?.score.toFixed(6)} UFE=${(result.ufe.ufeRatio * 100).toFixed(1)}% (${result.totalEvals} evals, ${result.discoveries.length} discoveries)`);
            if (this.config.enableMemory && result.best) {
                this.memory.learnFromRun(job.name, {
                    bestScore: result.best.score,
                    bestParams: result.best.params,
                    topStrategy: result.strategies[0]?.type || 'unknown',
                    totalEvals: result.totalEvals,
                    discoveries: result.discoveries.length,
                    ufe: result.ufe,
                    allDiscoveries: result.discoveries,
                });
                this.memory.save();
            }
            // Chain to next job
            if (job.chainTo && result.best) {
                const nextJob = this.jobs.get(job.chainTo);
                const nextState = this.jobStates.get(job.chainTo);
                if (nextJob && nextState && nextState.status !== 'running') {
                    nextJob.task.chainedInput = result.best;
                    nextState.status = 'queued';
                    nextState.nextRun = Date.now();
                }
            }
            // Reschedule
            if (job.schedule === 'continuous') {
                currentState.status = 'queued';
                currentState.nextRun = Date.now() + 5000;
            }
            else if (typeof job.schedule === 'number') {
                currentState.status = 'queued';
                currentState.nextRun = Date.now() + job.schedule * 1000;
            }
        }
        catch (err) {
            const currentState = this.jobStates.get(jobId);
            if (currentState) {
                currentState.status = 'failed';
                currentState.errors.push(`${new Date().toISOString()}: ${err.message}`);
                if (currentState.errors.length > 20)
                    currentState.errors = currentState.errors.slice(-10);
                if (job.schedule === 'continuous' || typeof job.schedule === 'number') {
                    const backoff = Math.min(60000, 5000 * Math.pow(2, Math.min(currentState.errors.length, 5)));
                    currentState.status = 'queued';
                    currentState.nextRun = Date.now() + backoff;
                    this.log(`  RETRY: ${job.name} in ${backoff / 1000}s`);
                }
            }
            this.log(`  ERROR: ${job.name} — ${err.message}`);
        }
        this.activeAgents.delete(jobId);
    }
    startAPI() {
        this.server = http.createServer((req, res) => {
            const url = req.url || '/';
            res.setHeader('Content-Type', 'application/json');
            res.setHeader('Access-Control-Allow-Origin', '*');
            if (url === '/api/status') {
                res.end(JSON.stringify({
                    name: this.config.name, uptime: (Date.now() - this.startTime) / 1000,
                    jobs: this.getJobStates(), memory: this.memory.getSize(),
                    activeAgents: this.activeAgents.size,
                }));
            }
            else if (url === '/api/jobs') {
                res.end(JSON.stringify(this.getJobStates()));
            }
            else if (url === '/api/best') {
                const bests = {};
                for (const [id, state] of this.jobStates) {
                    if (state.best)
                        bests[id] = { score: state.best.score, params: state.best.params, ufeRatio: state.ufeRatio };
                }
                res.end(JSON.stringify(bests));
            }
            else if (url === '/api/memory') {
                res.end(JSON.stringify(this.memory.recent(20)));
            }
            else if (url.startsWith('/api/job/')) {
                const jobId = url.split('/api/job/')[1];
                res.end(JSON.stringify(this.jobStates.get(jobId) || { error: 'not found' }));
            }
            else {
                res.end(JSON.stringify({ endpoints: ['/api/status', '/api/jobs', '/api/best', '/api/memory', '/api/job/:id'] }));
            }
        });
        this.server.listen(this.config.apiPort, () => {
            this.log(`API: http://localhost:${this.config.apiPort}`);
        });
    }
    alert(message) {
        this.log(`🔔 ALERT: ${message}`);
        if (this.config.webhookUrl) {
            const body = JSON.stringify({ text: message, timestamp: new Date().toISOString() });
            try {
                const parsed = new URL(this.config.webhookUrl);
                const lib = parsed.protocol === 'https:' ? require('https') : require('http');
                const req = lib.request(this.config.webhookUrl, {
                    method: 'POST', headers: { 'Content-Type': 'application/json' },
                });
                req.on('error', () => { });
                req.write(body);
                req.end();
            }
            catch { }
        }
    }
    saveState() {
        const statePath = path.join(this.config.workDir, 'daemon-state.json');
        fs.writeFileSync(statePath, JSON.stringify({
            config: this.config, jobStates: [...this.jobStates.entries()],
            startTime: this.startTime, savedAt: new Date().toISOString(),
        }, null, 2));
    }
    loadState() {
        const statePath = path.join(this.config.workDir, 'daemon-state.json');
        if (!fs.existsSync(statePath))
            return;
        try {
            const data = JSON.parse(fs.readFileSync(statePath, 'utf-8'));
            if (data.jobStates) {
                for (const [id, state] of data.jobStates) {
                    if (state.status === 'running')
                        state.status = 'queued';
                    this.jobStates.set(id, state);
                }
            }
        }
        catch { }
    }
    log(msg) {
        const ts = new Date().toISOString().slice(11, 19);
        const line = `[${ts}] ${msg}`;
        console.log(line);
        this.logStream?.write(line + '\n');
    }
    printBanner() {
        console.log(`
╔═══════════════════════════════════════════════════════════╗
║   ____            _                                       ║
║  / ___|  ___  ___| | _____ _ __                           ║
║  \\___ \\ / _ \\/ _ \\ |/ / _ \\ '__|                          ║
║   ___) |  __/  __/   <  __/ |     Daemon                  ║
║  |____/ \\___|\\___|_|\\_\\___|_|                             ║
║                                                           ║
║   ${this.config.name.padEnd(51)}║
║   Autonomous • Recording • Never Sleeps                  ║
╚═══════════════════════════════════════════════════════════╝`);
    }
    getMemory() { return this.memory; }
    getUptime() { return (Date.now() - this.startTime) / 1000; }
    isRunning() { return this.running; }
}
exports.SeekerDaemon = SeekerDaemon;
function startDaemon(name, jobs, config) {
    const daemon = new SeekerDaemon({ name, ...config });
    for (const job of jobs)
        daemon.addJob(job);
    daemon.start();
    return daemon;
}
//# sourceMappingURL=daemon.js.map
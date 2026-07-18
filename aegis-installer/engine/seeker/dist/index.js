"use strict";
/**
 * Seeker — Public API
 * Autonomous discovery engine that solves UFE optimization,
 * hunts anomalies, surfaces discoveries, scripts, records, and learns.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.fTGravity_Exponential = exports.fTGravity_Logarithmic = exports.fTGravity_BornInfeld = exports.fTGravity_PowerLaw = exports.torsionWaveResidual = exports.ufeTorsionFunctional = exports.fTCosmologyResidual = exports.einsteinCartanResidual = exports.crossDomainUFE = exports.crossDomainTask = exports.torsionWaveTask = exports.ufeTorsionTask = exports.fTGravityTask = exports.einsteinCartanTask = exports.torsionTasks = exports.createMonitor = exports.LiveMonitor = exports.warmStartFrom = exports.autoSave = exports.loadCheckpoint = exports.saveCheckpoint = exports.differentialEvolutionPlugin = exports.latinHypercubePlugin = exports.plugins = exports.Memory = exports.createRecorder = exports.DataRecorder = exports.startDaemon = exports.SeekerDaemon = exports.SelfEvolver = exports.Swarm = exports.multiOptimize = exports.parallelOptimize = exports.benchmarkFunctions = exports.runBenchmarks = exports.compareModels = exports.ELORating = exports.cohensD = exports.wilcoxonSignedRank = exports.mannWhitneyU = exports.bootstrapCI = exports.formatDuration = exports.getMessages = exports.MetaLearner = exports.AnomalyDetector = exports.UFETracker = exports.SeededRNG = exports.optimize = exports.seeker = exports.SeekerAgent = void 0;
exports.createEquationWriter = exports.EquationWriter = exports.HZ_OBSERVATIONS = exports.computeSpatialAnomalies = exports.computeAxialTorsion = exports.computeTraceVector = exports.computeTorsionScalar = void 0;
// Core
var agent_1 = require("./agent");
Object.defineProperty(exports, "SeekerAgent", { enumerable: true, get: function () { return agent_1.SeekerAgent; } });
Object.defineProperty(exports, "seeker", { enumerable: true, get: function () { return agent_1.seeker; } });
Object.defineProperty(exports, "optimize", { enumerable: true, get: function () { return agent_1.optimize; } });
// Seeded RNG
var rng_1 = require("./rng");
Object.defineProperty(exports, "SeededRNG", { enumerable: true, get: function () { return rng_1.SeededRNG; } });
// UFE + Anomaly Detection
var ufe_1 = require("./ufe");
Object.defineProperty(exports, "UFETracker", { enumerable: true, get: function () { return ufe_1.UFETracker; } });
Object.defineProperty(exports, "AnomalyDetector", { enumerable: true, get: function () { return ufe_1.AnomalyDetector; } });
// Strategies
var strategies_1 = require("./strategies");
Object.defineProperty(exports, "MetaLearner", { enumerable: true, get: function () { return strategies_1.MetaLearner; } });
// Language
var language_1 = require("./language");
Object.defineProperty(exports, "getMessages", { enumerable: true, get: function () { return language_1.getMessages; } });
Object.defineProperty(exports, "formatDuration", { enumerable: true, get: function () { return language_1.formatDuration; } });
// Statistical Engine
var statistics_1 = require("./statistics");
Object.defineProperty(exports, "bootstrapCI", { enumerable: true, get: function () { return statistics_1.bootstrapCI; } });
Object.defineProperty(exports, "mannWhitneyU", { enumerable: true, get: function () { return statistics_1.mannWhitneyU; } });
Object.defineProperty(exports, "wilcoxonSignedRank", { enumerable: true, get: function () { return statistics_1.wilcoxonSignedRank; } });
Object.defineProperty(exports, "cohensD", { enumerable: true, get: function () { return statistics_1.cohensD; } });
Object.defineProperty(exports, "ELORating", { enumerable: true, get: function () { return statistics_1.ELORating; } });
// Model Comparison
var comparison_1 = require("./comparison");
Object.defineProperty(exports, "compareModels", { enumerable: true, get: function () { return comparison_1.compareModels; } });
// Benchmarks
var benchmarks_1 = require("./benchmarks");
Object.defineProperty(exports, "runBenchmarks", { enumerable: true, get: function () { return benchmarks_1.runBenchmarks; } });
Object.defineProperty(exports, "benchmarkFunctions", { enumerable: true, get: function () { return benchmarks_1.benchmarkFunctions; } });
// Parallel
var parallel_1 = require("./parallel");
Object.defineProperty(exports, "parallelOptimize", { enumerable: true, get: function () { return parallel_1.parallelOptimize; } });
// Multi-Objective
var multi_objective_1 = require("./multi-objective");
Object.defineProperty(exports, "multiOptimize", { enumerable: true, get: function () { return multi_objective_1.multiOptimize; } });
// Swarm
var swarm_1 = require("./swarm");
Object.defineProperty(exports, "Swarm", { enumerable: true, get: function () { return swarm_1.Swarm; } });
// Self-Evolution
var self_evolve_1 = require("./self-evolve");
Object.defineProperty(exports, "SelfEvolver", { enumerable: true, get: function () { return self_evolve_1.SelfEvolver; } });
// Daemon
var daemon_1 = require("./daemon");
Object.defineProperty(exports, "SeekerDaemon", { enumerable: true, get: function () { return daemon_1.SeekerDaemon; } });
Object.defineProperty(exports, "startDaemon", { enumerable: true, get: function () { return daemon_1.startDaemon; } });
// Data Recorder
var recorder_1 = require("./recorder");
Object.defineProperty(exports, "DataRecorder", { enumerable: true, get: function () { return recorder_1.DataRecorder; } });
Object.defineProperty(exports, "createRecorder", { enumerable: true, get: function () { return recorder_1.createRecorder; } });
// Memory
var memory_1 = require("./memory");
Object.defineProperty(exports, "Memory", { enumerable: true, get: function () { return memory_1.Memory; } });
// Plugins
var plugins_1 = require("./plugins");
Object.defineProperty(exports, "plugins", { enumerable: true, get: function () { return plugins_1.plugins; } });
Object.defineProperty(exports, "latinHypercubePlugin", { enumerable: true, get: function () { return plugins_1.latinHypercubePlugin; } });
Object.defineProperty(exports, "differentialEvolutionPlugin", { enumerable: true, get: function () { return plugins_1.differentialEvolutionPlugin; } });
// Warm Start
var warm_start_1 = require("./warm-start");
Object.defineProperty(exports, "saveCheckpoint", { enumerable: true, get: function () { return warm_start_1.saveCheckpoint; } });
Object.defineProperty(exports, "loadCheckpoint", { enumerable: true, get: function () { return warm_start_1.loadCheckpoint; } });
Object.defineProperty(exports, "autoSave", { enumerable: true, get: function () { return warm_start_1.autoSave; } });
Object.defineProperty(exports, "warmStartFrom", { enumerable: true, get: function () { return warm_start_1.warmStartFrom; } });
// Live Monitor
var monitor_1 = require("./monitor");
Object.defineProperty(exports, "LiveMonitor", { enumerable: true, get: function () { return monitor_1.LiveMonitor; } });
Object.defineProperty(exports, "createMonitor", { enumerable: true, get: function () { return monitor_1.createMonitor; } });
// Torsion Field Theory
var torsion_1 = require("./torsion");
Object.defineProperty(exports, "torsionTasks", { enumerable: true, get: function () { return torsion_1.torsionTasks; } });
Object.defineProperty(exports, "einsteinCartanTask", { enumerable: true, get: function () { return torsion_1.einsteinCartanTask; } });
Object.defineProperty(exports, "fTGravityTask", { enumerable: true, get: function () { return torsion_1.fTGravityTask; } });
Object.defineProperty(exports, "ufeTorsionTask", { enumerable: true, get: function () { return torsion_1.ufeTorsionTask; } });
Object.defineProperty(exports, "torsionWaveTask", { enumerable: true, get: function () { return torsion_1.torsionWaveTask; } });
Object.defineProperty(exports, "crossDomainTask", { enumerable: true, get: function () { return torsion_1.crossDomainTask; } });
Object.defineProperty(exports, "crossDomainUFE", { enumerable: true, get: function () { return torsion_1.crossDomainUFE; } });
Object.defineProperty(exports, "einsteinCartanResidual", { enumerable: true, get: function () { return torsion_1.einsteinCartanResidual; } });
Object.defineProperty(exports, "fTCosmologyResidual", { enumerable: true, get: function () { return torsion_1.fTCosmologyResidual; } });
Object.defineProperty(exports, "ufeTorsionFunctional", { enumerable: true, get: function () { return torsion_1.ufeTorsionFunctional; } });
Object.defineProperty(exports, "torsionWaveResidual", { enumerable: true, get: function () { return torsion_1.torsionWaveResidual; } });
Object.defineProperty(exports, "fTGravity_PowerLaw", { enumerable: true, get: function () { return torsion_1.fTGravity_PowerLaw; } });
Object.defineProperty(exports, "fTGravity_BornInfeld", { enumerable: true, get: function () { return torsion_1.fTGravity_BornInfeld; } });
Object.defineProperty(exports, "fTGravity_Logarithmic", { enumerable: true, get: function () { return torsion_1.fTGravity_Logarithmic; } });
Object.defineProperty(exports, "fTGravity_Exponential", { enumerable: true, get: function () { return torsion_1.fTGravity_Exponential; } });
Object.defineProperty(exports, "computeTorsionScalar", { enumerable: true, get: function () { return torsion_1.computeTorsionScalar; } });
Object.defineProperty(exports, "computeTraceVector", { enumerable: true, get: function () { return torsion_1.computeTraceVector; } });
Object.defineProperty(exports, "computeAxialTorsion", { enumerable: true, get: function () { return torsion_1.computeAxialTorsion; } });
Object.defineProperty(exports, "computeSpatialAnomalies", { enumerable: true, get: function () { return torsion_1.computeSpatialAnomalies; } });
Object.defineProperty(exports, "HZ_OBSERVATIONS", { enumerable: true, get: function () { return torsion_1.HZ_OBSERVATIONS; } });
var equation_writer_1 = require("./equation-writer");
Object.defineProperty(exports, "EquationWriter", { enumerable: true, get: function () { return equation_writer_1.EquationWriter; } });
Object.defineProperty(exports, "createEquationWriter", { enumerable: true, get: function () { return equation_writer_1.createEquationWriter; } });
//# sourceMappingURL=index.js.map
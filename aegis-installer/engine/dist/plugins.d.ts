/**
 * AEGIS — Plugin System
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Extensible plugin architecture for custom strategies, reporters,
 * and evaluation transforms. Add your own optimization algorithms.
 */
import { ParameterDef, EvalResult, AgentEvent } from './interfaces';
export interface StrategyPlugin {
    /** Unique name (becomes a StrategyType) */
    name: string;
    /** Human description */
    description: string;
    /** Generate next parameter set to evaluate */
    suggest(params: ParameterDef[], best: EvalResult | null, history: EvalResult[], config: Record<string, any>): Record<string, number>;
    /** Default configuration */
    defaultConfig?: Record<string, any>;
}
export interface ReporterPlugin {
    name: string;
    /** Called on every agent event */
    onEvent(event: AgentEvent): void;
    /** Called on shutdown */
    onComplete?(state: any): void;
}
export interface TransformPlugin {
    name: string;
    /** Transform parameters before evaluation */
    preEval?(params: Record<string, number>): Record<string, number>;
    /** Transform score after evaluation */
    postEval?(score: number, params: Record<string, number>): number;
}
declare class PluginRegistry {
    private strategies;
    private reporters;
    private transforms;
    registerStrategy(plugin: StrategyPlugin): void;
    registerReporter(plugin: ReporterPlugin): void;
    registerTransform(plugin: TransformPlugin): void;
    getStrategy(name: string): StrategyPlugin | undefined;
    getAllStrategies(): StrategyPlugin[];
    getAllReporters(): ReporterPlugin[];
    getAllTransforms(): TransformPlugin[];
    listPlugins(): {
        strategies: string[];
        reporters: string[];
        transforms: string[];
    };
}
export declare const plugins: PluginRegistry;
/** Latin Hypercube Sampling — better coverage than pure random */
export declare const latinHypercubePlugin: StrategyPlugin;
/** Differential Evolution — powerful for non-convex problems */
export declare const differentialEvolutionPlugin: StrategyPlugin;
/** JSON file reporter — saves all events to a file */
export declare const jsonReporterPlugin: ReporterPlugin;
export {};
//# sourceMappingURL=plugins.d.ts.map
/**
 * Seeker — Plugin System
 * Extensible strategies, reporters, and transforms.
 * Includes DE and Latin Hypercube built-in.
 */
import { ParameterDef, EvalResult, AgentEvent } from './interfaces';
import { SeededRNG } from './rng';
export interface StrategyPlugin {
    name: string;
    description: string;
    suggest(params: ParameterDef[], best: EvalResult | null, history: EvalResult[], config: Record<string, any>, rng: SeededRNG): Record<string, number>;
    defaultConfig?: Record<string, any>;
}
export interface ReporterPlugin {
    name: string;
    onEvent(event: AgentEvent): void;
    onComplete?(state: any): void;
}
export interface TransformPlugin {
    name: string;
    preEval?(params: Record<string, number>): Record<string, number>;
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
export declare const latinHypercubePlugin: StrategyPlugin;
export declare const differentialEvolutionPlugin: StrategyPlugin;
export {};
//# sourceMappingURL=plugins.d.ts.map
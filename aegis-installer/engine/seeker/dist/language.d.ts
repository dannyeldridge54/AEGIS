/**
 * Seeker — Localization / Language System
 * Multi-language output. Rebranded for Seeker.
 */
export type LangCode = 'en' | 'es' | 'fr' | 'de' | 'ja' | 'zh' | 'pt' | 'ko';
interface Messages {
    started: string;
    newBest: string;
    converged: string;
    exploring: string;
    exploiting: string;
    curious: string;
    discovery: string;
    strategySwitch: string;
    progress: string;
    stopped: string;
    evalCount: string;
    bestScore: string;
    improvement: string;
    noImprovement: string;
    timeElapsed: string;
    phaseChange: string;
}
export declare function getMessages(lang: string): Messages;
export declare function formatDuration(seconds: number): string;
export {};
//# sourceMappingURL=language.d.ts.map
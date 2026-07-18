/**
 * AEGIS — Localization / Language System
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Multi-language output support. Add new languages by extending MESSAGES.
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
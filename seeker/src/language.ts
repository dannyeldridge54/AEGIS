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

const MESSAGES: Record<LangCode, Messages> = {
  en: {
    started: '🔎 Seeker launched',
    newBest: '⭐ New best found!',
    converged: '✅ Converged!',
    exploring: '🔍 Exploring...',
    exploiting: '🎯 Exploiting best region...',
    curious: '🧭 Curiosity-driven exploration...',
    discovery: '💡 Discovery:',
    strategySwitch: '🔄 Strategy switch:',
    progress: '📊 Progress:',
    stopped: '⏹️ Seeker stopped.',
    evalCount: 'evaluations',
    bestScore: 'Best score',
    improvement: 'improvement',
    noImprovement: 'no improvement in',
    timeElapsed: 'Time elapsed',
    phaseChange: '📍 Phase:',
  },
  es: {
    started: '🔎 Seeker iniciado',
    newBest: '⭐ ¡Nuevo mejor encontrado!',
    converged: '✅ ¡Convergido!',
    exploring: '🔍 Explorando...',
    exploiting: '🎯 Explotando mejor región...',
    curious: '🧭 Exploración por curiosidad...',
    discovery: '💡 Descubrimiento:',
    strategySwitch: '🔄 Cambio de estrategia:',
    progress: '📊 Progreso:',
    stopped: '⏹️ Seeker detenido.',
    evalCount: 'evaluaciones',
    bestScore: 'Mejor puntuación',
    improvement: 'mejora',
    noImprovement: 'sin mejora en',
    timeElapsed: 'Tiempo transcurrido',
    phaseChange: '📍 Fase:',
  },
  fr: {
    started: '🔎 Seeker lancé',
    newBest: '⭐ Nouveau meilleur trouvé !',
    converged: '✅ Convergé !',
    exploring: '🔍 Exploration...',
    exploiting: '🎯 Exploitation de la meilleure zone...',
    curious: '🧭 Exploration par curiosité...',
    discovery: '💡 Découverte :',
    strategySwitch: '🔄 Changement de stratégie :',
    progress: '📊 Progrès :',
    stopped: '⏹️ Seeker arrêté.',
    evalCount: 'évaluations',
    bestScore: 'Meilleur score',
    improvement: 'amélioration',
    noImprovement: 'pas d\'amélioration depuis',
    timeElapsed: 'Temps écoulé',
    phaseChange: '📍 Phase :',
  },
  de: {
    started: '🔎 Seeker gestartet',
    newBest: '⭐ Neues Bestes gefunden!',
    converged: '✅ Konvergiert!',
    exploring: '🔍 Erkundung...',
    exploiting: '🎯 Beste Region ausnutzen...',
    curious: '🧭 Neugier-Erkundung...',
    discovery: '💡 Entdeckung:',
    strategySwitch: '🔄 Strategiewechsel:',
    progress: '📊 Fortschritt:',
    stopped: '⏹️ Seeker gestoppt.',
    evalCount: 'Auswertungen',
    bestScore: 'Beste Punktzahl',
    improvement: 'Verbesserung',
    noImprovement: 'keine Verbesserung seit',
    timeElapsed: 'Verstrichene Zeit',
    phaseChange: '📍 Phase:',
  },
  ja: {
    started: '🔎 Seeker開始',
    newBest: '⭐ 新しい最良値発見！',
    converged: '✅ 収束完了！',
    exploring: '🔍 探索中...',
    exploiting: '🎯 最良領域を活用中...',
    curious: '🧭 好奇心駆動探索...',
    discovery: '💡 発見:',
    strategySwitch: '🔄 戦略切替:',
    progress: '📊 進捗:',
    stopped: '⏹️ Seeker停止',
    evalCount: '回評価',
    bestScore: '最良スコア',
    improvement: '改善',
    noImprovement: '改善なし',
    timeElapsed: '経過時間',
    phaseChange: '📍 フェーズ:',
  },
  zh: {
    started: '🔎 Seeker已启动',
    newBest: '⭐ 发现新最优！',
    converged: '✅ 已收敛！',
    exploring: '🔍 探索中...',
    exploiting: '🎯 利用最优区域...',
    curious: '🧭 好奇心驱动探索...',
    discovery: '💡 发现:',
    strategySwitch: '🔄 策略切换:',
    progress: '📊 进度:',
    stopped: '⏹️ Seeker已停止',
    evalCount: '次评估',
    bestScore: '最佳分数',
    improvement: '改进',
    noImprovement: '无改进',
    timeElapsed: '已用时间',
    phaseChange: '📍 阶段:',
  },
  pt: {
    started: '🔎 Seeker iniciado',
    newBest: '⭐ Novo melhor encontrado!',
    converged: '✅ Convergido!',
    exploring: '🔍 Explorando...',
    exploiting: '🎯 Explorando melhor região...',
    curious: '🧭 Exploração por curiosidade...',
    discovery: '💡 Descoberta:',
    strategySwitch: '🔄 Mudança de estratégia:',
    progress: '📊 Progresso:',
    stopped: '⏹️ Seeker parado.',
    evalCount: 'avaliações',
    bestScore: 'Melhor pontuação',
    improvement: 'melhoria',
    noImprovement: 'sem melhoria em',
    timeElapsed: 'Tempo decorrido',
    phaseChange: '📍 Fase:',
  },
  ko: {
    started: '🔎 Seeker 시작',
    newBest: '⭐ 새로운 최적값 발견!',
    converged: '✅ 수렴 완료!',
    exploring: '🔍 탐색 중...',
    exploiting: '🎯 최적 영역 활용 중...',
    curious: '🧭 호기심 기반 탐색...',
    discovery: '💡 발견:',
    strategySwitch: '🔄 전략 전환:',
    progress: '📊 진행 상황:',
    stopped: '⏹️ Seeker 정지',
    evalCount: '회 평가',
    bestScore: '최고 점수',
    improvement: '개선',
    noImprovement: '개선 없음',
    timeElapsed: '경과 시간',
    phaseChange: '📍 단계:',
  },
};

export function getMessages(lang: string): Messages {
  return MESSAGES[(lang as LangCode)] || MESSAGES.en;
}

export function formatDuration(seconds: number): string {
  if (seconds < 60) return `${seconds.toFixed(1)}s`;
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ${Math.floor(seconds % 60)}s`;
  return `${Math.floor(seconds / 3600)}h ${Math.floor((seconds % 3600) / 60)}m`;
}

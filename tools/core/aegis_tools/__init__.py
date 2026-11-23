"""AEGIS toolkits for CubeMind: a whitelisted tool registry the model can call as
    TOOL: <name> {"json": "args"}
Each call runs in an isolated subprocess with a time limit and returns JSON. Toolkits come from an AEGIS checkout (env AEGIS_DIR,
default ~/aegis or the bundled copy in ./aegis_bundle). Tools (all validated in AEGIS; D-numbers in each docstring):
  janus_single   n_s, r, α_s, β_s for a single-field potential V(phi) (sympy expression), at N*            (Janus core; D1035, D1127, D1146–D1149)
  janus_mf       exact multi-field n_s, r, α_s for V = ½ Σ m_i² φ_i² from φ_init                         (Janus-MF; D1162)
  janus_lt       late-universe distances/growth for flat w0waCDM: D_M, H, f, D, fσ8 at z                   (Janus-LT; D1041–D1134)
  kaluza_tensor  lowest tensor KK masses² of the D-dim tadpole vacuum (γ subcritical), cutoff ε           (KALUZA; D1036, D1160)
  kaluza_stable  scalar-sector sufficient stability check (BTR Eq. 5.10)                                  (KALUZA; D1140)
  lock_lint      LOCKBENCH lock checker on a lock text                                                     (D1164)
  lock_verdict   LOCKBENCH claims evaluator: lock text + results dict → verdicts                           (D1163)"""
from .registry import TOOLS, call, TOOL_INTRO

# (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""J2b nested-model guard (20 Nov 2026). A model that CONTAINS another (ΛCDM ⊂ thread ⊂ coupled thread; phi^2 ⊂ phi^2 + R^2 ...)
can never have a higher minimum chi^2 than the model inside it. If a fit reports one, the minimiser failed, and every
Δχ² built on that number is wrong. That is what happened in D1724 (coupled +0.90 above ΛCDM) and D1725 (coupled above
the thread on 2 of 3 sets). This guard checks a set of fit results against declared nestings before anything is scored.

check(chi2, nest, tol=0.5) -> list of violations; each says which pair failed and by how much.
best_lower_bound(chi2, nest) -> for each model, the tightest value its true minimum must sit below (the min over every
model it contains), so a report can quote 'chi2 <= X' instead of a failed number."""

def check(chi2, nest, tol=0.5):
    """chi2: {model: min chi2}; nest: [(inner, outer), ...] meaning inner ⊂ outer. tol: allowed numerical slack."""
    out = []
    for inner, outer in nest:
        if inner in chi2 and outer in chi2 and chi2[outer] > chi2[inner] + tol:
            out.append(dict(inner=inner, outer=outer, excess=chi2[outer] - chi2[inner],
                            message=f'{outer} chi2 is {chi2[outer] - chi2[inner]:.2f} ABOVE {inner}, which it contains: minimiser failed'))
    return out

def best_lower_bound(chi2, nest):
    """The true minimum of each model is <= its own value and <= that of every model nested inside it (transitively)."""
    inside = {}
    for a, b in nest: inside.setdefault(b, set()).add(a)
    def all_inside(m, seen=None):
        seen = seen or set()
        for a in inside.get(m, ()):
            if a not in seen: seen.add(a); all_inside(a, seen)
        return seen
    return {m: min([v] + [chi2[a] for a in all_inside(m) if a in chi2]) for m, v in chi2.items()}

def report(chi2, nest, tol=0.5):
    v = check(chi2, nest, tol)
    return 'NESTED OK' if not v else 'NESTED VIOLATION\n' + '\n'.join('  ' + x['message'] for x in v)

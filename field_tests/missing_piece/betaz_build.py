"""Helper for the beta(z) model: load the AxiCLASS_coupled_betabins build (MISSING-PIECE beta(z); see PREREG_BETAZ.md).
Sets sys.path so `import classy` gets that build; must be imported before anything imports classy. AI-assisted."""
import os, sys, types, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); AEG = os.path.abspath(os.path.join(HERE, "..", ".."))
BUILD = os.path.join(os.environ.get("TWIST_BUILDS", os.path.expanduser("~")), "AxiCLASS_coupled_betabins")
assert "classy" not in sys.modules, "import betaz_build before classy"
sys.path.insert(0, os.path.join(BUILD, "python", "build", [d for d in os.listdir(os.path.join(BUILD, "python", "build")) if d.startswith("lib")][0]))
for n in ("candl", "candl.interface", "spt_candl_data"):
    sys.modules.setdefault(n, types.SimpleNamespace(CandlCobayaLikelihood=None, SPT3G_D1_TnE=None, interface=None))
sys.modules["candl"].interface = sys.modules["candl.interface"]
sys.path.insert(1, os.path.join(AEG, "cmb-fit", "axiclass"))
import early_late_spa as E, spiral_guess
import classy
assert BUILD in classy.__file__, classy.__file__
SPIRAL = {k: v for k, v in E.make("ax_spa_spiraltwist_kappa1_nlfix")["theory"]["classytwist"]["extra_args"].items()
          if k not in ("lensing", "l_max_scalars", "non_linear")}

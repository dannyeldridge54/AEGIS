import ast
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "nlfix" / "patch_nlfix.py"


class PatchTests(unittest.TestCase):
    def test_exact_anchors_and_idempotence(self):
        tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
        assignments = [
            node for node in tree.body
            if isinstance(node, ast.Assign)
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id in {"SCF_OUT", "W_EFF", "EDITS"}
        ]
        namespace = {}
        exec(compile(ast.Module(body=assignments, type_ignores=[]), str(SCRIPT), "exec"), namespace)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative, old, _new in namespace["EDITS"]:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open("a", encoding="utf-8") as stream:
                    stream.write(old + "\n")
            command = [sys.executable, str(SCRIPT), str(root)]
            subprocess.run(command, check=True, capture_output=True, text=True)
            first = {p: p.read_bytes() for p in root.rglob("*.c")}
            subprocess.run(command, check=True, capture_output=True, text=True)
            self.assertEqual(first, {p: p.read_bytes() for p in root.rglob("*.c")})
            halofit = (root / "external" / "Halofit" / "halofit.c").read_text()
            self.assertIn("fnu = pba->Omega0_ncdm_tot/Omega_m;", halofit)
            self.assertNotIn("fnu = pba->Omega0_ncdm_tot/pba->Omega0_m;", halofit)
            for relative, _old, new in namespace["EDITS"]:
                self.assertIn(new, (root / relative).read_text())


if __name__ == "__main__":
    unittest.main()

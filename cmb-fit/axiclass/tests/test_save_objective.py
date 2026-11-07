import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


RUNNER = Path(__file__).resolve().parents[1] / "early_late_spa.py"


class SaveTests(unittest.TestCase):
    def test_each_objective_reads_its_own_collection(self):
        spec = importlib.util.spec_from_file_location("save_test_runner", RUNNER)
        runner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(runner)
        with tempfile.TemporaryDirectory() as directory:
            runner.OUT = directory
            chains = Path(directory) / "chains"
            chains.mkdir()
            for ignore_prior, extension, chi2 in ((False, "minimum", 42), (True, "bestfit", 39)):
                (chains / f"cmp_control.{extension}.txt").write_text(
                    f"# chi2 omega_b omega_cdm H0 Omega_m\n{chi2} 0.0225 0.118 68 3.08\n"
                )
                runner.save("control", ignore_prior=ignore_prior)
                result = json.loads((Path(directory) / "cmp_control.json").read_text())
                self.assertEqual(result["minimum"]["chi2"], chi2)
                self.assertEqual(result["minimum"]["Omega_m_class_reported"], 3.08)
                self.assertLess(result["minimum"]["Omega_m"], 1)


if __name__ == "__main__":
    unittest.main()

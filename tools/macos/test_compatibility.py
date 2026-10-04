"""Portable launcher tests and real compilation of the patched Poisson APIs."""
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("native_mm3d", HERE / "native_mm3d.py")
launcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(launcher)


class CompatibilityTests(unittest.TestCase):
    def test_native_defaults_and_explicit_overrides_paths_are_literal(self):
        argv = launcher.command(["Tapioca", "All", "images with spaces/.*png", "640"], Path("/path with spaces/source"))
        self.assertEqual(argv[-2:], ["Detect=mm3d:Digeo", "Match=mm3d:Ann"])
        self.assertEqual(argv[0], "/path with spaces/source/bin/mm3d")
        custom = ["Tapioca", "All", ".*png", "640", "Detect=other", "Match=other"]
        self.assertEqual(launcher.command(custom)[1:], custom)

    def test_non_tapioca_commands_unchanged(self):
        for args in (["Tapas", "RadialBasic", ".*png"], ["Malt", "-help"], []):
            self.assertEqual(launcher.command(args)[1:], list(args))

    def test_patched_poisson_apis_compile_and_execute(self):
        compiler = os.environ.get("CXX", "c++")
        if not shutil.which(compiler):
            self.skipTest("C++ compiler is required for native API regression")
        with tempfile.TemporaryDirectory() as temporary:
            binary = Path(temporary) / "compatibility"
            subprocess.run([compiler, "-std=c++11", "-Wno-unknown-pragmas", "-I", str(HERE.parents[1] / "CodeExterne/Poisson/include"), str(HERE / "compatibility_smoke.cpp"), "-o", str(binary)], check=True, timeout=60)
            subprocess.run([str(binary)], check=True, timeout=10)


if __name__ == "__main__":
    unittest.main()

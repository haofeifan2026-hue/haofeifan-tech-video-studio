from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "compose_vertical_still.py"


class ComposeVerticalStillTest(unittest.TestCase):
    def test_preserves_source_and_creates_requested_canvas(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            source = temp / "source.png"
            output = temp / "output.jpg"
            Image.new("RGB", (320, 180), (32, 120, 180)).save(source)
            source_before = source.read_bytes()

            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(source),
                    str(output),
                    "--width",
                    "360",
                    "--height",
                    "640",
                    "--box",
                    "30,70,330,500",
                    "--blur",
                    "8",
                    "--radius",
                    "10",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertEqual(source.read_bytes(), source_before)
            self.assertTrue(output.is_file())
            with Image.open(output) as result:
                self.assertEqual(result.size, (360, 640))
                self.assertEqual(result.mode, "RGB")


if __name__ == "__main__":
    unittest.main()

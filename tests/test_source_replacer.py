import tempfile
import unittest
from pathlib import Path

from optimizer.source_replacer import replace_function, restore_source


class SourceReplacerTests(unittest.TestCase):
    def test_replaces_only_named_function_and_can_restore(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "target.py"
            original = "def first():\n    return 1\n\n\ndef second():\n    return 2\n"
            path.write_text(original)
            old_source = replace_function(path, "first", "def first():\n    return 10")
            self.assertIn("return 10", path.read_text())
            self.assertIn("def second():", path.read_text())
            restore_source(path, old_source)
            self.assertEqual(path.read_text(), original)

    def test_rejects_wrong_function(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "target.py"
            path.write_text("def first():\n    return 1\n")
            with self.assertRaises(ValueError):
                replace_function(path, "first", "def wrong():\n    return 2")


if __name__ == "__main__":
    unittest.main()

import unittest

from functions.common_items import find_common_items
from functions.duplicates import find_duplicates
from functions.sentence import create_sentence


class FunctionTests(unittest.TestCase):
    def test_duplicates(self):
        self.assertEqual(find_duplicates([]), [])
        self.assertEqual(find_duplicates([1, 2, 2, 3, 3]), [2, 3])
        self.assertEqual(find_duplicates([3, 3, 3]), [3])

    def test_duplicates_supports_unhashable_values(self):
        self.assertEqual(find_duplicates([[1], [2], [1]]), [[1]])

    def test_common_items_preserves_order_and_duplicates(self):
        self.assertEqual(find_common_items([3, 1, 1, 2], [1, 3]), [3, 1, 1])

    def test_sentence(self):
        self.assertEqual(create_sentence([]), "")
        self.assertEqual(create_sentence(["hello", "world"]), "hello world")


if __name__ == "__main__":
    unittest.main()

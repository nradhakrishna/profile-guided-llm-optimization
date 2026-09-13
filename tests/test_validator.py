import unittest

from optimizer.validator import validate_optimization


class ValidatorTests(unittest.TestCase):
    def test_rejects_candidate_that_raises_for_supported_input(self):
        def original(values):
            return list(values)

        def candidate(values):
            return list(set(values))

        self.assertFalse(
            validate_optimization(original, candidate, [[[1], [1]]])
        )


if __name__ == "__main__":
    unittest.main()

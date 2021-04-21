import unittest
from QuestionB import compare_versions


class TestQuestionB(unittest.TestCase):

    def test_greater_than(self):
        self.assertEqual(compare_versions("1.4.3", "1.4.2"), 1)

    def test_less_than(self):
        self.assertEqual(compare_versions("5.4", "6.2.1"), -1)

    def test_equal(self):
        self.assertEqual(compare_versions("4.5.5", "4.5.5"), 0)
        # Check that additional 0's at the end don't affect the result
        self.assertEqual(compare_versions("1.1.0", "1.1"), 0)

    def test_invalid_version_letters(self):
        self.assertRaises(ValueError, lambda: compare_versions("v1", "v2"))

    def test_invalid_version_negative(self):
        self.assertRaises(
            ValueError, lambda: compare_versions("1.-1.2", "1.5.4"))


if __name__ == '__main__':
    unittest.main()

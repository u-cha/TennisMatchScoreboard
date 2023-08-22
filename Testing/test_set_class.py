import unittest

from Set import Set


class TestSetClass(unittest.TestCase):

    def test_is_over(self, expected_result=True):
        test_cases = [
            (6, 0, expected_result),
            (0, 6, expected_result),
            (7, 0, expected_result),
            (3, 6, expected_result),
            (7, 6, True),
            (5, 4, False),
            (0, 0, False)
        ]
        for p1, p2, expected_result in test_cases:
            set_ = Set()
            with self.subTest(p1=p1, p2=p2, expected_result=expected_result):

                while p1 and p2:
                    set_.add_point(1)
                    p1 -= 1
                    set_.add_point(2)
                    p2 -= 1
                while p1:
                    set_.add_point(1)
                    p1 -= 1
                while p2:
                    set_.add_point(2)
                    p2 -= 1
                self.assertEqual(set_.is_over, expected_result)

    def test_needs_tie(self, expected_result=True):
        test_cases = [
            (6, 6, expected_result),
            (7, 6, expected_result),
            (6, 7, expected_result),
            (7, 7, expected_result),
            (7, 8, expected_result),
            (5, 5, False)

        ]
        for p1, p2, expected_result in test_cases:
            set_ = Set()
            with self.subTest(p1=p1, p2=p2, expected_result=expected_result):
                while p1 and p2:
                    set_.add_point(1)
                    p1 -= 1
                    set_.add_point(2)
                    p2 -= 1
                while p1:
                    set_.add_point(1)
                    p1 -= 1
                while p2:
                    set_.add_point(2)
                    p2 -= 1

                self.assertEqual(set_.needs_tie, expected_result)


if __name__ == "__main__":
    unittest.main(verbosity=2)

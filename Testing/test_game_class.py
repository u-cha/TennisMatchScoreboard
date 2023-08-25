import unittest

from Scores.Score import Game


class TestGameClass(unittest.TestCase):

    def test_winning_cases_not_tie(self, expected_result=True):
        test_cases = [
            (4, 0, expected_result),
            (0, 4, expected_result),
            (2, 10, expected_result),
            (2, 4, expected_result)
        ]
        for p1, p2, expected_result in test_cases:
            game = Game(is_tie=False)
            with self.subTest(p1=p1, p2=p2, expected_result=expected_result):

                for _ in range(p1):
                    game.add_point(1)
                for _ in range(p2):
                    game.add_point(2)
                self.assertEqual(game.is_over, expected_result)

    def test_winning_cases_tie(self, expected_result=True):
        test_cases = [
            (7, 0, expected_result),
            (0, 7, expected_result),
            (2, 7, expected_result),
            (5, 7, expected_result)
        ]
        for p1, p2, expected_result in test_cases:
            game = Game(is_tie=True)
            with self.subTest(p1=p1, p2=p2, expected_result=expected_result):
                for _ in range(p1):
                    game.add_point(1)
                for _ in range(p2):
                    game.add_point(2)
                self.assertEqual(game.is_over, expected_result)

    def test_not_winning_cases_not_tie(self, expected_result=False):
        test_cases = [
            (0, 0, expected_result),
            (2, 1, expected_result)
        ]
        for p1, p2, expected_result in test_cases:
            game = Game(is_tie=False)
            with self.subTest(p1=p1, p2=p2, expected_result=expected_result):
                for _ in range(p1):
                    game.add_point(1)
                for _ in range(p2):
                    game.add_point(2)
                self.assertEqual(game.is_over, expected_result)

    def test_special_cases_not_tie(self, expected_result=False):
        test_cases = [
            (4, 4, expected_result),
            (5, 5, expected_result),
            (6, 5, expected_result)
        ]
        for p1, p2, expected_result in test_cases:
            game = Game(is_tie=False)
            with self.subTest(p1=p1, p2=p2, expected_result=expected_result):
                while p1 and p2:

                    game.add_point(1)
                    p1 -= 1
                    game.add_point(2)
                    p2 -= 1
                while p1:
                    game.add_point(1)
                    p1 -= 1
                while p2:
                    game.add_point(2)
                    p2 -= 1
                self.assertEqual(game.is_over, expected_result)

    def test_special_cases_tie(self, expected_result=False):
        test_cases = [
            (7, 7, expected_result),
            (6, 7, expected_result),
            (7, 8, expected_result)
        ]
        for p1, p2, expected_result in test_cases:
            game = Game(is_tie=True)
            with self.subTest(p1=p1, p2=p2, expected_result=expected_result):

                while p1 and p2:
                    game.add_point(1)
                    p1 -= 1
                    game.add_point(2)
                    p2 -= 1
                while p1:
                    game.add_point(1)
                    p1 -= 1
                while p2:
                    game.add_point(2)
                    p2 -= 1
                self.assertEqual(game.is_over, expected_result)


if __name__ == "__main__":
    unittest.main(verbosity=2)

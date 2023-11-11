import unittest
from unittest.mock import patch
from game import Game

class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_initialization(self):
        self.assertEqual(len(self.game.number), 4)
        self.assertEqual(self.game.number_length, 4)
        self.assertEqual(self.game.attempts, 10)
        self.assertEqual(self.game.guesses, [])
        # self.assertEqual(self.game.feedback, [])
        self.assertEqual(self.game.player_won, [])

    def test_process_guess_correct_feedback(self):
        self.game.number = [1, 2, 3, 4]
        feedback = self.game.process_guess([1, 5, 3, 4])
        self.assertEqual(feedback, "3 right numbers, 3 in the right location")

    def test_guess1(self):
        self.game.number = [1, 2, 3, 4]
        feedback = self.game.process_guess([5, 6, 7, 8])
        self.assertEqual(feedback, "0 right numbers, 0 in the right location")

    def test_guess2(self):
        self.game.number = [0, 1, 3, 5]
        feedback = self.game.process_guess([0, 2, 4, 6])
        self.assertEqual(feedback, "1 right numbers, 1 in the right location")

    def test_guess3(self):
        self.game.number = [0, 1, 3, 5]
        feedback = self.game.process_guess([0, 1, 5, 6])
        self.assertEqual(feedback, "3 right numbers, 2 in the right location")



if __name__ == '__main__':
    unittest.main()
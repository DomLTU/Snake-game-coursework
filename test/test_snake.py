import unittest
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.entities import Snake, Food, FoodFactory
from core.game import SnakeGame
from data.highscore import ScoreManager

class TestSnakeGame(unittest.TestCase):
    def setUp(self):
        self.snake = Snake((15, 12))
        
        # Reset ScoreManager state for clean testing
        ScoreManager._instance = None
        self.score_manager = ScoreManager()

    def test_snake_initial_size(self):
        """Test if the snake initializes with length 3."""
        self.assertEqual(len(self.snake.get_positions()), 3)

    def test_snake_movement(self):
        """Test snake movement logic (without growth)."""
        initial_head = self.snake.head
        self.snake.move(1, 0, grow=False)  # Move right
        self.assertEqual(self.snake.head, (initial_head[0] + 1, initial_head[1]))
        self.assertEqual(len(self.snake.get_positions()), 3)

    def test_snake_growth(self):
        """Test snake growth logic when eating food."""
        self.snake.move(1, 0, grow=True)  # Move right and grow
        self.assertEqual(len(self.snake.get_positions()), 4)

    def test_score_manager_singleton(self):
        """Test if the ScoreManager properly implements the Singleton pattern."""
        sm1 = ScoreManager()
        sm2 = ScoreManager()
        self.assertIs(sm1, sm2, "ScoreManager instances are not the same (Singleton failed)")

    def test_file_io_high_score(self):
        """Test reading and writing high score to the JSON file."""
        # Set a high score higher than any existing score
        self.score_manager.high_score = 9999
        self.assertEqual(self.score_manager.high_score, 9999)
        
        # Verify file creation and contents in cache folder
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(__file__), "..", "resources", "cache", "highscore.json")))
        
        # Create a new instance to test loading
        ScoreManager._instance = None
        new_sm = ScoreManager()
        self.assertEqual(new_sm.high_score, 9999)

if __name__ == '__main__':
    unittest.main()

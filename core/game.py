from .constants import COLS, ROWS, DIRS, OPPOSITE
from .entities import Snake, FoodFactory
from data.highscore import ScoreManager


class SnakeGame:
    """
    Manages game state using Composition/Aggregation.
    Has-a Snake, has-a Food, has-a ScoreManager.
    """

    def __init__(self):
        self.score_manager = ScoreManager()
        self.reset()

    def reset(self):
        self.snake = Snake((COLS // 2, ROWS // 2))
        self.food = FoodFactory.spawn_food(self.snake.get_positions())
        self.next_dir = "Right"
        self.score = 0
        self.alive = True
        self.grew = False

    def set_direction(self, d):
        if d != OPPOSITE.get(self.snake.direction):
            self.next_dir = d

    def step(self):
        if not self.alive:
            return

        self.snake.direction = self.next_dir
        dx, dy = DIRS[self.snake.direction]
        hx, hy = self.snake.head
        new_head = (hx + dx, hy + dy)

        # Wall collision
        if not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS):
            self.alive = False
            return

        # Self collision
        if new_head in self.snake.get_positions()[:-1]:
            self.alive = False
            return

        # Check if eating food
        self.grew = new_head == self.food.position

        # Move snake
        self.snake.move(dx, dy, self.grew)

        if self.grew:
            self.score += 10
            self.score_manager.high_score = self.score
            self.food = FoodFactory.spawn_food(self.snake.get_positions())

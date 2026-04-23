import random
from abc import ABC, abstractmethod

from .constants import COLS, ROWS, DIRS


# ── OOP Pillar: Abstraction & Inheritance ──────────────────────────────────────
class GameObject(ABC):
    """Abstract base class for all game entities."""

    @abstractmethod
    def get_positions(self):
        """Must be implemented by subclasses to return list of coordinates."""
        pass


class Food(GameObject):
    """Represents the food entity. Inherits from GameObject."""

    def __init__(self, x, y):
        # Encapsulation: Private coordinates
        self.__x = x
        self.__y = y

    @property
    def position(self):
        return self.__x, self.__y

    # Polymorphism: Overriding abstract method
    def get_positions(self):
        return [(self.__x, self.__y)]


class FoodFactory:
    """Factory to handle the logic of spawning food in valid locations."""

    @staticmethod
    def spawn_food(occupied_positions):
        while True:
            x = random.randint(0, COLS - 1)
            y = random.randint(0, ROWS - 1)
            if (x, y) not in occupied_positions:
                return Food(x, y)


class Snake(GameObject):
    """Represents the snake entity. Inherits from GameObject."""

    def __init__(self, start_pos):
        # Encapsulation: Private internal state
        cx, cy = start_pos
        self.__body = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.__direction = "Right"

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, d):
        self.__direction = d

    @property
    def head(self):
        return self.__body[0]

    # Polymorphism: Overriding abstract method
    def get_positions(self):
        return self.__body

    def move(self, dx, dy, grow):
        hx, hy = self.head
        new_head = (hx + dx, hy + dy)
        self.__body.insert(0, new_head)
        if not grow:
            self.__body.pop()

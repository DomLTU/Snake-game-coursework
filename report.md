# OOP Coursework Report: Classic Snake Game

## 1. Introduction

**What is this application?**
This project is an object-oriented implementation of the classic arcade game "Snake". The application is built using Python's built-in `tkinter` library for the graphical user interface. The primary goal of this project was to take a functional, procedural game script and completely refactor it to strictly adhere to Object-Oriented Programming (OOP) principles, design patterns, and best practices.

**How to run the program?**
1. Ensure you have Python 3.x installed on your system.
2. Clone or download the repository.
3. Open your terminal or command prompt, navigate to the project directory, and run:
```bash
    python snake_game.py
```
4. To run the unit tests, execute:
```bash
    python test_snake.py
```

**How to use the program?**
Once the application launches, you will be greeted by the main menu.

Start/Play: Press ENTER.
Controls: Use the Arrow Keys or W, A, S, D to change the snake's direction.
Pause: Press P to pause or resume the game.
Restart: Press R after a game over to restart.
Quit: Press Q to exit the application.

Objective: Eat the red food to grow your snake and increase your score. Avoid colliding with the walls or your own tail.

## 2. Body / Analysis
This section explains how the program implements the required functional requirements and OOP principles.

## The 4 OOP Pillars

**1. Encapsulation**
Encapsulation is the bundling of data and the methods that operate on that data into a single unit, while restricting direct access to some of the object's components. In this project, internal states are hidden using private attributes (denoted by a double underscore __).

Usage in Code: In the Snake and Food classes, the coordinates and body segments are kept private. They are only accessible via @property getters and setters to ensure the state cannot be arbitrarily corrupted from outside the class.

```bash
Python
class Food(GameObject):
    def __init__(self, x, y):
        # Private attributes
        self.__x = x
        self.__y = y

    @property
    def position(self):
        return self.__x, self.__y
```

**2. Abstraction**
Abstraction involves hiding complex implementation details and showing only the essential features of the object.

Usage in Code: I created an abstract base class GameObject using Python's abc module. This enforces a contract that any game entity must implement the get_positions() method, hiding the specific logic of how a snake or food piece stores its location.

```bash
Python
class GameObject(ABC):
    @abstractmethod
    def get_positions(self):
        pass
```

**3. Inheritance**
Inheritance allows a class (child) to acquire the properties and methods of another class (parent), promoting code reusability.

Usage in Code: Both the Snake and Food classes inherit from the abstract GameObject class. This establishes an "is-a" relationship, meaning a Snake is a GameObject.

```bash
Python
class Snake(GameObject):
    # Inherits from GameObject and must implement its abstract methods
    def __init__(self, start_pos):
        # ...
```

**4. Polymorphism**
Polymorphism allows objects of different classes to be treated as objects of a common superclass, specifically by allowing methods to do different things based on the object calling them.

Usage in Code: The get_positions() method behaves differently depending on the object. For Food, it returns a single coordinate pair. For Snake, it overrides the method to return a list of all body segment coordinates.

```bash
Python
# In Food class:
def get_positions(self):
    return [(self.__x, self.__y)]

# In Snake class:
def get_positions(self):
    return self.__body
```

**Design Patterns**
To ensure a robust architecture, the following design patterns were implemented:

**Singleton Pattern:**
The ScoreManager is implemented as a Singleton. This ensures that there is only one central point responsible for managing the high score and file I/O operations. Since multiple instances trying to read/write to the same file simultaneously could cause data corruption or crashes, the Singleton provides a safe, globally accessible state manager.

```bash
Python
class ScoreManager:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ScoreManager, cls).__new__(cls)
        return cls._instance
```

**Factory Method Pattern:**
The FoodFactory handles the complex logic of randomly spawning food in valid locations (ensuring it doesn't spawn inside the snake's body). This separates object creation from the core game loop.

**Composition and Aggregation**
Composition is a "has-a" relationship where complex objects are built from smaller, simpler objects.

Usage in Code: The SnakeGame class relies heavily on composition. Rather than inheriting from a Snake or Food class, it instantiates them as attributes. SnakeGame manages a Snake object, a Food object, and a ScoreManager. If the SnakeGame is destroyed, the specific instances of the current game's Snake and Food are also destroyed.

```bash
Python
class SnakeGame:
    def reset(self):
        # Composition: The game consists of these components
        self.snake = Snake((COLS // 2, ROWS // 2))
        self.food = FoodFactory.spawn_food(self.snake.get_positions())
```

**File I/O**
The game persistently saves the user's high score. The ScoreManager uses Python's built-in json and os modules to check for, read, and write to a highscore.json file. This ensures the player's progress is saved between sessions.

## 3. Results and Summary
Results: The program successfully fulfills all functional requirements. The core mechanics (movement, growth, collision, scoring) work flawlessly, and the codebase is now highly modular, readable, and strictly follows PEP8 code styling rules.

Challenges: A primary challenge was adapting tkinter's .after() loop—which is highly procedural—into an Object-Oriented environment without creating tightly coupled classes. This was solved by clearly separating the GUI logic (SnakeApp) from the pure game state logic (SnakeGame). Additionally, writing unit tests for a Singleton required careful manual resetting of the _instance variable between tests to avoid state leakage.

Extensibility: The OOP architecture makes this game highly extensible. Because of the Factory pattern, adding new types of food (e.g., "Poison" that shrinks the snake, or "Golden Apples" worth double points) would be trivial. The GameObject abstraction also paves the way to easily introduce obstacles or moving enemies.

## 4. Conclusions
This coursework successfully demonstrates the transition from procedural scripting to a structured Object-Oriented paradigm. By implementing all four pillars of OOP, utilizing Singleton and Factory design patterns, and applying composition, the resulting software is vastly more maintainable and robust. Core functionalities were successfully verified using the unittest framework.

In the future, the prospects for this application could include migrating the backend logic to a more advanced graphics library like Pygame, introducing multiplayer network support, or integrating a database instead of a JSON file for global leaderboards.
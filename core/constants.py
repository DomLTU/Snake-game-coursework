CELL = 20
COLS = 30
ROWS = 25
W = COLS * CELL
H = ROWS * CELL

SPEEDS = {"Slow": 180, "Normal": 110, "Fast": 60}

COLORS = {
    "bg": "#1a1a2e",
    "grid": "#16213e",
    "snake_head": "#00d4aa",
    "snake_body": "#00a878",
    "snake_eye": "#1a1a2e",
    "food": "#ff6b6b",
    "food_glow": "#ff4757",
    "score_bg": "#16213e",
    "text": "#e0e0e0",
    "accent": "#00d4aa",
    "god_glow": "#ffcc00",
    "danger": "#ff6b6b",
    "border": "#0f3460",

}

DIRS = {
    "Up": (0, -1),
    "Down": (0, 1),
    "Left": (-1, 0),
    "Right": (1, 0),
}
OPPOSITE = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}

import tkinter as tk

from core.constants import CELL, W, H, COLS, ROWS, SPEEDS, COLORS
from core.game import SnakeGame


class SnakeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Snake OOP")
        self.resizable(False, False)
        self.configure(bg=COLORS["bg"])

        self.speed_var = tk.StringVar(value="Normal")
        self.game = SnakeGame()
        self._after_id = None
        self._paused = False
        self._state = "menu"

        self._build_ui()
        self._bind_keys()
        self._show_menu()

    # ── UI Construction ────────────────────────────────────────────────────────

    def _build_ui(self):
        top = tk.Frame(self, bg=COLORS["score_bg"], pady=6)
        top.pack(fill="x")

        tk.Label(top, text="🐍³ PYTHON PYTHON PYTHON", font=("Courier", 16, "bold"),
                 bg=COLORS["score_bg"], fg=COLORS["accent"]).pack(side="left", padx=14)

        right_frame = tk.Frame(top, bg=COLORS["score_bg"])
        right_frame.pack(side="right", padx=14)

        tk.Label(right_frame, text="SPEED", font=("Courier", 9),
                 bg=COLORS["score_bg"], fg=COLORS["text"]).grid(row=0, column=0, padx=(0, 4))

        for idx, s in enumerate(SPEEDS):
            tk.Radiobutton(right_frame, text=s, variable=self.speed_var, value=s,
                           font=("Courier", 9), bg=COLORS["score_bg"],
                           fg=COLORS["text"], selectcolor=COLORS["border"],
                           activebackground=COLORS["score_bg"],
                           activeforeground=COLORS["accent"]).grid(row=0, column=idx + 1)

        score_frame = tk.Frame(top, bg=COLORS["score_bg"])
        score_frame.pack(side="left", expand=True)

        self.score_lbl = tk.Label(score_frame, text="SCORE  0",
                                  font=("Courier", 13, "bold"),
                                  bg=COLORS["score_bg"], fg=COLORS["accent"])
        self.score_lbl.pack(side="left", padx=18)

        self.hi_lbl = tk.Label(score_frame, text=f"BEST  {self.game.score_manager.high_score}",
                               font=("Courier", 13, "bold"),
                               bg=COLORS["score_bg"], fg=COLORS["text"])
        self.hi_lbl.pack(side="left", padx=18)

        canvas_frame = tk.Frame(self, bg=COLORS["border"], padx=2, pady=2)
        canvas_frame.pack()
        self.canvas = tk.Canvas(canvas_frame, width=W, height=H,
                                bg=COLORS["bg"], highlightthickness=0)
        self.canvas.pack()

        bottom = tk.Frame(self, bg=COLORS["score_bg"], pady=4)
        bottom.pack(fill="x")
        self.hint_lbl = tk.Label(bottom,
                                 text="ENTER – start   P – pause   R – restart   Q – quit",
                                 font=("Courier", 9), bg=COLORS["score_bg"], fg=COLORS["text"])
        self.hint_lbl.pack()

    def _bind_keys(self):
        for key, d in [("<Up>", "Up"), ("<Down>", "Down"), ("<Left>", "Left"), ("<Right>", "Right"),
                       ("w", "Up"), ("s", "Down"), ("a", "Left"), ("d", "Right")]:
            self.bind(key, lambda _e, d=d: self._on_dir(d))
        self.bind("<Return>", lambda _e: self._on_enter())
        self.bind("p", lambda _e: self._toggle_pause())
        self.bind("P", lambda _e: self._toggle_pause())
        self.bind("r", lambda _e: self._restart())
        self.bind("R", lambda _e: self._restart())
        self.bind("q", lambda _e: self.quit())
        self.bind("Q", lambda _e: self.quit())

    # ── State Transitions ──────────────────────────────────────────────────────

    def _show_menu(self):
        self._state = "menu"
        self._cancel_loop()
        self._draw_grid()
        body = "Use arrow keys or WASD\nto control the snake.\n\nEat food to grow!"
        footer = ("Press ENTER to Play")
        self._overlay("SNAKE", body, footer)

    def _on_enter(self):
        if self._state in ("menu", "game_over"):
            self._start_game()
        elif self._state == "paused":
            self._toggle_pause()

    def _start_game(self):
        self.game.reset()
        self._paused = False
        self._state = "playing"
        self._update_scoreboard()
        self._loop()

    def _restart(self):
        self._cancel_loop()
        self._start_game()

    def _toggle_pause(self):
        if self._state not in ("playing", "paused"):
            return
        self._paused = not self._paused
        if self._paused:
            self._state = "paused"
            self._cancel_loop()
            self._overlay("PAUSED", "", "Press P or ENTER to resume")
        else:
            self._state = "playing"
            self._loop()

    def _game_over(self):
        self._state = "game_over"
        self._cancel_loop()
        msg = f"Score: {self.game.score}"
        self._overlay("GAME OVER", msg, "Press ENTER or R to restart")

    # ── Game Loop ──────────────────────────────────────────────────────────────

    def _loop(self):
        self.game.step()
        self._draw()
        self._update_scoreboard()
        if not self.game.alive:
            self._game_over()
            return
        delay = SPEEDS[self.speed_var.get()]
        self._after_id = self.after(delay, self._loop)

    def _cancel_loop(self):
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None

    def _on_dir(self, d):
        if self._state == "playing":
            self.game.set_direction(d)

    # ── Drawing ────────────────────────────────────────────────────────────────

    def _draw_grid(self):
        self.canvas.delete("all")
        for c in range(0, W, CELL):
            self.canvas.create_line(c, 0, c, H, fill=COLORS["grid"], width=1)
        for r in range(0, H, CELL):
            self.canvas.create_line(0, r, W, r, fill=COLORS["grid"], width=1)

    def _draw(self):
        self._draw_grid()
        g = self.game

        # Draw Food
        fx, fy = g.food.position
        x1, y1 = fx * CELL, fy * CELL
        x2, y2 = x1 + CELL, y1 + CELL
        self.canvas.create_oval(x1 - 2, y1 - 2, x2 + 2, y2 + 2,
                                fill=COLORS["food_glow"], outline="", tags="food")
        self.canvas.create_oval(x1 + 2, y1 + 2, x2 - 2, y2 - 2,
                                fill=COLORS["food"], outline="", tags="food")

        # Draw Snake
        for i, (sx, sy) in enumerate(g.snake.get_positions()):
            x1, y1 = sx * CELL + 1, sy * CELL + 1
            x2, y2 = x1 + CELL - 2, y1 + CELL - 2
            color = COLORS["snake_head"] if i == 0 else COLORS["snake_body"]
            r = 6 if i == 0 else 4
            self._rounded_rect(x1, y1, x2, y2, r, color)

        # Draw Eyes
        self._draw_eyes(g.snake.head, g.snake.direction)

    def _rounded_rect(self, x1, y1, x2, y2, r, color):
        self.canvas.create_polygon(
            x1 + r, y1, x2 - r, y1,
            x2, y1, x2, y1 + r,
            x2, y2 - r, x2, y2,
            x2 - r, y2, x1 + r, y2,
            x1, y2, x1, y2 - r,
            x1, y1 + r, x1, y1,
            smooth=True, fill=color, outline=""
        )

    def _draw_eyes(self, head, direction):
        hx, hy = head
        cx = hx * CELL + CELL // 2
        cy = hy * CELL + CELL // 2
        offset = 4
        if direction in ("Right", "Left"):
            ex = cx + (4 if direction == "Right" else -4)
            e1 = (ex, cy - offset)
            e2 = (ex, cy + offset)
        else:
            ey = cy + (4 if direction == "Down" else -4)
            e1 = (cx - offset, ey)
            e2 = (cx + offset, ey)
        for ex, ey in (e1, e2):
            self.canvas.create_oval(ex - 2, ey - 2, ex + 2, ey + 2,
                                    fill=COLORS["snake_eye"], outline="")

    def _overlay(self, title, body, footer):
        ow, oh = 380, 240
        ox = (W - ow) // 2
        oy = (H - oh) // 2
        self.canvas.create_rectangle(ox + 6, oy + 6, ox + ow + 6, oy + oh + 6,
                                     fill="#000000", outline="", stipple="gray50")
        self.canvas.create_rectangle(ox, oy, ox + ow, oy + oh,
                                     fill=COLORS["score_bg"], outline=COLORS["accent"], width=2)
        self.canvas.create_text(ox + ow // 2, oy + 48,
                                text=title, font=("Courier", 26, "bold"),
                                fill=COLORS["accent"])
        if body:
            self.canvas.create_text(ox + ow // 2, oy + 130,
                                    text=body, font=("Courier", 11),
                                    fill=COLORS["text"], justify="center")
        self.canvas.create_text(ox + ow // 2, oy + oh - 22,
                                text=footer, font=("Courier", 10),
                                fill=COLORS["danger"])

    def _update_scoreboard(self):
        self.score_lbl.config(text=f"SCORE  {self.game.score}")
        self.hi_lbl.config(text=f"BEST  {self.game.score_manager.high_score}")

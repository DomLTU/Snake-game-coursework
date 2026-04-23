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
        
        # Cheat code attributes
        self._godmode = False
        self._cheat_buffer = ""
        self._purple_snake = False
        self._quit_confirm = False
        self._prev_state = None

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
        # Use a single generic key handler to avoid duplicate event processing in cheat mode.
        self.bind("<Key>", self._on_key_press)

    # ── State Transitions ──────────────────────────────────────────────────────

    def _show_menu(self):
        self._state = "menu"
        self._cancel_loop()
        self._draw_grid()
        body = "Use arrow keys or WASD\nto control the snake.\n\nEat food to grow!"
        footer = ("Press ENTER to Play")
        self._overlay("SNAKE", body, footer)

    def _on_enter(self):
        if self._state == "cheat_mode":
            self._process_cheat_key("Return")
            return "break"
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
        if self._state == "cheat_mode":
            self._process_cheat_key("r")
            return "break"
        self._cancel_loop()
        self._start_game()

    def _toggle_pause(self):
        if self._state == "cheat_mode":
            self._process_cheat_key("p")
            return "break"
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

    def _enter_cheat_mode(self):
        if self._state not in ("playing", "paused"):
            return
        self._prev_state = self._state
        self._state = "cheat_mode"
        self._cancel_loop()
        self._cheat_buffer = ""
        self._overlay("CHEAT MODE", "Enter cheat code using arrows/WASD + letters:", "Press ESC to cancel")

    def _process_cheat_key(self, key):
        if self._state != "cheat_mode":
            return
        
        if key == "Escape":
            self._exit_cheat_mode()
            return

        # Handle arrow keys as directions
        if key in ("Up", "Down", "Left", "Right"):
            cheat_key = key.lower()
        # Handle WASD as LETTERS, not directions (preserve 'd', 'a', 's', 'w' for cheat codes)
        elif key.lower() in ("w", "a", "s", "d", "i", "q", "k", "f", "b"):
            cheat_key = key.lower()
        elif len(key) == 1 and key.isalpha():
            # Any other letter
            cheat_key = key.lower()
        elif key == "Return":
            cheat_key = "return"
        else:
            return

        self._cheat_buffer += cheat_key

        # 3. Check for successful codes
        if "iddqd" in self._cheat_buffer:
            self._activate_godmode()
            return
        if "idkfa" in self._cheat_buffer:
            self._fill_map_with_apples()
            return
        if "upupdowndownleftrightleftrightab" in self._cheat_buffer:
            self._purple_snake_cheat() # Renamed to avoid collision with the bool attribute
            return

        # Update UI feedback
        masked = "*" * len(self._cheat_buffer)
        self._overlay("CHEAT MODE", f"Code: {masked}", "Press ESC to cancel")

    def _activate_godmode(self):
        self._godmode = True
        self._overlay("CHEAT ACTIVATED", "GODMODE ENABLED", "Resuming in 1 second...")
        self.after(1000, self._exit_cheat_mode)

    def _fill_map_with_apples(self):
        occupied = set(self.game.snake.get_positions())
        for food in self.game.foods:
            occupied.add(food.position)
        
        from core.entities import FoodFactory
        for _ in range(20):  # Spawn 20 apples
            food = FoodFactory.spawn_food(occupied)
            self.game.foods.append(food)
            occupied.add(food.position)
        self._overlay("CHEAT ACTIVATED", "MAP FILLED WITH APPLES", "Resuming in 1 second...")
        self.after(1000, self._exit_cheat_mode)

    def _purple_snake_cheat(self):
        self._purple_snake = True # This sets the boolean flag
        self._overlay("CHEAT ACTIVATED", "SNAKE IS NOW PURPLE", "Resuming in 1 second...")
        self.after(1000, self._exit_cheat_mode)

    def _exit_cheat_mode(self):
        if self._prev_state == "paused":
            self._state = "paused"
            self._overlay("PAUSED", "", "Press P or ENTER to resume")
        else:
            self._state = "playing"
            self._loop()
        self._prev_state = None

    # ── Game Loop ──────────────────────────────────────────────────────────────

    def _loop(self):
        self.game.step(invincible=self._godmode)
        self._draw()
        self._update_scoreboard()
        if not self.game.alive and not self._godmode:
            self._game_over()
            return
        delay = SPEEDS[self.speed_var.get()]
        self._after_id = self.after(delay, self._loop)

    def _cancel_loop(self):
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None

    def _on_dir(self, d):
        if self._state == "cheat_mode":
            self._process_cheat_key(d)
            return "break"
        if self._state == "playing":
            self.game.set_direction(d)

    def _on_key_press(self, event):
        if self._state == "cheat_mode":
            self._process_cheat_key(event.keysym)
            return "break"
        
        key = event.keysym
        if key in ("Up", "Down", "Left", "Right"):
            self._on_dir(key)
            return "break"
        if key.lower() == "w":
            self._on_dir("Up")
            return "break"
        if key.lower() == "s":
            self._on_dir("Down")
            return "break"
        if key.lower() == "a":
            self._on_dir("Left")
            return "break"
        if key.lower() == "d":
            self._on_dir("Right")
            return "break"
        if key == "Return":
            self._on_enter()
            return "break"
        if key.lower() == "p":
            self._toggle_pause()
            return "break"
        if key.lower() == "r":
            self._restart()
            return "break"
        if key.lower() == "q":
            self._handle_quit()
            return "break"
        if key.lower() == "x":
            self._enter_cheat_mode()
            return "break"

    def _handle_quit(self):
        if self._state == "cheat_mode":
            self._process_cheat_key("q")
            return "break"
        if self._quit_confirm:
            self.quit()
        else:
            self._quit_confirm = True
            self.hint_lbl.config(text="Press Q again to confirm quit")
            self.after(2000, lambda: self._reset_quit_confirm())  # Reset after 2 seconds

    def _reset_quit_confirm(self):
        self._quit_confirm = False
        self.hint_lbl.config(text="ENTER – start   P – pause   R – restart   Q – quit")

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
        snake_pos = g.snake.get_positions()

        # Draw Food
        for food in g.foods:
            fx, fy = food.position
            x1, y1 = fx * CELL, fy * CELL
            x2, y2 = x1 + CELL, y1 + CELL
            self.canvas.create_oval(x1 - 2, y1 - 2, x2 + 2, y2 + 2,
                                    fill=COLORS["food_glow"], outline="", tags="food")
            self.canvas.create_oval(x1 + 2, y1 + 2, x2 - 2, y2 - 2,
                                    fill=COLORS["food"], outline="", tags="food")

        # ── NEW: Draw Godmode Glow ──
        # We draw this BEFORE the snake so the glow stays behind the body segments
        if self._godmode:
            for sx, sy in snake_pos:
                x1, y1 = sx * CELL - 3, sy * CELL - 3
                x2, y2 = x1 + CELL + 6, y1 + CELL + 6
                # Using a larger oval to create a "halo" effect
                self.canvas.create_oval(x1, y1, x2, y2, fill=COLORS["god_glow"], outline="")

        # Draw Snake segments
        for i, (sx, sy) in enumerate(snake_pos):
            x1, y1 = sx * CELL + 1, sy * CELL + 1
            x2, y2 = x1 + CELL - 2, y1 + CELL - 2
            
            if self._purple_snake:
                color = "#800080" if i == 0 else "#9932CC"
            else:
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

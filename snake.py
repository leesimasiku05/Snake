import tkinter as tk
import random
import json
import os


# -----------------------------
# Settings
# -----------------------------

WIDTH = 600
HEIGHT = 600
CELL_SIZE = 20

SNAKE_SPEED = 100

BACKGROUND = "black"
SNAKE_COLOR = "lime"
FOOD_COLOR = "red"
TEXT_COLOR = "white"

SCORE_FILE = "scores.json"


# -----------------------------
# Load high score
# -----------------------------

def load_high_score():
    if not os.path.exists(SCORE_FILE):
        return 0

    try:
        with open(SCORE_FILE, "r") as file:
            data = json.load(file)

        return data.get("high_score", 0)

    except (json.JSONDecodeError, FileNotFoundError):
        return 0


# -----------------------------
# Save high score
# -----------------------------

def save_high_score(score):
    data = {
        "high_score": score
    }

    with open(SCORE_FILE, "w") as file:
        json.dump(data, file, indent=4)


# -----------------------------
# Game variables
# -----------------------------

snake = []
food = None

direction = "Right"
next_direction = "Right"

score = 0
high_score = load_high_score()

game_over = False


# -----------------------------
# Create window
# -----------------------------

window = tk.Tk()
window.title("Snake The Game")
window.resizable(False, False)


# -----------------------------
# Score display
# -----------------------------

score_label = tk.Label(
    window,
    text=f"Score: {score}    High Score: {high_score}",
    font=("Arial", 18),
    bg=BACKGROUND,
    fg=TEXT_COLOR
)

score_label.pack(fill="x")


# -----------------------------
# Game canvas
# -----------------------------

canvas = tk.Canvas(
    window,
    width=WIDTH,
    height=HEIGHT,
    bg=BACKGROUND,
    highlightthickness=0
)

canvas.pack()


# -----------------------------
# Create snake
# -----------------------------

def create_snake():
    global snake

    snake = [
        [300, 300],
        [280, 300],
        [260, 300]
    ]


# -----------------------------
# Create food
# -----------------------------

def create_food():
    global food

    while True:
        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(0, HEIGHT, CELL_SIZE)

        if [x, y] not in snake:
            food = [x, y]
            break


# -----------------------------
# Draw game
# -----------------------------

def draw_game():
    canvas.delete("all")

    # Draw snake
    for x, y in snake:
        canvas.create_rectangle(
            x,
            y,
            x + CELL_SIZE,
            y + CELL_SIZE,
            fill=SNAKE_COLOR,
            outline="black"
        )

    # Draw food
    x, y = food

    canvas.create_oval(
        x,
        y,
        x + CELL_SIZE,
        y + CELL_SIZE,
        fill=FOOD_COLOR,
        outline=""
    )


# -----------------------------
# Change direction
# -----------------------------

def change_direction(event):
    global next_direction

    key = event.keysym

    if key == "Up" and direction != "Down":
        next_direction = "Up"

    elif key == "Down" and direction != "Up":
        next_direction = "Down"

    elif key == "Left" and direction != "Right":
        next_direction = "Left"

    elif key == "Right" and direction != "Left":
        next_direction = "Right"


# -----------------------------
# Move snake
# -----------------------------

def move_snake():
    global direction
    global score
    global high_score
    global game_over

    if game_over:
        return

    direction = next_direction

    head_x, head_y = snake[0]

    if direction == "Up":
        head_y -= CELL_SIZE

    elif direction == "Down":
        head_y += CELL_SIZE

    elif direction == "Left":
        head_x -= CELL_SIZE

    elif direction == "Right":
        head_x += CELL_SIZE

    new_head = [head_x, head_y]

    # -------------------------
    # Check wall collision
    # -------------------------

    if (
        head_x < 0
        or head_x >= WIDTH
        or head_y < 0
        or head_y >= HEIGHT
    ):
        end_game()
        return

    # -------------------------
    # Check self collision
    # -------------------------

    if new_head in snake:
        end_game()
        return

    # Add new head
    snake.insert(0, new_head)

    # -------------------------
    # Check food collision
    # -------------------------

    if new_head == food:
        score += 1

        if score > high_score:
            high_score = score
            save_high_score(high_score)

        score_label.config(
            text=f"Score: {score}    High Score: {high_score}"
        )

        create_food()

    else:
        # Remove tail if food wasn't eaten
        snake.pop()

    draw_game()

    window.after(SNAKE_SPEED, move_snake)


# -----------------------------
# Game over
# -----------------------------

def end_game():
    global game_over

    game_over = True

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2 - 30,
        text="GAME OVER",
        fill="white",
        font=("Arial", 40, "bold")
    )

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2 + 30,
        text=f"Score: {score}",
        fill="white",
        font=("Arial", 24)
    )

    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2 + 70,
        text="Press R to restart",
        fill="white",
        font=("Arial", 18)
    )


# -----------------------------
# Restart game
# -----------------------------

def restart_game(event=None):
    global score
    global direction
    global next_direction
    global game_over

    if not game_over:
        return

    score = 0

    direction = "Right"
    next_direction = "Right"

    game_over = False

    score_label.config(
        text=f"Score: {score}    High Score: {high_score}"
    )

    create_snake()
    create_food()
    draw_game()

    window.after(SNAKE_SPEED, move_snake)


# -----------------------------
# Keyboard controls
# -----------------------------

window.bind("<KeyPress>", change_direction)
window.bind("<r>", restart_game)
window.bind("<R>", restart_game)


# -----------------------------
# Start game
# -----------------------------

create_snake()
create_food()
draw_game()

window.after(SNAKE_SPEED, move_snake)

window.mainloop()


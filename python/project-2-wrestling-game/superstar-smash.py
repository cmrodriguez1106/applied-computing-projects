"""
WWE Superstar Smash
A WWE-themed Rock, Paper, Scissors game built with Python and Tkinter.

Run with: python superstar-smash.py

Only Python's standard library is required. Tkinter is included with most
standard Python installations.
"""

import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import random

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
ASSET_DIR = BASE_DIR / "assets"
BACKGROUND_FILE = ASSET_DIR / "ring.png"

WINDOW_WIDTH = 1350
WINDOW_HEIGHT = 900

CARD_WIDTH = 590
CARD_HEIGHT = 112
CARD_X = (WINDOW_WIDTH - CARD_WIDTH) // 2
CARD_START_Y = 175
CARD_GAP = 18

GOLD = "#D7B56D"
LIGHT_GOLD = "#FFE08A"
DARK = "#101827"
WHITE = "#FFFFFF"
BLACK = "#000000"

WRESTLERS = {
    "Roman Reigns": {
        "finisher": "<---- SPEAR ---->",
        "image": "roman_reigns.png"
    },
    "Seth Rollins": {
        "finisher": "##### STOMP #####",
        "image": "seth_rollins.png"
    },
    "Randy Orton": {
        "finisher": "!!!!! RKO !!!!!",
        "image": "randy_orton.png"
    }
}

# Each wrestler defeats the wrestler listed.
BEATS = {
    "Roman Reigns": "Randy Orton",
    "Seth Rollins": "Roman Reigns",
    "Randy Orton": "Seth Rollins"
}

# --------------------------------------------------
# WINDOW
# --------------------------------------------------

root = tk.Tk()
root.title("WWE Superstar Smash")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.resizable(False, False)

canvas = tk.Canvas(
    root,
    width=WINDOW_WIDTH,
    height=WINDOW_HEIGHT,
    highlightthickness=0,
    bd=0,
    bg=DARK
)

canvas.pack(fill="both", expand=True)

# --------------------------------------------------
# OUTLINED TEXT FUNCTION
# --------------------------------------------------

outlined_groups = {}

def create_outlined_text(
    x,
    y,
    text,
    fill=WHITE,
    font=("Verdana", 16, "bold"),
    outline_width=3,
    anchor="center"
):
    """
    Creates text with a thick black outline.
    Tkinter Canvas does not support native text strokes,
    so multiple offset text layers are used.
    """

    group = f"outlined_{len(outlined_groups)}"
    outlined_groups[group] = True

    offsets = [
        (-outline_width, 0),
        (outline_width, 0),
        (0, -outline_width),
        (0, outline_width),
        (-outline_width, -outline_width),
        (-outline_width, outline_width),
        (outline_width, -outline_width),
        (outline_width, outline_width)
    ]

    for dx, dy in offsets:
        canvas.create_text(
            x + dx,
            y + dy,
            text=text,
            fill=BLACK,
            font=font,
            anchor=anchor,
            tags=(group,)
        )

    canvas.create_text(
        x,
        y,
        text=text,
        fill=fill,
        font=font,
        anchor=anchor,
        tags=(group,)
    )

    return group

def update_outlined_text(group, text):
    """Updates all layers of an outlined text element."""
    canvas.itemconfigure(group, text=text)


# --------------------------------------------------
# BACKGROUND IMAGE
# --------------------------------------------------

try:
    background_image = tk.PhotoImage(
        file=str(BACKGROUND_FILE)
    )

    canvas.create_image(
        0,
        0,
        image=background_image,
        anchor="nw"
    )

except (tk.TclError, OSError) as error:
    messagebox.showerror(
        "Background Image Error",
        f"Could not load ring.png:\n\n{BACKGROUND_FILE}\n\n{error}"
    )
    root.destroy()
    raise SystemExit(1)


# --------------------------------------------------
# WRESTLER IMAGES
# --------------------------------------------------

wrestler_images = {}

for wrestler, details in WRESTLERS.items():

    image_path = ASSET_DIR / details["image"]

    try:
        original = tk.PhotoImage(file=str(image_path))

        wrestler_images[wrestler] = original.subsample(4, 4)

    except (tk.TclError, OSError) as error:

        messagebox.showerror(
            "Wrestler Image Error",
            f"Could not load:\n{image_path}\n\n{error}"
        )

        root.destroy()
        raise SystemExit(1)


# --------------------------------------------------
# GAME TITLE
# --------------------------------------------------

canvas.create_rectangle(
    345, 35, 1005, 105,
    fill=DARK,
    outline=GOLD,
    width=3
)

canvas.create_text(
    WINDOW_WIDTH // 2,
    70,
    text="WWE SUPERSTAR SMASH",
    fill=WHITE,
    font=("Verdana", 27, "bold")
)

# Subtitle: white text with black outline.
create_outlined_text(
    WINDOW_WIDTH // 2,
    135,
    "SELECT YOUR SUPERSTAR",
    fill=WHITE,
    font=("Verdana", 16, "bold"),
    outline_width=3
)


# --------------------------------------------------
# WRESTLER SELECTION CARDS
# --------------------------------------------------

card_tags = {}

def draw_card(wrestler, index):

    y1 = CARD_START_Y + index * (CARD_HEIGHT + CARD_GAP)
    y2 = y1 + CARD_HEIGHT

    tag = f"wrestler_{index}"

    # Card background.
    canvas.create_rectangle(
        CARD_X,
        y1,
        CARD_X + CARD_WIDTH,
        y2,
        fill=DARK,
        outline=GOLD,
        width=3,
        tags=(tag,)
    )

    # Wrestler image.
    canvas.create_image(
        CARD_X + 85,
        (y1 + y2) // 2,
        image=wrestler_images[wrestler],
        tags=(tag,)
    )

    # Wrestler name.
    canvas.create_text(
        CARD_X + 165,
        y1 + 39,
        text=wrestler,
        fill=WHITE,
        font=("Verdana", 18, "bold"),
        anchor="w",
        tags=(tag,)
    )

    # Finisher directly underneath the name.
    canvas.create_text(
        CARD_X + 165,
        y1 + 77,
        text=f"Finisher: {WRESTLERS[wrestler]['finisher']}",
        fill=LIGHT_GOLD,
        font=("Verdana", 12, "bold"),
        anchor="w",
        tags=(tag,)
    )

    card_tags[wrestler] = tag

    # Entire card is clickable.
    canvas.tag_bind(
        tag,
        "<Button-1>",
        lambda event, choice=wrestler: play(choice)
    )

    canvas.tag_bind(
        tag,
        "<Enter>",
        lambda event, choice=wrestler: highlight_card(choice, True)
    )

    canvas.tag_bind(
        tag,
        "<Leave>",
        lambda event, choice=wrestler: highlight_card(choice, False)
    )


def highlight_card(wrestler, hovered):

    color = LIGHT_GOLD if hovered else GOLD

    # The rectangle is the first item belonging to each card.
    rectangle = canvas.find_withtag(card_tags[wrestler])[0]

    canvas.itemconfigure(
        rectangle,
        outline=color
    )


for index, wrestler in enumerate(WRESTLERS):
    draw_card(wrestler, index)


# --------------------------------------------------
# GAME RESULTS
# --------------------------------------------------

player_text = create_outlined_text(
    WINDOW_WIDTH // 2,
    690,
    "",
    fill=WHITE,
    font=("Verdana", 17, "bold"),
    outline_width=4
)

computer_text = create_outlined_text(
    WINDOW_WIDTH // 2,
    725,
    "",
    fill=WHITE,
    font=("Verdana", 17, "bold"),
    outline_width=4
)

result_text = create_outlined_text(
    WINDOW_WIDTH // 2,
    765,
    "Choose a wrestler to begin!",
    fill=LIGHT_GOLD,
    font=("Verdana", 22, "bold"),
    outline_width=4
)

winner_text = create_outlined_text(
    WINDOW_WIDTH // 2,
    805,
    "",
    fill=WHITE,
    font=("Verdana", 15, "bold"),
    outline_width=4
)


# --------------------------------------------------
# GAME LOGIC
# --------------------------------------------------

def play(player_choice):

    computer_choice = random.choice(list(WRESTLERS.keys()))

    update_outlined_text(
        player_text,
        f"PLAYER: {player_choice} - "
        f"{WRESTLERS[player_choice]['finisher']}"
    )

    update_outlined_text(
        computer_text,
        f"COMPUTER: {computer_choice} - "
        f"{WRESTLERS[computer_choice]['finisher']}"
    )

    if player_choice == computer_choice:

        result = "IT'S A TIE!"
        winner = player_choice

    elif BEATS[player_choice] == computer_choice:

        result = "PLAYER WINS!"
        winner = player_choice

    else:

        result = "COMPUTER WINS!"
        winner = computer_choice

    update_outlined_text(result_text, result)

    update_outlined_text(
        winner_text,
        f"Winning Superstar: {winner}"
    )


# --------------------------------------------------
# RESET BUTTON
# --------------------------------------------------

def reset():

    update_outlined_text(player_text, "")
    update_outlined_text(computer_text, "")

    update_outlined_text(
        result_text,
        "Choose a wrestler to begin!"
    )

    update_outlined_text(winner_text, "")


RESET_X1 = 560
RESET_Y1 = 835
RESET_X2 = 790
RESET_Y2 = 885

canvas.create_rectangle(
    RESET_X1,
    RESET_Y1,
    RESET_X2,
    RESET_Y2,
    fill=DARK,
    outline=GOLD,
    width=3,
    tags=("reset_button",)
)

canvas.create_text(
    (RESET_X1 + RESET_X2) // 2,
    (RESET_Y1 + RESET_Y2) // 2,
    text="RESET MATCH",
    fill=WHITE,
    font=("Verdana", 13, "bold"),
    tags=("reset_button",)
)

canvas.tag_bind(
    "reset_button",
    "<Button-1>",
    lambda event: reset()
)

canvas.tag_bind(
    "reset_button",
    "<Enter>",
    lambda event: canvas.itemconfigure(
        "reset_button",
        outline=LIGHT_GOLD
    )
)

canvas.tag_bind(
    "reset_button",
    "<Leave>",
    lambda event: canvas.itemconfigure(
        "reset_button",
        outline=GOLD
    )
)


# --------------------------------------------------
# START GAME
# --------------------------------------------------

root.mainloop()

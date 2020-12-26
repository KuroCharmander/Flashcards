from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
ORIGINAL_FILE = "./data/french_words.csv"
LEARN_FILE = "./data/words_to_learn.csv"

try:
    data_file = pandas.read_csv(LEARN_FILE)
except FileNotFoundError:
    data_file = pandas.read_csv(ORIGINAL_FILE)
except Exception:
    # When there is a words_to_learn.csv but it is empty
    print("No cards in this file. Default to original file.")
    data_file = pandas.read_csv(ORIGINAL_FILE)
flashcard_words = data_file.to_dict(orient="records")
current_card = {}


def next_card():
    """Randomly choose another card to display if there are cards in flashcard_words."""
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    canvas.itemconfig(canvas_image, image=card_front_image)
    if len(flashcard_words) == 0:
        canvas.itemconfig(title_text, text="No Cards Left", fill="black")
        canvas.itemconfig(word_text, text="", fill="black")
    else:
        current_card = random.choice(flashcard_words)
        word = current_card[data_file.columns[0]]
        canvas.itemconfig(title_text, text=data_file.columns[0], fill="black")
        canvas.itemconfig(word_text, text=word, fill="black")
        flip_timer = window.after(3000, flip_card)


def flip_card():
    """Flip the card to show the answer."""
    word = current_card[data_file.columns[1]]
    canvas.itemconfig(canvas_image, image=card_back_image)
    canvas.itemconfig(title_text, text=data_file.columns[1], fill="white")
    canvas.itemconfig(word_text, text=word, fill="white")


def known_card():
    """User knows the card and answer so it will not reappear in the card deck."""
    if flashcard_words:
        flashcard_words.remove(current_card)
        words_to_learn = pandas.DataFrame(flashcard_words)
        words_to_learn.to_csv(LEARN_FILE, index=False)
        next_card()


# Setup window
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

# Setup the flashcards
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = PhotoImage(file="./images/card_front.png")
card_back_image = PhotoImage(file="./images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_image)
title_text = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)
right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=known_card)
right_button.grid(row=1, column=1)

next_card()


window.mainloop()

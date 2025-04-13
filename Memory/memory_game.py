import random
import tkinter as tk
from tkinter import messagebox


class MemoryGame:
    def __init__(self):
        self.selected = []
        self.moves = 0
        self.matched_pairs = 0

        button_style = {
            "font": ("Arial", 18, "bold"),
            "bg": "black",
            "fg": "white",
            "activebackground": "gray",
            "activeforeground": "white",
            "borderwidth": 0,
            "highlightthickness": 0,
        }
        self.rows = 4
        self.cols = 4

        button_width = 150
        button_height = 150

        self.root = tk.Tk()
        self.root.title("Memory Card Game")
        self.root.attributes("-fullscreen", True)

        canvas = tk.Canvas(
            self.root,
            width=self.root.winfo_screenwidth(),
            height=self.root.winfo_screenheight(),
        )
        canvas.pack()

        background_image = tk.PhotoImage(file=r"GUI\\space_background.png")
        canvas.create_image(0, 0, anchor="nw", image=background_image)

        self.create_card_grid()

        self.card_images = []
        for image_path in self.cards:
            image = tk.PhotoImage(file=image_path).subsample(3)
            self.card_images.append(image)

        self.card_back_image = tk.PhotoImage(file="GUI\\cards\\card_back.png")

        self.card_buttons = [[None] * self.cols for _ in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                card_button = tk.Button(
                    canvas,
                    image=self.card_back_image,
                    width=button_width,
                    height=button_height,
                    command=lambda r=row, c=col: self.show_card(r, c),
                    **button_style,
                )
                card_button.place(
                    relx=0.5
                    - (self.cols * button_width) / (2 * self.root.winfo_screenwidth()),
                    rely=0.5
                    - (self.rows * button_height)
                    / (2 * self.root.winfo_screenheight()),
                    x=col * button_width,
                    y=row * button_height,
                )
                self.card_buttons[row][col] = card_button

        self.moves_label = tk.Label(
            self.root, text="Moves: 0", font=("Arial", 16), fg="white", bg="black"
        )
        self.moves_label.place(relx=1.0, x=-10, y=10, anchor="ne")

        exit_button = tk.Button(
            self.root, text="Exit", font=("Arial", 14), command=self.exit_game
        )
        exit_button.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")

        self.root.mainloop()

    def create_card_grid(self):
        image_list = [
            "GUI\\cards\\1.png",
            "GUI\\cards\\1.png",
            "GUI\\cards\\2.png",
            "GUI\\cards\\2.png",
            "GUI\\cards\\3.png",
            "GUI\\cards\\3.png",
            "GUI\\cards\\4.png",
            "GUI\\cards\\4.png",
            "GUI\\cards\\5.png",
            "GUI\\cards\\5.png",
            "GUI\\cards\\6.png",
            "GUI\\cards\\6.png",
            "GUI\\cards\\7.png",
            "GUI\\cards\\7.png",
            "GUI\\cards\\8.png",
            "GUI\\cards\\8.png",
        ]

        random.shuffle(image_list)
        self.cards = [
            image_list[i % len(image_list)] for i in range(self.rows * self.cols)
        ]
        random.shuffle(self.cards)

    def show_card(self, row, col):
        if len(self.selected) < 2 and (row, col) not in self.selected:
            self.selected.append((row, col))
            self.card_buttons[row][col].config(
                image=self.card_images[row * self.cols + col]
            )
            self.card_buttons[row][col].update_idletasks()

            if len(self.selected) == 2:
                self.moves += 1
                self.moves_label.config(text="Moves: {}".format(self.moves))
                self.check_matching()

    def check_matching(self):
        row1, col1 = self.selected[0]
        row2, col2 = self.selected[1]
        if self.cards[row1 * self.cols + col1] == self.cards[row2 * self.cols + col2]:
            self.matched_pairs += 1
            if self.matched_pairs == self.rows * self.cols // 2:
                messagebox.showinfo("Congratulations!", "You won!")
            self.selected = []
        else:
            self.root.after(1000, self.hide_selected_cards)

    def hide_selected_cards(self):
        row1, col1 = self.selected[0]
        row2, col2 = self.selected[1]
        if self.cards[row1 * self.cols + col1] != self.cards[row2 * self.cols + col2]:
            self.card_buttons[row1][col1].config(image=self.card_back_image)
            self.card_buttons[row2][col2].config(image=self.card_back_image)
        self.selected = []

    def exit_game(self):
        if messagebox.askokcancel("Exit", "Do you want to exit the game?"):
            self.root.destroy()

if __name__=="__main__":
    MemoryGame()

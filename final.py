from tkinter import *
import random
import csv
from tkextrafont import *
import mysql.connector

is_wordle_over = True
score_ssaw, score_memory, score_astro = 0, 2000, 800
score_total = 0
nickname = ""


class WordleGame:
    def __init__(self, root):
        global is_wordle_over
        self.gamelauncher = GameLauncher
        self.root = root
        self.root.title("AstroWordle")
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.root.geometry("%dx%d" % (width, height))

        self.button_style = {
            "font": ("Consolas", 18, "bold"),
            "bg": "black",
            "fg": "white",
            "activebackground": "gray",
            "activeforeground": "white",
            "borderwidth": 0,
            "highlightthickness": 0,
        }

        self.background_image = PhotoImage(file=r"Wordle\wordle_bg.png")
        self.background_label = Label(root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        width = 400
        height = 800
        self.word_list = self.load_word_list()
        self.secret_word = self.generate_secret_word()
        print(self.secret_word)
        self.attempts = 0
        self.max_attempts = 7

        self.canvas1 = Canvas(self.root, width=width, height=height)
        self.canvas = Canvas(self.root, width=width, height=height, bg="black")
        self.canvas.pack()
        self.label = self.canvas.create_text(
            200,
            100,
            text="Enter a 5-letter word:",
            font=("Consolas", 18),
            fill="white",
        )

        self.entry = Entry(self.root)
        self.entry_window = self.canvas.create_window(200, 150, window=self.entry)
        self.entry.bind("<Return>", self.check_guess)

        self.next_button = Button(
            self.root,
            text="Next",
            state="disabled",
            command=self.destroy_game_window,
            **self.button_style,
        )
        self.next_button_window = self.canvas.create_window(
            200, 500, window=self.next_button
        )

        self.result_label = self.canvas.create_text(200, 300, text="", fill="white")

        self.feedback_frame = Frame(self.root, bg="black")
        self.feedback_frame_window = self.canvas.create_window(
            200, 450, window=self.feedback_frame
        )

    def load_word_list(self):
        with open("Wordle\wordlist.txt", "r") as file:
            return [line.strip() for line in file.readlines()]

    def generate_secret_word(self):
        self.word_list = self.load_word_list()
        return random.choice(self.word_list)

    def check_guess(self, event):
        guess = self.entry.get()
        guess = guess.lower()
        if len(guess) == 5:
            self.attempts += 1
            global score_astro
            score_astro -= 100
            if guess == self.secret_word:
                print(score_astro)
                self.feedback = self.get_feedback(guess)
                self.canvas.itemconfig(
                    self.result_label,
                    text=(f"Attempt {self.attempts}/{self.max_attempts}"),
                )
                self.game_over = True
                self.next_button.config(state=ACTIVE)
                self.canvas.itemconfig(
                    self.result_label,
                    text="""  CONGRATULATIONS! 
You guessed the word.""",
                    font=("Consolas", 18),
                )
            else:
                self.feedback = self.get_feedback(guess)
                self.canvas.itemconfig(
                    self.result_label,
                    text=f"Attempt {self.attempts}/{self.max_attempts}",
                    font=("Consolas", 18),
                )
                print(score_astro)

                if self.attempts >= self.max_attempts:
                    print(score_astro)
                    self.canvas.itemconfig(
                        self.result_label,
                        text=f"""     GAME OVER 
The word was '{self.secret_word}'""",
                        font=("Consolas", 16),
                    )
                    self.game_over = True
                    self.check_button.config(state=DISABLED)
                    self.next_button.config(state=ACTIVE)

        else:
            self.canvas.itemconfig(
                self.result_label,
                text="Please enter a 5 letter word!",
                font=("Consolas", 15),
            )

    def get_feedback(self, guess):
        for i in range(len(guess)):
            self.label = Label(
                self.feedback_frame,
                text=guess[i].upper(),
                font=("Consolas", 18),
                bg="black",
                fg="white",
            )
            self.label.grid(row=0, column=i, padx=10, pady=0)

            if guess[i] == self.secret_word[i]:
                self.label.config(fg="green")
            elif guess[i] in self.secret_word:
                self.label.config(fg="yellow")
            else:
                self.label.config(fg="white")
            self.new_label = tk.Label(
                root, text=self.label.cget("text"), font=self.label.cget("font")
            )

    def destroy_game_window(self):
        is_wordle_over = True
        self.root.destroy()


class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.selected = []
        self.moves = 0
        self.is_game_over = False
        self.matched_pairs = 0

        self.button_style = {
            "font": ("Consolas", 18, "bold"),
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

        self.root = root
        self.root.title("Memory Card Game")

        self.canvas = Canvas(
            self.root,
            width=self.root.winfo_screenwidth(),
            height=self.root.winfo_screenheight(),
        )
        self.canvas.pack()
        self.root.update()

        self.background_image = PhotoImage(file=r"Memory\memory_bg.png")
        self.background_label = Label(self.canvas, image=self.background_image)
        self.background_label.pack()

        self.create_card_grid()

        self.card_images = []
        for image_path in self.cards:
            image = PhotoImage(file=image_path).subsample(3)
            self.card_images.append(image)

        self.card_back_image = PhotoImage(file=r"Memory\cards\card_back.png")

        self.card_buttons = [[None] * self.cols for _ in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                self.card_button = Button(
                    self.canvas,
                    image=self.card_back_image,
                    width=button_width,
                    height=button_height,
                    command=lambda r=row, c=col: self.show_card(r, c),
                    **self.button_style,
                )
                self.card_button.place(
                    relx=0.5
                    - (self.cols * button_width) / (2 * self.root.winfo_screenwidth()),
                    rely=0.5
                    - (self.rows * button_height)
                    / (2 * self.root.winfo_screenheight()),
                    x=col * button_width,
                    y=row * button_height,
                )
                self.card_buttons[row][col] = self.card_button

        self.moves_label = Label(
            self.root, text="Moves: 0", font=("Consolas", 16), fg="white", bg="black"
        )
        self.moves_label.place(relx=1.0, x=-10, y=10, anchor="ne")

        self.next_button = Button(
            self.root,
            text="Next",
            state="disabled",
            command=self.destroy_game_window,
            **self.button_style,
        )
        self.next_button.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")

        self.root.mainloop()

    def create_card_grid(self):
        image_list = [
            r"memory\\cards\\1.png",
            r"memory\\cards\\1.png",
            r"memory\\cards\\2.png",
            r"memory\\cards\\2.png",
            r"memory\\cards\\3.png",
            r"memory\\cards\\3.png",
            r"memory\\cards\\4.png",
            r"memory\\cards\\4.png",
            r"memory\\cards\\5.png",
            r"memory\\cards\\5.png",
            r"memory\\cards\\6.png",
            r"memory\\cards\\6.png",
            r"memory\\cards\\7.png",
            r"memory\\cards\\7.png",
            r"memory\\cards\\8.png",
            r"memory\\cards\\8.png",
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
                global score_memory
                score_memory -= 50
                self.moves_label.config(text="Moves: {}".format(self.moves))
                self.check_matching()

    def check_matching(self):
        row1, col1 = self.selected[0]
        row2, col2 = self.selected[1]
        if self.cards[row1 * self.cols + col1] == self.cards[row2 * self.cols + col2]:
            self.matched_pairs += 1
            if self.matched_pairs == (self.rows * self.cols / 2):
                self.card_button.config(state="disabled")
                self.next_button.config(state="active")
                self.is_game_over = True
                self.label = Label(
                    self.root,
                    text="""CONGRATULATIONS!
YOU WON""",
                    font=("Consolas", 21, "bold"),
                    fg="white",
                    bg="black",
                    justify="center",
                )
                if self.moves > 25:
                    global score_memory
                    score_memory = 0
                self.label.place(relx=0.5, rely=0.5, anchor="center")
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

    def destroy_game_window(self):
        self.root.destroy()


class ShootingStarsAndWormholes:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="black")

        self.button_style = {
            "font": ("Consolas", 18, "bold"),
            "bg": "black",
            "fg": "white",
            "activebackground": "gray",
            "activeforeground": "white",
            "borderwidth": 0,
            "highlightthickness": 0,
        }

        self.canvas = Canvas(root, width=1300, height=720)
        self.canvas.configure(bg="black")
        self.canvas.pack()
        self.board = PhotoImage(file=r"Snakes and ladders\board\board.png")
        self.canvas.create_image(280, 0, anchor="nw", image=self.board)

        self.notice = Label(
            self.canvas, text="", font=("Consolas", 13), fg="white", bg="black"
        )
        self.notice.place(x=1000, y=250, anchor="nw")
        global score_ssaw

        self.computer_token = PhotoImage(file=r"Snakes and ladders\player\alien.png")
        self.computer_id = self.canvas.create_image(
            321, 630, anchor="nw", image=self.computer_token
        )

        self.player_token = PhotoImage(
            file=r"Snakes and ladders\player\playertoken.png"
        )
        self.player_id = self.canvas.create_image(
            321, 630, anchor="nw", image=self.player_token
        )

        self.dice_images = [
            PhotoImage(file=f"Snakes and ladders\dice\dice_{i}.png")
            for i in range(1, 7)
        ]

        self.roll_dice_button = Button(
            root, text="CLICK TO ROLL", command=self.turn, **self.button_style
        )
        self.roll_dice_button.place(x=50, y=150)

        self.message = Label(
            self.canvas, text="", font=("Consolas", 15), fg="white", bg="black"
        )
        self.message.place(x=1058, y=150, anchor="nw")

        self.computer_position = 0
        self.player_position = 0
        self.turn_counter = 0
        self.game_over = False

    def roll_dice(self):
        dice = random.randint(1, 6)
        dice_image = self.dice_images[dice - 1]
        self.canvas.create_image(140, 310, image=dice_image)
        self.root.update()
        self.notice.config(text="")
        self.message.config(text="")
        return dice

    def snake_check(self, position):
        with open("Snakes and ladders\\board\\snakes.txt", "r") as snakes:
            snakes_list = snakes.readlines()
            for i in snakes_list:
                start, end = map(int, i.strip().split(","))
                if position == start:
                    self.notice.config(
                        text="""OOPS! SOMEONE FELL INTO 
A WORMHOLE,
BETTER LUCK NEXT TIME..."""
                    )
                    return end
        return position

    def ladder_check(self, position):
        with open("Snakes and ladders\\board\\ladders.txt", "r") as ladders:
            ladders_list = ladders.readlines()
            for i in ladders_list:
                start, end = map(int, i.strip().split(","))
                if position == start:
                    self.notice.config(
                        text="""INCREDIBLE!
SOMEONE FOUND 
THEMSELF A SHOOTING STAR..."""
                    )
                    return end
        return position

    def move_player_token(self):
        dice_value = self.roll_dice()
        self.player_position += dice_value
        self.player_position = self.snake_check(self.player_position)
        self.player_position = self.ladder_check(self.player_position)

        if self.player_position > 100:
            self.player_position -= dice_value
            self.message.config(text="INVALID THROW")
        self.update_token_position(self.player_position, self.player_id)
        self.win_conditions()

    def move_computer_token(self):
        dice_value = self.roll_dice()
        self.computer_position += dice_value
        self.computer_position = self.snake_check(self.computer_position)
        self.computer_position = self.ladder_check(self.computer_position)

        if self.computer_position > 100:
            self.computer_position -= dice_value
            self.message.config(text="INVALID THROW")
        self.update_token_position(self.computer_position, self.computer_id)
        self.roll_dice_button.config(state="active")
        self.win_conditions()

    def update_token_position(self, position, token_id):
        with open("Snakes and ladders\\board\\co-ordinates.csv", "r") as coords_file:
            r = csv.reader(coords_file, delimiter="|")
            for i in r:
                if position == int(i[0]):
                    dx, dy = int(i[1]), int(i[2])
                    self.canvas.coords(token_id, dx, dy)
                    break

    def win_conditions(self):
        if self.computer_position == 100:
            self.message.config(text="ALIEN WINS")
            self.roll_dice_button.config(state="disabled")
            self.next_button = Button(
                self.root,
                text="Finish Game",
                command=self.destroy_game_window,
                **self.button_style,
            )
            self.next_button.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")
            self.game_over = True
        elif self.player_position == 100:
            self.message.config(text="   YOU WIN")
            global score_ssaw
            score_ssaw = 50
            self.roll_dice_button.config(state="disabled")
            self.next_button = Button(
                self.root,
                text="Finish Game",
                command=self.destroy_game_window,
                **self.button_style,
            )
            self.next_button.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")
            self.game_over = True

    def turn(self):
        if self.game_over == False:
            self.move_player_token()
            self.roll_dice_button.config(state="disabled")
            self.canvas.after(0, self.move_computer_token)

    def destroy_game_window(self):
        self.root.destroy()


class GameLauncher:
    def __init__(self, root):
        global score_total, score_ssaw, score_memory, score_astro
        self.root = root
        self.root.attributes("-fullscreen", True)
        self.root.title("Aztura")
        self.root.configure(bg="black")
        bg_image = PhotoImage(file=r"bg.png")
        background_label = Label(self.root, image=bg_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.big_font = Font(
            file=r"fonts\big_font.ttf",
            family="Dreamscape",
            size=80,
        )

        text = Label(
            self.root, text="AZTURA", font=self.big_font, fg="white", bg="black"
        )
        text.pack(pady=30)
        self.button_style = {
            "font": ("Consolas", 18, "bold"),
            "bg": "black",
            "fg": "white",
            "activebackground": "gray",
            "activeforeground": "white",
            "borderwidth": 0,
            "highlightthickness": 0,
        }
        self.button0 = Button(
            self.root, text="START", command=self.start, **self.button_style
        )
        self.button0.pack(pady=(40, 5))
        self.button1 = Button(
            self.root,
            text="ASTROWORDLE",
            state=DISABLED,
            command=self.start_wordle,
            **self.button_style,
        )
        self.button1.pack(pady=5)

        self.button_memory = Button(
            self.root,
            text="MEMORY GAME",
            state=DISABLED,
            command=self.start_memory,
            **self.button_style,
        )
        self.button_memory.pack(pady=5)
        self.button_ssaw = Button(
            self.root,
            text="SHOOTING STARS AND WORMHOLES",
            command=self.start_ssaw,
            state=DISABLED,
            **self.button_style,
        )
        self.button_ssaw.pack(pady=5)
        self.button3 = Button(
            self.root,
            text="SCOREBOARD",
            **self.button_style,
            command=self.score_board,
            state="disabled",
        )
        self.button3.pack(pady=5)
        self.button4 = Button(
            self.root, text="EXIT", command=self.exit_, **self.button_style
        )

        self.button2 = Button(
            self.root, text="HOW TO PLAY", command=self.how_to_play, **self.button_style
        )
        self.button2.pack(pady=5)
        self.button4.pack(pady=5)
        self.root.mainloop()

    def start(self):
        self.newwindow = Toplevel(self.root)
        self.newwindow.attributes("-fullscreen", True)
        self.newwindow.title("START")
        self.bg_image = PhotoImage(file=r"bg.png")
        self.background_label = Label(self.newwindow, image=self.bg_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.label_name = Label(
            self.newwindow,
            text="NICKNAME:",
            font=("Consolas", 15),
            fg="white",
            bg="black",
        )
        self.label_name.pack(pady=(30, 10))

        def display_story(event):
            global nickname
            nickname = self.name_entry.get()
            self.display = Label(
                self.newwindow,
                bg="black",
                fg="white",
                font=("Consolas", 14, "bold"),
                justify="left",
                text="Hello " + nickname + ","
                """

The year is 6048.The world as we know it is no more,
a radioactive leak destroyed life on Earth. Since then, a base named ASKY-40 
was founded to search for other planets with habitable conditions. Many tales 
of a planet was spread, which promised a safe atmosphere and even water bodies.
The search however was known to be a treacherous one, filled with wormholes, and aliens.
                               
You are an explorer. You have forever dreamed of finding this planet and saving humanity. 
Your mission is to travel across the interstellar void and find


               AZTURA...""",
            )

            self.display.pack(pady=(40, 0))

        self.name_entry = Entry(self.newwindow, font=("Consolas", 16))
        self.name_entry.pack()
        self.name_entry.bind("<Return>", display_story)
        self.button1.config(state=ACTIVE)
        self.button0.config(state=DISABLED)
        self.return_button = Button(
            self.newwindow,
            text="Return to Menu",
            command=lambda: self.return_to_menu(),
            **self.button_style,
        )
        self.return_button.pack(padx=10, pady=10, anchor="se", side="bottom")

        self.newwindow.mainloop()

    def start_wordle(self):
        self.button1.config(state=DISABLED)
        self.button_memory.config(state=ACTIVE)
        self.newwindow = Toplevel(self.root)
        self.newwindow.attributes("-fullscreen", True)
        self.newwindow.title("LEVEL 1")
        self.wordle_launch = WordleGame(self.newwindow)
        self.wordle_launch
        self.newwindow.mainloop()

    def start_memory(self):
        self.button_ssaw.config(state=ACTIVE)
        self.button_memory.config(state=DISABLED)
        self.newwindow = Toplevel(self.root)
        self.newwindow.attributes("-fullscreen", True)
        self.newwindow.title("LEVEL 2")
        self.memory_launch = MemoryGame(self.newwindow)
        self.memory_launch
        self.newwindow.mainloop()

    def start_ssaw(self):
        self.button3.config(state=ACTIVE)
        self.button_ssaw.config(state=DISABLED)
        self.newwindow = Toplevel(self.root)
        self.newwindow.attributes("-fullscreen", True)
        self.newwindow.title("LEVEL 3")
        self.ssaw_launch = ShootingStarsAndWormholes(self.newwindow)
        self.ssaw_launch
        self.newwindow.mainloop()

    def return_to_menu(self):
        self.newwindow.destroy()
        self.root.deiconify()

    def score_board(self):
        self.newwindow = Toplevel(self.root)
        self.newwindow.attributes("-fullscreen", True)
        self.newwindow.title("SCOREBOARD")
        self.scoreboard_launch = ScoreBoard(self.newwindow)
        self.scoreboard_launch
        self.newwindow.mainloop()

    def how_to_play(self):
        self.newwindow = Toplevel(self.root)
        self.newwindow.attributes("-fullscreen", True)
        self.newwindow.title("HOW TO PLAY")
        self.newwindow.configure(bg="black")

        self.bg_image = PhotoImage(file=r"bg.png")
        self.background_label = Label(self.newwindow, image=self.bg_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.rules_frame = Frame(self.newwindow, bg="black")
        self.rules_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.rules = Label(
            self.rules_frame,
            text="""Level 1: AstroWordle

1. In the "AstroWordle Game" the alien will provide you with a secret five-letter word to guess.
2. Remember! The words are related to what the alien sees!
3. You have 10 attempts to guess the word correctly.
4. After each guess, you will receive feedback on your word:
     ○ A green letter indicates that a letter is in the correct position.
     ○ A yellow letter indicates that a letter is in the word but in the wrong position.
     ○ A red letter means the letter is not in the word at all.
5. Your goal is to guess the five-letter word within the 10 attempts given.
6. You earn points based on the number of guesses it takes you to guess the word
7. If you successfully guess the word within 10 attempts, you win the round and earn points.

Level 2: Memory Card Game

1. In the "Memory Card Game," the alien will present a grid of face-down cards, each with a different pattern on the other side.
2. You will start by clicking on one card to reveal its pattern. The location of that card will be revealed.
3. Your goal is to find all the matching pairs of cards with the same pattern.
4. To find a matching pair, click on a second card. If the patterns on the two cards match, they will remain face-up.
5. If the patterns on the two cards do not match, they will be flipped back over, and their locations will be concealed again.
6. Your score is based on the number of moves you make to find all matching pairs.

Level 3: Wormholes and Shooting Stars

1. The game "Wormholes and Shooting Stars" is similar to the classic game of Snake and Ladders.
2. Roll the dice to determine the number of spaces you can move.
3. Your goal is to reach the finish line before the alien does.
4. Watch out for wormholes, which can teleport you to a different location on the board.
5. Shooting stars will boost your progress, allowing you to move ahead.
6. The game continues until either you or the alien reaches the finish line.""",
            font=("Consolas", 13, "bold"),
            fg="white",
            bg="black",
            justify="left",
        )

        self.rules.pack()
        return_button = Button(
            self.newwindow,
            text="Return to Menu",
            command=lambda: self.return_to_menu(),
            **self.button_style,
        )
        return_button.pack(padx=10, pady=10, anchor="se", side="bottom")

        self.root.withdraw()
        self.newwindow.mainloop()

    def exit_(self):
        self.root.destroy()


class ScoreBoard:
    def __init__(self, root):
        self.button_style = {
            "font": ("Consolas", 18, "bold"),
            "bg": "black",
            "fg": "white",
            "activebackground": "gray",
            "activeforeground": "white",
            "borderwidth": 0,
            "highlightthickness": 0,
        }
        global nickname, score_total, score_ssaw, score_memory, score_astro
        score_total = score_astro + score_memory + score_ssaw
        obj = mysql.connector.connect(
            host="localhost", user="root", database="aztura", password="123"
        )
        c = obj.cursor()
        c.execute("use aztura")
        c.execute(
            "insert into scoreboard values(%s,%s,%s,%s,%s)",
            (nickname, score_astro, score_memory, score_ssaw, score_total),
        )
        obj.commit()
        c.execute("select player_name,total_score from scoreboard")
        rank = c.fetchall()
        c.close()
        obj.close()
        print(score_total)
        rank_dictionary = {}
        for i in rank:
            print(i)
            rank_dictionary[i[1]] = i[0]
        print(rank_dictionary.items())
        sorted_dict_keys = dict(sorted(rank_dictionary.items(), reverse=True))

        self.root = root
        self.canvas = Canvas(
            self.root,
            background="red",
            width=self.root.winfo_screenwidth(),
            height=self.root.winfo_screenheight(),
        )
        self.canvas.pack()
        self.background_image = PhotoImage(file=r"bg.png")
        self.background_label = Label(
            self.canvas, image=self.background_image, font=("Consolas", 20, "bold")
        )
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.current_score_label = Label(
            self.canvas,
            text="Total Score:" + str(score_total),
            bg="black",
            fg="yellow",
            font=("Consolas", 20, "bold"),
        )
        self.current_score_label.place(x=0, y=0)
        self.ranktext_label = Label(
            self.canvas,
            text="HIGHSCORE",
            pady=5,
            bg="black",
            fg="yellow",
            font=("Consolas", 20, "bold"),
        )
        self.ranktext_label.place(x=500, y=10)
        n = 0
        for i in sorted_dict_keys:
            self.rank_label = Label(
                self.canvas,
                text=str(n + 1) + "." + str(sorted_dict_keys[i]) + "   " + str(i),
                bg="black",
                fg="yellow",
                font=("Consolas", 20, "bold"),
            )
            self.rank_label.place(x=500, y=(1 + n) * 50)
            n += 1

        self.next_button = Button(
            self.root,
            text="Return to Menu",
            command=self.destroy_game_window,
            **self.button_style,
        )
        self.next_button.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")

    def destroy_game_window(self):
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    game_launcher = GameLauncher(root)
    root.mainloop()

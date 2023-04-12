import random
import tkinter as tk


class Spēle: # Satur spēles pamatinformāciju
    def __init__(self, player_starts=True):
        self.target_number = random.randint(15, 25)
        self.current_number = 0
        self.player1_score = 0
        self.is_player1_turn = player_starts
        self.is_game_over = False

        if not player_starts:
            self.best_move()

    def speletaja_gajiens(self, move): # Nosaka ko darīt, kad ir spēlētāja gājiens vai nav
        if not self.is_game_over:
            if self.is_player1_turn:
                self.current_number += move
                self.player1_score = self.current_number
                self.is_player1_turn = False
            self.best_move()
            self.parbaudit_speles_notikumu()

    def best_move(self):  # Minimaks gājiens jeb nosaka labāko gājienu
        best_score, best_move = self.minimax(0, self.is_player1_turn)
        self.current_number += best_move
        if self.is_player1_turn:
            self.player1_score = self.current_number
            self.is_player1_turn = False
        else:
            self.is_player1_turn = True

    def minimax(self, depth, is_maximizing):  # Minimaks algoritms kas nosaka VISU koku, turot rezultātus Tuplī
        if self.current_number >= self.target_number:
            if is_maximizing:
                return -10 + depth, None
            else:
                return 10 - depth, None

        if is_maximizing:
            best_score = -float('inf')
            best_move = None
            for move in range(1, 4):
                self.current_number += move
                score, _ = self.minimax(depth + 1, False)
                self.current_number -= move
                if score > best_score:
                    best_score = score
                    best_move = move
        else:
            best_score = float('inf')
            best_move = None
            for move in range(1, 4):
                self.current_number += move
                score, _ = self.minimax(depth + 1, True)
                self.current_number -= move
                if score < best_score:
                    best_score = score
                    best_move = move

        return best_score, best_move

    def parbaudit_speles_notikumu(self):  # Pārbauda vai spēle ir beigusies
        if self.current_number >= self.target_number:
            self.is_game_over = True


class GUI: # Rāda visas pogas uz ekrāna
    def __init__(self, master, is_player1_human):
        self.master = master
        self.master.title("Number Spēle")
        self.master.geometry("250x150")
        self.game = Spēle(is_player1_human)

        self.label_target_number = tk.Label(self.master, text=f"Target number: {self.game.target_number}")
        self.label_target_number.pack()

        self.label_current_number = tk.Label(self.master, text=f"Current number: {self.game.current_number}")
        self.label_current_number.pack()

        self.button1 = tk.Button(self.master, text="1", command=lambda: self.speletaja_gajiens(1))
        self.button1.pack(side=tk.LEFT, padx=5)

        self.button2 = tk.Button(self.master, text="2", command=lambda: self.speletaja_gajiens(2))
        self.button2.pack(side=tk.LEFT, padx=5)

        self.button3 = tk.Button(self.master, text="3", command=lambda: self.speletaja_gajiens(3))
        self.button3.pack(side=tk.LEFT, padx=5)

        self.button4 = tk.Button(self.master, text="RETRY", command=lambda: self.retry())
        self.button4.pack(side=tk.RIGHT, padx=5)

        self.statusbar = tk.Label(self.master, text="Player 1's turn")
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.master.mainloop()

    def speletaja_gajiens(self, move):  # Nosaka ko darīt, kad ir spēlētāja gājiens vai nav
        if not self.game.is_game_over:
            if self.game.is_player1_turn:
                self.game.current_number += move
                self.game.player1_score = self.game.current_number
                self.game.is_player1_turn = False
            self.game.best_move()
            self.game.parbaudit_speles_notikumu()
            self.update_labels()

    def retry(self):  # Ļauj sākt spēli no jauna

        self.master.destroy()
        new_root = tk.Tk()
        start_screen = StartScreen(new_root, player_starts=True)
        new_root.mainloop()


    def update_labels(self): # Atjauno textu, kas nosaka kura spēlētāja gājiens ir
        self.label_current_number.config(text=f"Current number: {self.game.current_number}")
        if self.game.is_player1_turn:
            self.statusbar.config(text="Player 1's turn")
        else:
            self.statusbar.config(text="Player 2's turn")
        if self.game.is_game_over:
            if self.game.player1_score == self.game.target_number:
                self.statusbar.config(text="Player 1 wins!")
            else:
                self.statusbar.config(text="Player 2 wins!")


class StartScreen:   # Klase parāda logu kas vaicā kas grib sākt spēli
    def __init__(self, master, player_starts=True):
        self.master = master
        self.master.title("Number Spēle")
        self.master.geometry("300x200")

        self.game = None

        self.label_title = tk.Label(self.master, text="Number Spēle!", font=("Arial", 18))
        self.label_title.pack(pady=10)

        self.button_human_first = tk.Button(self.master, text="Human first", command=self.set_human_first)
        self.button_human_first.pack(pady=5)

        self.button_ai_first = tk.Button(self.master, text="AI first", command=self.set_ai_first)
        self.button_ai_first.pack(pady=5)

        if self.set_human_first:
            self.game = Spēle(player_starts=True)
        else:
            self.game = Spēle(player_starts=False)

    def set_human_first(self): # Pārbauda vai Cilvēks sāk gājienu
        self.is_human_first = True
        self.start_game()


    def set_ai_first(self): # Pārbauda vai AI sāk gājienu
        self.is_human_first = False
        self.start_game()

    def start_game(self):  # Tiek sākta spēle
        self.game.current_number = 0
        self.close()
        root = tk.Tk()
        gui = GUI(root, is_player1_human=self.is_human_first)

    def close(self):  # Tiek iznīcināts objekts
        self.master.destroy()


if __name__ == "__main__":  # Tiek palaists kods
    root = tk.Tk()
    start_screen = StartScreen(root, player_starts=True)
    root.mainloop()


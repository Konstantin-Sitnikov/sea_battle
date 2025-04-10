import tkinter as tk
from tkinter import BooleanVar, StringVar
from game_field import GameField


class TwoPlayer(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.wm_attributes("-topmost", 1)

        self.name_1 = "Имя 1"
        self.player_one_move = BooleanVar(value=True)

        self.name_2 = "Имя 2"
        self.player_two_move = BooleanVar(value=False)

        self.text_player_move = StringVar()

        self.player_name_display()
        self.player_one_move.trace_add("write", self.player_name_display)

        label_player_move = tk.Label(self, textvariable=self.text_player_move)
        label_player_move.grid(row=2, column=0, columnspan=3, sticky="n")


        container = tk.Frame(self, height=500, width=500)
        container.grid(row=3, column=0, columnspan=3, sticky="n")

        self.field_one = GameField(container, self, name=self.name_1, my_move=self.player_one_move, enemy_move=self.player_two_move)
        self.field_one.grid(row=3, column=0, sticky="n")

        self.fild_two = GameField(container, self, name=self.name_2, my_move=self.player_two_move, enemy_move=self.player_one_move)
        self.fild_two.grid(row=3, column=1, sticky="n")

        self.check_player_one_move()
        self.check_player_two_move()

        self.player_one_move.trace_add("write", self.check_player_one_move)
        self.player_two_move.trace_add("write", self.check_player_two_move)

    def player_name_display(self, *args):
        if self.player_one_move.get():
            self.text_player_move.set(f"Ход игрока: {self.name_1}")
        elif self.player_two_move:
            self.text_player_move.set(f"Ход игрока: {self.name_2}")

    def check_player_one_move(self, *args):
        if self.player_one_move.get():
            self.fild_two.move_true()
        else:
            self.fild_two.move_false()

    def check_player_two_move(self, *args):
        if self.player_two_move.get():
            self.field_one.move_true()
        else:
            self.field_one.move_false()



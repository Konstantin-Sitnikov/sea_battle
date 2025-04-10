import tkinter as tk
from one_player import OnePlayer
from two_player import TwoPlayer


class StartWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("400x400")
        self.wm_title("Игра морской бой")
        self.wm_attributes("-topmost", 1)
        label = tk.Label(self, text="Добро пожаловать в игру морской бой")
        label.grid(row=1, column=0, columnspan=3, sticky="n")

        tk.Button(self, text="Один игрок", command=lambda: self.start_one_player()).grid(row=2, column=0, columnspan=3, sticky="n")
        tk.Button(self, text="Два игрока", command=lambda: self.start_two_player()).grid(row=3, column=0, columnspan=3, sticky="n")

    def start_one_player(self):
        window = OnePlayer(self)
        window.grab_set()


    def start_two_player(self):
        window = TwoPlayer(self)
        window.grab_set()


if __name__ == "__main__":
    game = StartWindow()
    game.mainloop()
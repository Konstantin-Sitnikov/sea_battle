import tkinter as tk
from tkinter import ttk
import random


class Windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("200x200")
        self.wm_title("Игра морской бой")
        self.wm_attributes("-topmost", 1)

        tk.Button(self, text="Один игрок", command=lambda: self.start_one_player()).pack()
        tk.Button(self, text="Два игрока", command=lambda: self.start_two_player()).pack()

    def start_one_player(self):
        window = OnePlayer(self)
        window.grab_set()


    def start_two_player(self):
        window = TwoPlayer(self)
        window.grab_set()

class OnePlayer(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.wm_attributes("-topmost", 1)

        canvas_x = 400
        canvas_y = 400
        n_x = n_y = 10 #количество ячеек
        step_x = canvas_x // n_x
        step_y = canvas_y // n_y
        print(step_x, step_y)

        label = tk.Label(self, text="Добро пожаловать в игру морской бой")
        label.grid(row=1, column=0, columnspan=2, sticky="n")

        field_one = tk.Canvas(self, bg = "white",
                              width=canvas_x,
                              height=canvas_y,
                              highlightthickness=2,
                              highlightbackground='black'
                              )
        field_one.grid(row=2, column=0, sticky="n")

        for i in range(n_x):
            field_one.create_line(0, step_y * i, canvas_x+5, step_y * i)

        for i in range(n_y):
            field_one.create_line(step_x * i, 0, step_x * i, canvas_y+5)


        field_two = tk.Canvas(self, bg = "white", width=canvas_x, height=canvas_y)
        field_two.grid(row=2, column=1, sticky="n")

        for i in range(n_x):
            field_two.create_line(0, step_y * i, canvas_x, step_y * i)

        for i in range(n_y):
            field_two.create_line(step_x * i, 0, step_x * i, canvas_y)






class TwoPlayer(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)

        self.wm_attributes("-topmost", 1)

        canvas = tk.Canvas(self, bg = "white", width=800, height=400)
        canvas.pack()





if __name__ == "__main__":
    game = Windows()
    game.mainloop()
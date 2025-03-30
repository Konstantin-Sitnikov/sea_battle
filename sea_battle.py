import tkinter as tk
from tkinter import ttk
import random
import time


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

        self.canvas_x = 400
        self.canvas_y = 400
        self.n_x = self.n_y = 10 #количество ячеек
        self.step_x = self.canvas_x // self.n_x
        self.step_y = self.canvas_y // self.n_y


        label = tk.Label(self, text="Добро пожаловать в игру морской бой")
        label.grid(row=1, column=0, columnspan=3, sticky="n")

        self.field_one = self.field_creation(row=2, col=0)
        self.field_one_coord = self.coord_fild()
        print(self.field_one_coord)
        field_two = self.field_creation(row=2, col=2)

        self.field_one.bind("<Button-1>", self.field_coordinates)

        tk.Button(self, text="Очистить поле", command=self.clear_fild).grid(row=4, column=0, sticky="n")

    def clear_fild(self):
        self.field_one.delete("X")
        self.field_one_coord = self.coord_fild()


    def field_coordinates(self, event):
        n_x = event.x // self.step_x
        n_y = event.y // self.step_y
        self.field_one_coord[n_x, n_y] = "X"
        self.update_fild()


    def update_fild(self):
        for coord in self.field_one_coord:
            if self.field_one_coord[coord] == "X":
                n_x = coord[0]
                n_y = coord[1]
                self.field_one.create_line(n_x * self.step_x,
                                           n_y * self.step_y,
                                           n_x * self.step_x + self.step_x,
                                           n_y * self.step_y + self.step_y,
                                           fill="red", tags=["X"])
                self.field_one.create_line(n_x * self.step_x + self.step_x,
                                           n_y * self.step_y,
                                           n_x * self.step_x,
                                           n_y * self.step_y + self.step_y,
                                           fill="red", tags=["X"])
                self.update_idletasks()
                self.update()



    def field_creation(self, row, col):
        field = tk.Canvas(self, bg="white",
                              width=self.canvas_x,
                              height=self.canvas_y,
                              highlightthickness=2,
                              highlightbackground='black'
                              )
        field.grid(row=row, column=col, sticky="n")

        for i in range(self.n_x):
            field.create_line(0, self.step_y * i, self.canvas_x + 5, self.step_y * i)

        for i in range(self.n_y):
            field.create_line(self.step_x * i, 0, self.step_x * i, self.canvas_y + 5)
        return field

    def coord_fild(self):
        fild = {}
        for x in range(10):
            for y in range(10):
                fild[x, y] = '-'
        return fild





class TwoPlayer(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)

        self.wm_attributes("-topmost", 1)

        canvas = tk.Canvas(self, bg = "white", width=800, height=400)
        canvas.pack()





if __name__ == "__main__":
    game = Windows()
    game.mainloop()
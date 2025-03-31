import tkinter as tk
from tkinter import ttk, PhotoImage
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

        self.ships = {"Однопалубный_1": {(0, 0): "+"},
                      "Однопалубный_2": {(5, 7): "+"},
                      "Однопалубный_3": {(8, 1): "+"},
                      "Однопалубный_4": {(9, 9): "+"},
                      "Двухпалубный_1": {(2, 3): "+", (3, 3): "+"},
                      "Двухпалубный_2": {(5, 1): "+", (6, 1): "+"},
                      # "Трехпалубный": {(4, 1): "+", (5, 1): "+", (6, 1): "+"}
                      }

        self.field_one = self.field_creation(row=2, col=0)
        self.field_one_coord = self.coord_fild()
        print(self.field_one_coord)
        field_two = self.field_creation(row=2, col=2)

        self.field_one.bind("<Button-1>", self.set_coordinates)
        frame = tk.Frame(self)
        frame.grid(row=4, column=1, sticky="n")

        tk.Button(frame, text="Очистить поле", command=self.clear_fild).grid(row=1, column=1, sticky="n")
        tk.Button(frame, text="Показать корабли", command=self.show_ships).grid(row=1, column=2, sticky="n")
        tk.Button(frame, text="Скрыть корабли", command=self.hide_ships).grid(row=1, column=3, sticky="n")

    def clear_fild(self):
        self.field_one.delete("X")
        self.field_one_coord = self.coord_fild()

    def hide_ships(self):
        self.field_one.delete("ship")

    def show_ships(self):
        for ship in self.ships.values():
            for coord in ship.keys():
                n_x = coord[0] * self.step_x
                n_y = coord[1] * self.step_y
                self.field_one.create_rectangle(n_x, n_y, n_x + self.step_x, n_y + self.step_y, fill="black", tags=["ship"])



    def set_coordinates(self, event):
        n_x = event.x // self.step_x
        n_y = event.y // self.step_y
        test = False
        for ship in self.ships.values():
            if not test:
                for coord, val in ship.items():
                    # print(coord)
                    # print((n_x, n_y) == coord)
                    if (n_x, n_y) == coord:
                        test = True
                        ship[n_x, n_y] = "-"
                        break

            else: break

        if test:
            self.field_one_coord[n_x, n_y] = "X"
        else:
            self.field_one_coord[n_x, n_y] = "0"

        print(self.ships)

        self.update_fild()


    def update_fild(self):

        for coord in self.field_one_coord:
            n_x = coord[0] * self.step_x
            n_y = coord[1] * self.step_y
            if self.field_one_coord[coord] == "X":

                self.field_one.create_rectangle(n_x + 5, n_y + 5, n_x + self.step_x - 5, n_y + self.step_y - 5, fill="red", tags=["X"])

                self.field_one.create_line(n_x + 5, n_y + 5, n_x + self.step_x -5 , n_y + self.step_y - 5,
                                           fill="black", tags=["X"])

                self.field_one.create_line(n_x + self.step_x - 5,
                                           n_y + 5,
                                           n_x + 5,
                                           n_y + self.step_y - 5,
                                           fill="black", tags=["X"])

            elif self.field_one_coord[coord] == "0":
                self.field_one.create_oval(n_x + 3 * self.step_x // 8,
                                           n_y + 3 * self.step_y // 8,
                                           n_x + 3 * self.step_x // 8 + self.step_x // 4,
                                           n_y + 3 * self.step_y // 8 + self.step_y // 4,
                                           fill="red", tags=["X"])




    def field_creation(self, row, col):
        frame_x = tk.Frame(self)
        frame_x.grid(row=row, column=col + 1, sticky="n")
        for i in range(self.n_x):
            tk.Label(frame_x, text=i).grid(row=0, column=i, padx=14)

        frame_y = tk.Frame(self)
        frame_y.grid(row=row + 1 , column=col, rowspan=self.n_y, sticky="n")
        for i in range(self.n_y):
            tk.Label(frame_y, text=i).grid(row=i, column=0, pady=9.4)


        field = tk.Canvas(self, bg="white",
                              width=self.canvas_x-2,
                              height=self.canvas_y-2,
                              highlightthickness=2,
                              highlightbackground='black'
                              )
        field.grid(row=row + 1, column=col + 1, sticky="n")

        for i in range(self.n_x):
            field.create_line(0, self.step_y * i, self.canvas_x, self.step_y * i)

        for i in range(self.n_y):
            field.create_line(self.step_x * i, 0, self.step_x * i, self.canvas_y)
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
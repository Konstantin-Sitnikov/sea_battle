import tkinter as tk
from idlelib import testing
from tkinter import BooleanVar

from set_ships import SetShips




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
        label = tk.Label(self, text="Добро пожаловать в игру морской бой")
        label.grid(row=1, column=0, columnspan=3, sticky="n")
        self.name_1 = "Имя 1"
        self.var_1 = BooleanVar(value=True)

        self.name_2 = "Имя 2"
        self.var_2 = BooleanVar(value=False)

        container = tk.Frame(self, height=500, width=500)
        container.grid(row=2, column=0, columnspan=3, sticky="n")


        self.fild_one = Test(container, self, name=self.name_1, my_move=self.var_1, enemy_move=self.var_2)
        self.fild_one.grid(row=3, column=0, sticky="n")

        self.fild_two = Test(container, self, name=self.name_2, my_move=self.var_2, enemy_move=self.var_1)
        self.fild_two.grid(row=3, column=1, sticky="n")






class Test(tk.Frame):
    def __init__(self, parent, controller, name, my_move, enemy_move):
        tk.Frame.__init__(self, parent)
        self.name = name
        self.my_move = my_move
        self.enemy_move = enemy_move

        tk.Label(self, text=self.name).grid(row=1, column=1, sticky="n")

        self.canvas_x = 400
        self.canvas_y = 400
        self.n_x = self.n_y = 10 #количество ячеек
        self.step_x = self.canvas_x // self.n_x
        self.step_y = self.canvas_y // self.n_y



        self.ships = {'Однопалубный_1': {(0, 0): '+'},
                      'Однопалубный_2': {(0, 9): '+'},
                      'Однопалубный_3': {(9, 9): '+'},
                      'Однопалубный_4': {(9, 0): '+'},
                      'Двухпалубный_1': {(0, 7): '+', (1, 7): '+'},
                      'Двухпалубный_2': {(8, 7): '+', (9, 7): '+'},
                      'Двухпалубный_3': {(4, 0): '+', (4, 1): '+'},
                      'Трехпалубный_1': {(3, 7): '+', (3, 8): '+', (3, 9): '+'},
                      'Трехпалубный_2': {(6, 7): '+', (6, 8): '+', (6, 9): '+'},
                      'Четырехпалубный': {(3, 4): '+', (4, 4): '+', (5, 4): '+', (6, 4): '+'}
                    }


        self.field = self.field_creation(row=2, col=0)
        self.field_coord = self.coord_fild()

        self.check_var()
        self.my_move.trace_add("write", self.check_var)

        self.frame = tk.Frame(self)
        self.frame.grid(row=4, column=1, sticky="n")

        tk.Button(self.frame, text="Очистить поле", command=self.clear_fild).grid(row=1, column=1, sticky="n")
        tk.Button(self.frame, text="Показать корабли", command=self.show_ships).grid(row=1, column=2, sticky="n")
        tk.Button(self.frame, text="Скрыть корабли", command=self.hide_ships).grid(row=1, column=3, sticky="n")
        tk.Button(self.frame, text="Задать координаты кораблей", command=self.set_coordinates_ship).grid(row=2, column=2, sticky="n")
        tk.Button(self.frame, text="False", command=self.stroke_transition).grid(row=3,column=1, sticky="n")

    def stroke_transition(self):
        self.my_move.set(False)
        self.enemy_move.set(True)



    def check_var(self, *args):
        if self.my_move.get():
            self.field.bind("<Button-1>", self.set_coordinates)
        else:
            self.field.unbind("<Button-1>")

    def clear_fild(self):
        self.field.delete("X")
        self.field_coord = self.coord_fild()

    def hide_ships(self):
        self.field.delete("ship")

    def show_ships(self):
        for ship in self.ships.values():
            for coord in ship.keys():
                n_x = coord[0] * self.step_x
                n_y = coord[1] * self.step_y
                self.field.create_rectangle(n_x, n_y, n_x + self.step_x, n_y + self.step_y, fill="black", tags=["ship"])

    def set_coordinates_ship(self):
        print(self.ships)
        ships = SetShips(self)
        self.ships = ships.open()
        print(self.ships)



    def check_ship_destroyed(self):
        ship_destroyed = {}
        for ship, values in self.ships.items():
            list_values = list(values.values())
            if list_values.count("-") == len(list_values):
                ship_destroyed[ship] = values
                del self.ships[ship]
                break

        return ship_destroyed


    def outline_destroyed_ship(self, dict):

        def valid_coord(coord):
            if coord == 0:
                list_coord = [coord, coord + 1]
            elif coord == 9:
                list_coord = [coord - 1, coord]
            else:
                list_coord = [coord - 1, coord, coord + 1]
            return list_coord


        for values in dict.values():
            for coord in values.keys():
                x = coord[0]
                y = coord[1]

                for i in valid_coord(x):
                    for j in valid_coord(y):
                        if self.field_coord[i, j] == "-":
                            self.field_coord[i, j] = "0"

                            self.field.create_oval(i * self.step_x + 3 * self.step_x // 8,
                                                   j * self.step_y + 3 * self.step_y // 8,
                                                   i * self.step_x + 3 * self.step_x // 8 + self.step_x // 4,
                                                   j * self.step_y + 3 * self.step_y // 8 + self.step_y // 4,
                                                   fill="red", tags=["X"])




    def set_coordinates(self, event):
        n_x = event.x // self.step_x
        n_y = event.y // self.step_y
        if self.field_coord[n_x, n_y] == "-":
            x = n_x * self.step_x
            y = n_y * self.step_y

            test = False
            for ship in self.ships.values():
                if not test:
                    for coord in ship.keys():
                        if (n_x, n_y) == coord:
                            test = True
                            ship[n_x, n_y] = "-"
                            break

                else: break

            if test:
                self.field_coord[n_x, n_y] = "X"

                self.field.create_rectangle(x + 5, y + 5, x + self.step_x - 5, y + self.step_y - 5, fill="red",
                                            tags=["X"])

                self.field.create_line(x + 5, y + 5, x + self.step_x - 5, y + self.step_y - 5,
                                       fill="black", tags=["X"])

                self.field.create_line(x + self.step_x - 5,
                                       y + 5,
                                       x + 5,
                                       y + self.step_y - 5,
                                       fill="black", tags=["X"])

                ship_destroyed = self.check_ship_destroyed()

                if ship_destroyed:
                    self.outline_destroyed_ship(ship_destroyed)
                    print("Корабль уничтожен")
                else:
                    print("Неа")


            elif not test:
                self.field_coord[n_x, n_y] = "0"

                self.field.create_oval(x + 3 * self.step_x // 8,
                                       y + 3 * self.step_y // 8,
                                       x + 3 * self.step_x // 8 + self.step_x // 4,
                                       y + 3 * self.step_y // 8 + self.step_y // 4,
                                       fill="red", tags=["X"])
                self.stroke_transition()




        # self.update_fild()


    # def update_fild(self):
    #     self.field.delete("X")
    #     for coord in self.field_coord:
    #         n_x = coord[0] * self.step_x
    #         n_y = coord[1] * self.step_y
    #         if self.field_coord[coord] == "X":
    #
    #             self.field.create_rectangle(n_x + 5, n_y + 5, n_x + self.step_x - 5, n_y + self.step_y - 5, fill="red", tags=["X"])
    #
    #             self.field.create_line(n_x + 5, n_y + 5, n_x + self.step_x - 5, n_y + self.step_y - 5,
    #                                    fill="black", tags=["X"])
    #
    #             self.field.create_line(n_x + self.step_x - 5,
    #                                    n_y + 5,
    #                                    n_x + 5,
    #                                    n_y + self.step_y - 5,
    #                                    fill="black", tags=["X"])
    #
    #         elif self.field_coord[coord] == "0":
    #             self.field.create_oval(n_x + 3 * self.step_x // 8,
    #                                    n_y + 3 * self.step_y // 8,
    #                                    n_x + 3 * self.step_x // 8 + self.step_x // 4,
    #                                    n_y + 3 * self.step_y // 8 + self.step_y // 4,
    #                                    fill="red", tags=["X"])


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
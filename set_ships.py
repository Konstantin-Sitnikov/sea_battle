import tkinter as tk

class SetShips(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.wm_attributes("-topmost", 1)

        label = tk.Label(self, text="Добро пожаловать в игру морской бой")
        label.grid(row=1, column=0, columnspan=3, sticky="n")
        container = tk.Frame(self, height=500, width=500)
        container.grid(row=2, column=0, columnspan=3, sticky="n")


        self.ships = {
                        "Однопалубный_1": {(0, 0): "+"},
                      "Однопалубный_2": {(5, 7): "+"},
                      "Однопалубный_3": {(8, 1): "+"},
                      "Однопалубный_4": {(9, 9): "+"},
                      "Двухпалубный_1": {(2, 3): "+", (3, 3): "+"},
                      "Двухпалубный_2": {(5, 1): "+", (6, 1): "+"},
                      "Двухпалубный_3": {(5, 1): "+", (6, 1): "+"},
                      "Трехпалубный_1": {(4, 1): "+", (5, 1): "+", (6, 1): "+"},
                      "Трехпалубный_2": {(4, 1): "+", (5, 1): "+", (6, 1): "+"},
                      "Четырехпалубный": {(4, 1): "+", (5, 1): "+", (6, 1): "+", (6, 2): "+"},
                      }

        self.field_coord = self.coord_fild()

        for ship, coord in self.ships.items():
            frame = Ship(container, self, type=ship)
            frame.grid(row=3, column=0, sticky="nsew")
            frame.wait_window()
            s = frame.get_ship()
            self.ships[ship] = s
            print(self.ships)



        tk.Button(self, text="Готово", command=self.destroy).grid(row=10, column=0, columnspan=3, sticky="n")

    def coord_fild(self):
        fild = {}
        for x in range(10):
            for y in range(10):
                fild[x, y] = '-'
        return fild

    def open(self):
        self.grab_set()
        self.wait_window()
        return self.ships


class Ship(tk.Frame):
    def __init__(self, parent, controller, type):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.type = type

        self.ship = {}

        self.canvas_x = 400
        self.canvas_y = 400
        self.n_x = self.n_y = 10  # количество ячеек
        self.step_x = self.canvas_x // self.n_x
        self.step_y = self.canvas_y // self.n_y

        self.field = self.field_creation(row=2, col=0)
        self.field_coord = self.controller.field_coord
        self.field.bind("<Button-1>", self.set_coordinates)
        self.update_fild()

        tk.Button(self, text="Закончить ввод", command=self.destroy).grid(row=10, column=0, columnspan=3, sticky="n")


    def get_ship(self):
        return self.ship

    def set_coordinates(self, event):
        print("Длинна корабля",len(self.ship))
        print("нужная линна корабля", len(self.controller.ships[self.type]))


        if len(self.ship) != len(self.controller.ships[self.type]):
            x = event.x // self.step_x
            y = event.y // self.step_y
            self.ship[x, y] = "+"
            print(self.ship)
            self.field_coord[x, y] = "X"
            self.update_fild()


    def update_fild(self):

        for coord in self.field_coord:
            n_x = coord[0] * self.step_x
            n_y = coord[1] * self.step_y
            if self.field_coord[coord] == "X":

                self.field.create_rectangle(n_x + 5, n_y + 5, n_x + self.step_x - 5, n_y + self.step_y - 5, fill="green", tags=["X"])


            elif self.field_coord[coord] == "0":
                self.field.create_line(n_x + 5, n_y + 5, n_x + self.step_x - 5, n_y + self.step_y - 5,
                                       fill="black", tags=["X"])

                self.field.create_line(n_x + self.step_x - 5,
                                       n_y + 5,
                                       n_x + 5,
                                       n_y + self.step_y - 5,
                                       fill="black", tags=["X"])







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





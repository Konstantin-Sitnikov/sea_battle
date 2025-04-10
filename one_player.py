import tkinter as tk


class OnePlayer(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)

        self.wm_attributes("-topmost", 1)

        canvas = tk.Canvas(self, bg = "white", width=800, height=400)
        canvas.pack()

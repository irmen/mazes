import tkinter


class GuiWindow(tkinter.Tk):
    SCALE = 12

    def __init__(self, columns, rows):
        super().__init__()
        self.title("maze")
        self.geometry("{}x{}".format(columns*self.SCALE+self.SCALE, rows*self.SCALE+self.SCALE))
        self.canvas = tkinter.Canvas(self, bg='light gray')
        self.canvas.pack(fill=tkinter.BOTH, expand=True, padx=4, pady=4)

    def line(self, x1, y1, x2, y2):
        self.canvas.create_line(1+x1*self.SCALE, 1+y1*self.SCALE, 1+x2*self.SCALE, 1+y2*self.SCALE)

    def clear(self):
        self.canvas.delete(tkinter.ALL)

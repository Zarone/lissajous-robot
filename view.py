import tkinter as tk

class View(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        
        self.build_gui()

    def build_gui(self):
        left_frame = tk.Frame(self)
        left_frame.pack(side=tk.LEFT)
        
        right_frame = tk.Frame(self)
        right_frame.pack(side=tk.RIGHT)

        self.C = tk.Canvas(right_frame,bg="Red",height=500, width=500)
        self.C.pack()

        self.lblr1 = tk.Label(left_frame,text='r1')
        self.lblr1.pack(fill=tk.X)   
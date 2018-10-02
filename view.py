import tkinter as tk
from controller import Controller

class View(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()

        self.controller = Controller()

        self.build_gui()

    def build_gui(self):
        right_frame = tk.Frame(self)
        right_frame.pack(side=tk.RIGHT)

        self.canvas = tk.Canvas(right_frame, height=500, width=500)
        self.canvas.pack()

        left_frame = tk.Frame(self)
        left_frame.pack(side=tk.LEFT)

        #Start button
        start = tk.Button(left_frame, text="Start", command=self.start)
        start.grid(row=0, column=0, sticky=tk.N+tk.S+tk.W+tk.E)

        #Stop button
        stop = tk.Button(left_frame, text="Stop", command=self.stop)
        stop.grid(row=0, column=1, sticky=tk.N+tk.S+tk.W+tk.E)

        #Radius set 1
        self.radius1 = tk.Scale(left_frame, from_=100, to=250, resolution=10, command=self.redraw_curve, orient=tk.HORIZONTAL, label="Radius 1")
        self.radius1.grid(row=1, column=0, columnspan=2, sticky=tk.N+tk.S+tk.W+tk.E)

        #Raduis set 2 
        self.radius2 = tk.Scale(left_frame, from_=100, to=250, resolution=10, command=self.redraw_curve, orient=tk.HORIZONTAL, label="Radius 2")
        self.radius2.grid(row=2, column=0, columnspan=2, sticky=tk.N+tk.S+tk.W+tk.E)

        #Omega set 1 
        self.omega1 = tk.Scale(left_frame, from_=2.0, to=5.0, resolution=0.20, command=self.redraw_curve, orient=tk.HORIZONTAL, label="Omega 1")
        self.omega1.grid(row=3, column=0, columnspan=2, sticky=tk.N+tk.S+tk.W+tk.E)

        #Omega set 2
        self.omega2 = tk.Scale(left_frame, from_=2.0, to=5.0, resolution=0.20, command=self.redraw_curve, orient=tk.HORIZONTAL, label="Omega 2")
        self.omega2.grid(row=4, column=0, columnspan=2, sticky=tk.N+tk.S+tk.W+tk.E)

        #Phi
        self.phi = tk.Scale(left_frame, from_=0.0, to=3.0, resolution=0.20, command=self.redraw_curve, orient=tk.HORIZONTAL, label="Phi")
        self.phi.grid(row=5, column=0, columnspan=2, sticky=tk.N+tk.S+tk.W+tk.E)

        #Range
        rangeLbl = tk.Label(left_frame, text='Punkter')
        rangeLbl.grid(row=6, column=0, sticky=tk.N+tk.S+tk.W)

        self.range = tk.Spinbox(left_frame, from_=100, to=1000)
        self.range.grid(row=7, column=0, columnspan=2, sticky=tk.N+tk.S+tk.W+tk.E)

        #Step
        stepLbl = tk.Label(left_frame, text='Trin')
        stepLbl.grid(row=8, column=0, sticky=tk.N+tk.S+tk.W)

        self.step = tk.Spinbox(left_frame, from_=0.01, to=1)
        self.step.grid(row=9, column=0, columnspan=2, sticky=tk.N+tk.S+tk.W+tk.E)

    def redraw_curve(self, evt=None):
        r1 = self.radius1.get()
        r2 = self.radius2.get()
        w1 = self.omega1.get()
        w2 = self.omega2.get()
        p = self.phi.get()
        rang = self.range.get()
        step = self.step.get()

        try:
            rang = int(rang)
            step = float(step)
        except:
            return

        coordinates = self.controller.get_curve(r1, r2, w1, w2, p, rang, step)

        self.canvas.delete("all")

        for i in range(0, rang-1):
            coord1 = coordinates[i]
            x1 = coord1[0] + 250
            y1 = coord1[1] + 250

            coord2 = coordinates[i+1]
            x2 = coord2[0] + 250
            y2 = coord2[1] + 250

            self.canvas.create_line(x1, y1, x2, y2, fill="blue")

    def start(self):
        pass

    def stop(self):
        pass

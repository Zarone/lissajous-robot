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
        start = tk.Button(left_frame, text="Start", command=self.start_drawing)
        start.grid(row=0, column=0, sticky=tk.N+tk.S+tk.W+tk.E)

        #Stop button
        stop = tk.Button(left_frame, text="Stop", command=self.stop_drawing)
        stop.grid(row=0, column=1, sticky=tk.N+tk.S+tk.W+tk.E)

        #Radius set 1
        self.radius1 = tk.Scale(left_frame, from_=50, to=250, resolution=10, command=self.redraw_curve, orient=tk.HORIZONTAL, label="Radius 1")
        self.radius1.grid(row=1, column=0, columnspan=2, sticky=tk.N+tk.S+tk.W+tk.E)

        #Raduis set 2 
        self.radius2 = tk.Scale(left_frame, from_=50, to=250, resolution=10, command=self.redraw_curve, orient=tk.HORIZONTAL, label="Radius 2")
        self.radius2.grid(row=2, column=0, columnspan=2, sticky=tk.N+tk.S+tk.W+tk.E)

        #Omega set 1
        self.omega1 = tk.Scale(left_frame, from_=0, to=1.0, resolution=0.05, command=self.redraw_curve, orient=tk.HORIZONTAL, label="Omega 1")
        self.omega1.grid(row=3, column=0, columnspan=2, sticky=tk.N+tk.S+tk.W+tk.E)

        #Omega set 2
        self.omega2 = tk.Scale(left_frame, from_=0, to=1, resolution=0.05, command=self.redraw_curve, orient=tk.HORIZONTAL, label="Omega 2")
        self.omega2.grid(row=4, column=0, columnspan=2, sticky=tk.N+tk.S+tk.W+tk.E)

        #Phi
        self.phi = tk.Scale(left_frame, from_=-7.0, to=7.0, resolution=0.01, command=self.redraw_curve, orient=tk.HORIZONTAL, label="Phi")
        self.phi.grid(row=5, column=0, columnspan=2, sticky=tk.N+tk.S+tk.W+tk.E)

        self.points = tk.Scale(left_frame, from_=100, to=1000, command=self.redraw_curve, orient=tk.HORIZONTAL, label="Antal af punkter")
        self.points.grid(row=7, column=0, columnspan=2, sticky=tk.N+tk.S+tk.W+tk.E)

    def redraw_curve(self, evt=None):
        r1 = self.radius1.get()
        r2 = self.radius2.get()
        w1 = self.omega1.get()
        w2 = self.omega2.get()
        p = self.phi.get()
        points = self.points.get()

        try:
            points = int(points)
        except ValueError:
            return

        coordinates = self.controller.get_curve(r1, r2, w1, w2, p, points)

        self.canvas.delete("all")

        for i in range(0, points-1):
            coord1 = coordinates[i]
            x0, y0 = coord1

            coord2 = coordinates[i+1]
            x1, y1 = coord2

            # Ligger 250 til for at centrerer det i billedet
            self.canvas.create_line(x0 + 250, y0 + 250, x1 + 250, y1 + 250, fill="blue")

    def start_drawing(self):
        pass

    def stop_drawing(self):
        pass

import tkinter as tk
from robot import Data, Programmer
from curve import Curve

class View(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()

        self.confirmation_window = None

        ip = '10.130.58.13'

        self.data = Data()
        self.programmer = Programmer()

        self.data.connect(ip)
        self.programmer.connect(ip)

        self.build_gui()

    def build_gui(self):
        right_frame = tk.Frame(self)
        right_frame.pack(side=tk.RIGHT)

        self.canvas = tk.Canvas(right_frame, height=500, width=500)
        self.canvas.pack()

        left_frame = tk.Frame(self)
        left_frame.pack(side=tk.LEFT)

        #Start button
        start = tk.Button(left_frame, text="Tegn", command=self.start_drawing)
        start.grid(row=0, column=0, columnspan=2, sticky=tk.N+tk.S+tk.W+tk.E)

        #Radius set 1
        self.radius1 = tk.Scale(left_frame, from_=50, to=250, resolution=10, command=self.redraw_curve, orient=tk.HORIZONTAL, label="Radius 1")
        self.radius1.grid(row=1, column=0, columnspan=2, sticky=tk.N+tk.S+tk.W+tk.E)

        #Raduis set 2 
        self.radius2 = tk.Scale(left_frame, from_=50, to=250, resolution=10, command=self.redraw_curve, orient=tk.HORIZONTAL, label="Radius 2")
        self.radius2.grid(row=2, column=0, columnspan=2, sticky=tk.N+tk.S+tk.W+tk.E)

        #Omega set 1
        self.omega1 = tk.Scale(left_frame, from_=0.05, to=1, resolution=0.05, command=self.redraw_curve, orient=tk.HORIZONTAL, label="Omega 1")
        self.omega1.grid(row=3, column=0, columnspan=2, sticky=tk.N+tk.S+tk.W+tk.E)

        #Omega set 2
        self.omega2 = tk.Scale(left_frame, from_=0.05, to=1, resolution=0.05, command=self.redraw_curve, orient=tk.HORIZONTAL, label="Omega 2")
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
        
        curve = Curve(r1, r2, w1, w2, p, points)

        self.canvas.delete("all")

        for i in range(0, points-1):
            coord0 = curve.coordinates[i]
            x0, y0 = coord0

            coord1 = curve.coordinates[i+1]
            x1, y1 = coord1

            # Ligger 250 til for at centrerer det i billedet
            self.canvas.create_line(x0 + 250, y0 + 250, x1 + 250, y1 + 250, fill="blue")

    def start_drawing(self):
        if self.confirmation_window is not None:
            return

        def confirm():
            start_button.destroy()
            abort_button.config(text="Afbryd")
            information_label.config(text="Starter robotten...\nTryk på afbryd for at stoppe den igen.")

            #Start robotten

            self.programmer.move_curve(curve.coordinates)

        def abort():
            close()

        def close():
            dlg.destroy()
            self.confirmation_window = None

            self.programmer.move_home()

        dlg = tk.Toplevel(height=200, width=200)
        dlg.protocol("WM_DELETE_WINDOW", close)
        dlg.bind('<Escape>', lambda e: close())

        self.confirmation_window = dlg

        r1 = self.radius1.get()
        r2 = self.radius2.get()
        w1 = self.omega1.get()
        w2 = self.omega2.get()
        p = self.phi.get()
        points = self.points.get()

        # Beregn koordinaterne til kurven
        curve = Curve(r1, r2, w1, w2, p, points)
        # Beregn længden af kurven (i millimeter)
        curve.calc_length()

        # Beregn den estimerede tid til at tegne kurven
        print_time = curve.estimate_print_time()

        msg = "Det vil tage"
        if print_time < 1:
            msg += " mindre end 1 sekund"
        else:
            msg += " omkring " + str(round(print_time)) + " sekunder"
        msg += " at lave tegningen.\nEr du sikker på at du vil lave tegningen?"

        information_label = tk.Label(dlg, text=msg)
        information_label.pack(side=tk.TOP)

        start_button = tk.Button(dlg, text="Ja", command=confirm)
        start_button.pack(side=tk.LEFT)

        abort_button = tk.Button(dlg, text="Nej", command=abort)
        abort_button.pack(side=tk.RIGHT)

        dlg.mainloop()

    def close_confirmation_window(self):
        if self.confirmation_window is None:
            self.confirmation_window.destroy()
            self.confirmation_window = None

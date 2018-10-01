import tkinter as tk

class View(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()

        self.build_gui()

    def build_gui(self):
        right_frame = tk.Frame(self)
        right_frame.pack(side=tk.RIGHT)

        self.C = tk.Canvas(right_frame, bg='Red', height=500, width=500)
        self.C.pack()

        left_frame = tk.Frame(self)
        left_frame.pack(side=tk.LEFT)

        #Start button
        self.B1 = tk.Button(left_frame, text="Start", command=self.start)
        self.B1.grid(row=0, column=0, sticky=tk.N+tk.S+tk.W+tk.E)

        self.B2 = tk.Button(left_frame, text="Stop", command=self.stop)
        self.B2.grid(row=0, column=1, sticky=tk.N+tk.S+tk.W+tk.E)
        #Radius set 1
        self.R1 = tk.Scale(left_frame, from_=0.0, to=3.0, resolution=0.20, orient=tk.HORIZONTAL, label="Radius 1")
        self.R1.grid(row=1, column=0, columnspan=2, sticky=tk.N+tk.S+tk.W+tk.E)

        #Raduis set 2 
        self.R2 = tk.Scale(left_frame, from_=0.0, to=3.0, resolution=0.20, orient=tk.HORIZONTAL, label="Radius 2")
        self.R2.grid(row=2, column=0, columnspan=2, sticky=tk.N+tk.S+tk.W+tk.E)

        #Omega set 1 
        self.V1 = tk.Scale(left_frame, from_=0.0, to=3.0, resolution=0.20, orient=tk.HORIZONTAL, label="Omega 1")
        self.V1.grid(row=3, column=0, columnspan=2, sticky=tk.N+tk.S+tk.W+tk.E)

        #Omega set 2
        self.W2 = tk.Scale(left_frame, from_=0.0, to=3.0, resolution=0.20, orient=tk.HORIZONTAL, label="Omega 2")
        self.W2.grid(row=4, column=0, columnspan=2, sticky=tk.N+tk.S+tk.W+tk.E)

        #Phi
        self.P2 = tk.Scale(left_frame, from_=0.0, to=3.0, resolution=0.20, orient=tk.HORIZONTAL, label="Phi")
        self.P2.grid(row=5, column=0, columnspan=2, sticky=tk.N+tk.S+tk.W+tk.E)

        #Range(t)
        self.lblR = tk.Label(left_frame, text='Range(t)')
        self.lblR.grid(row=6, column=0, sticky=tk.N+tk.S+tk.W)

        self.Box = tk.Spinbox(left_frame, from_=0, to=10000)
        self.Box.grid(row=7, column=0, columnspan=2, sticky=tk.N+tk.S+tk.W+tk.E)

    def start(self):
        pass

    def stop(self):
        pass

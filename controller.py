from math import sin
from robot import Programmer, Data
class Controller():
    def __init__(self):
        ip = '10.130.58.13'
        self.data = Data()
        self.programmer = Programmer()

        self.offset = (-0.4, -0.4)
        self.draw_height = 0.063

        self.data.connect(ip)
        self.programmer.connect(ip)

    def get_curve(self, r1, r2, w1, w2, phi, points):
        xy = []
        for t in range(points):
            t *= 0.1
            x = r1 * sin(w1*t+phi)
            y = r2 * sin(w2*t)
            xy.append((x, y))
        return xy

    def start_moving(self, xy):
        self.programmer.move_curve(xy, self.offset, self.draw_height)
    
    def stop_moving(self):
        self.programmer.move_home()
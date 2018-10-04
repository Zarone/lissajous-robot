from math import sin

class Controller():
    def __init__(self):
        pass

    def get_curve(self, r1, r2, w1, w2, phi, points):
        xy = []
        for t in range(points):
            t *= 0.1
            x = r1 * sin(w1*t+phi)
            y = r2 * sin(w2*t)
            xy.append((x, y))
        return xy

from math import sin

class Controller():
    def __init__(self):
        pass
    
    def get_curve(self, r1, r2, w1, w2, phi, rang, step):
        xy = []
        for t in range(rang):
            x = r1 * sin(w1*t*step)
            y = r2 * sin(w2*t*step) + phi
            xy.append((x, y))
        return xy
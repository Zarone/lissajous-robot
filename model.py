from math import sin

class Model():
    def __init__(self):
        pass
    
    def get_curve(self, r1, r2, w1, w2, phi, rang=1000):
        xy = []
        for t in range(rang):
            x = r1 * sin(w1*float(t)/1000)
            y = r2 * sin(w2 * float(t)/1000) + phi
            xy.append((x, y))
        return xy        
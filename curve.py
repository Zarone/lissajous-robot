import math as math

class Curve():
    def __init__(self, r1, r2, w1, w2, phi, points):
        self.r1 = r1
        self.r2 = r2
        self.w1 = w1
        self.w2 = w2
        self.phi = phi
        self.num_points = points

        self.created = False
        self.coordinates = None
        self.length = None

        self.create()

    def create(self):
        coordinates = []

        for t in range(self.num_points):
            t *= 0.1
            x = self.r1 * math.sin(self.w1*t+self.phi)
            y = self.r2 * math.sin(self.w2*t)
            coordinates.append((x, y, t))

        self.coordinates = coordinates
        self.created = True

        return coordinates

    def calc_length(self):
        # Længden er i millimeter
        if self.created is False:
            return
        
        if (self.num_points < 2):
            return

        total = 0.0
        for i in range(0, self.num_points-1):
            x0, y0, t0 = self.coordinates[i]
            x1, y1, t1 = self.coordinates[i+1]

            total += math.sqrt(math.pow(x1 - x0, 2) + math.pow(y1 - y0, 2))

        self.length = total
        return total

    def estimate_print_time(self):
        if self.length is not None:
            # Fået hastigheden ved at få robotten til at tegne en kurve som
            # var 2360 mm lang, det tog 44 sekunder (2360mm / 44s = 53mm/s)
            velocity = 53.6363636

            time = self.length / velocity
            return time

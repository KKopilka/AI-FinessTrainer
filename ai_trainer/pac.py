import numpy as np

class PointAccumulator:
    
    def __init__(self, amount, check=True, divAmount = True, cylcing = True):
        self.amount = amount
        self.seria = []
        self.check = check
        self.divAmount = divAmount
        self.cycling = cylcing

    def reset(self):
        self.seria = []

    def store(self, point):
        if self.check:
            if not np.array(point).any():
                return
            if point[0] == 0 and point[1] == 0:
                return
        
        if not self.filled():
            self.seria.append(point)
        else:
            if self.cycling:
                del self.seria[0]
                self.seria.append(point)


    def filled(self):
        return len(self.seria) >= self.amount

    def val(self):
        val = np.array(self.seria)
        val = val.sum(axis=0)
        if self.divAmount:
            val = val/self.amount
        else:
            l = len(self.seria)
            if l != 0:
                val = val/l
            else:
                val = None

        return val
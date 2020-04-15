import math


# suitable for coordinate system like below:
#  -----------------> x
#  |
#  |
#  |
#  |
#  |
#  ↓ y

class Point(object):
    def __init__(self, xParam=0.0, yParam=0.0):
        self.x = xParam
        self.y = yParam

    def __str__(self):
        return "(%.2f, %.2f)" % (self.x, self.y)

    def move(self, act="stay"):
        if act == 'rightup':
            return Point(self.x - 1, self.y + 1)
        elif act == 'up':
            return Point(self.x - 1, self.y)
        elif act == 'leftup':
            return Point(self.x - 1, self.y - 1)
        elif act == 'left':
            return Point(self.x, self.y - 1)
        elif act == 'leftdown':
            return Point(self.x + 1, self.y - 1)
        elif act == 'down':
            return Point(self.x + 1, self.y)
        elif act == 'rightdown':
            return Point(self.x + 1, self.y + 1)
        elif act == 'right':
            return Point(self.x, self.y + 1)
        else:
            return Point(self.x, self.y)

    def override(self, x, y):
        if 0 <= self.x <= x - 1 and 0 <= self.y <= y - 1:
            return False
        return True

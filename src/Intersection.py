class Intersection:

    def __init__(self, x, y, real_x, real_y):
        self.x_ = x
        self.y_ = y
        self.realX_ = real_x
        self.realY = real_y

    def get_x(self):
        return self.x_

    def get_y(self):
        return self.y_

    def coords_equal(self, x, y):
        if self.x_ == x and self.y_ == y:
            return True
        else:
            return False

    def coords_close(self, x, y):
        area = 4
        if (self.x_ - area) <= x <= (self.x_ + area) and (self.y_ - area) <= y <= (self.y_ + area):
            return True
        # for o in range(-2, 3):
        #     for o2 in range(-2, 3):
        #         if self.x_ == x+o and self.y_ == y+o2:
        #             return True
        return False

    def to_string(self):
        return "(x = " + str(self.x_) + ", y = " + str(self.y_) + ")"

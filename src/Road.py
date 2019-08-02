class Road:

    def __init__(self, int1, int2, through=None):
        if through is None:
            through = []
        self.int1_ = int1
        self.int2_ = int2
        self.connection_details_ = through
        self.connection_flag_ = None
        self.traffic_ = None

    def get_int1(self):
        return self.int1_

    def get_int2(self):
        return self.int2_

    def set_connection_flag(self, flag):
        self.connection_flag_ = flag

    def set_traffic(self, point):
        self.traffic_ = point.get_traffic()

    def to_string(self):
        return "x: ", self.int1_, " y: ", self.int2_

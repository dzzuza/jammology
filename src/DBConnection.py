import MySQLdb
from src import MeasuringPoint
from src import TrafficCounter


class DBConnection:

    def __init__(self):
        self.db = MySQLdb.connect(host="mysql.agh.edu.pl",
                                  user="zadworny",
                                  passwd="zadworny",
                                  db="zadworny")

    def read_data(self):
        tc = TrafficCounter.TrafficCounter()
        cur = self.db.cursor()
        cur.execute("select time, val_1, val_4 from car_data where location_id = 7 and lane = 'total'")
        id7 = cur.fetchall()
        dict = {}
        for row in id7:
            traffic = tc.calculate_traffic(row[1], row[2])
            dict[str(row[0])] = traffic
        cur.execute("select lat, lng from locations where id = 7")
        lat, lng = cur.fetchone()
        point1 = MeasuringPoint.MeasuringPoint(7, dict, lat, lng)

        cur.execute("select time, val_1, val_4 from car_data where location_id = 21 and lane = 'total'")
        id21 = cur.fetchall()
        for row in id21:
            traffic = tc.calculate_traffic(row[1], row[2])
            dict[str(row[0])] = traffic
        cur.execute("select lat, lng from locations where id = 21")
        lat, lng = cur.fetchone()
        point2 = MeasuringPoint.MeasuringPoint(21, dict, lat, lng)

        cur.close()
        self.db.close()
        return point1, point2


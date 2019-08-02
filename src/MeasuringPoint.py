import geopy.distance
import math

from src.Traffic import Traffic


class MeasuringPoint:

    def __init__(self, id, data, lat, lng):
        self.traffic_ = None
        self.id_ = id
        self.data_ = data
        self.lat_ = lat
        self.lng_ = lng
        self.x_ = None
        self.y_ = None
        self.date_ = '2019-01-01'

    def get_x(self):
        return self.x_

    def get_y(self):
        return self.y_

    def set_map_coordinates(self, start_lat, start_lng, scale,dpi):
        distance_lat = self.get_real_distance(start_lat, start_lng,self.lat_, start_lng)*100
        distance_lng = self.get_real_distance(start_lat, start_lng,start_lat, self.lng_)*100
        self.x_ = math.floor(dpi*distance_lat*scale)
        self.y_ = math.floor(dpi*distance_lng*scale)
        print(self.x_, self.y_)

    def to_string(self):
        return "id: {} \n lat: {} \n lng: {} \n data: {}".format(self.id_, self.lat_, self.lng_,
                                                                 self.data_['2019-01-01 15:40:00'])

    @staticmethod
    def get_real_distance(start_lat, start_lng, end_lat, end_lng):
        coords_a = (start_lat, start_lng)
        coords_b = (end_lat, end_lng)
        real_distance = geopy.distance.vincenty(coords_a, coords_b).m
        return real_distance

    def increase_date(self):
        day = int(self.date_.split('-')[2])
        if day < 5:
            day += 1
            self.date_ = self.date_[:-2] + '0' + str(day)

    def decrease_date(self):
        day = int(self.date_.split('-')[2])
        if day > 1:
            day -= 1
            self.date_ = self.date_[:-2] + '0' + str(day)

    def get_traffic(self, day_time):
        date = self.date_
        if day_time == 'Morning':
            date += ' 08:00:00'
        elif day_time == 'Afternoon':
            date += ' 13:00:00'
        elif day_time == 'Evening':
            date += ' 18:00:00'
        value = self.data_[date]
        if value < 4:
            self.traffic_ = Traffic(0)
        elif value < 7:
            self.traffic_ = Traffic(4)
        elif value < 18:
            self.traffic_ = Traffic(7)
        return self.traffic_, value

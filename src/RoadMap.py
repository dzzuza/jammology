from __future__ import division
from src import Intersection
from src import Road
import math
from skimage import io
from skimage.morphology import skeletonize
from skimage.util import invert
from PIL import Image
import geopy.distance


class RoadMap:

    def __init__(self):
        self.intersections_ = []
        self.roads_ = []
        self.data_points_ = []
        self.connectors_ = []
        self.img_skeleton_ = None
        self.img_ = None

    def add_intersection(self, intrsc):
        if intrsc not in self.intersections_:
            self.intersections_.append(intrsc)

    def add_data_point(self, data):
        self.data_points_.append(data)

    def add_road(self, road):
        self.roads_.append(road)
        if road.int1_ not in self.intersections_:
            self.add_intersection(road.int1_)
        if road.int2_ not in self.intersections_:
            self.add_intersection(road.int2_)

    def add_connector(self, connector):
        self.connectors_.append(connector)

    def get_morning_data(self):
        for p in self.data_points_:
            print('Morning: ' + str(p.get_traffic('Morning')))

    def get_afternoon_data(self):
        for p in self.data_points_:
            print('Afternoon: ' + str(p.get_traffic('Afternoon')))

    def get_evening_data(self):
        for p in self.data_points_:
            print('Evening: ' + str(p.get_traffic('Evening')))

    def previous_day(self, time):
        for p in self.data_points_:
            p.decrease_date()
            tr, val = p.get_traffic(time)
            print(time + ': ' + str(tr) + ' : ' + str(val))
        print('(previous_day called) Current day: ' + self.data_points_[0].date_)

    def next_day(self, time):
        for p in self.data_points_:
            p.increase_date()
            tr, val = p.get_traffic(time)
            print(time + ': ' + str(tr) + ' : ' + str(val))
        print('(next_day called) Current day: ' + self.data_points_[0].date_)

    @staticmethod
    def get_real_map_coordinates(image_x, image_y, start_lat, start_lng, scale):
        coord_x_ = start_lat - image_x * scale
        coord_y_ = start_lng + image_y * scale
        return coord_x_, coord_y_

    @staticmethod
    def get_real_distance_in_meters(start_lat, start_lng, end_lat, end_lng):
        coords_a = (start_lat, start_lng)
        coords_b = (end_lat, end_lng)
        real_distance = geopy.distance.vincenty(coords_a, coords_b).m
        return real_distance

    @staticmethod
    def get_map_distance_in_meters(image, dpi):
        map_image = Image.open(image)
        width, height = map_image.size
        width, height = width / dpi, height / dpi
        map_dist = math.sqrt(width * width + height * height)/100  # meters
        return map_dist

    def get_scale(self, image, dpi, start_lat, start_lng, end_lat, end_lng):
        map_distance = self.get_map_distance_in_meters(image, dpi)
        real_distance = self.get_real_distance_in_meters(start_lat, start_lng, end_lat, end_lng)
        scale = map_distance / real_distance
        print("scale", scale)
        return scale

    def find_closest_road(self, data_point):
        x = data_point.get_x()
        y = data_point.get_y()
        mm = self.find_edges()
        state = 0
        o = 1
        xo = 0
        yo = 0
        if mm[1][0] > mm[1][1]:
            max = mm[1][0]
        else:
            max = mm[1][1]

        # spiralne szukanie najbliższego białego piksela
        potential = []
        while o < max:
            if state == 0:
                yo += 1
                if yo == o:
                    state += 1
            elif state == 1:
                xo += 1
                if xo == o:
                    state += 1
            elif state == 2:
                yo -= 1
                if yo == -o:
                    state += 1
            elif state == 3:
                xo -= 1
                if xo == -o:
                    o += 1
                    state = 0

            if 0 <= x+xo < len(self.img_skeleton_) and 0 <= y+yo < len(self.img_skeleton_[0]) \
                    and self.img_skeleton_[x + xo][y + yo]:
                potential.append([x+xo, y+yo])
                break

        # szukanie najbliższych skrzyżowań podążając za białymi pikselami
        checked = []
        closest_intersections = []
        # p = potential[0]
        # for o in range(-1, 2):
        #     for o2 in range(-1, 2):
        #         if 0 <= p[0] + o < len(self.img_skeleton_) and 0 <= p[1] + o2 < len(self.img_skeleton_[0]) \
        #                 and self.img_skeleton_[p[0]+o][p[1]+o2] \
        #                 and [x+o, y+o2] not in checked:
        #             potential.append([p[0] + o, p[1] + o2])
        while len(closest_intersections) < 2 and len(potential) > 0:
            for p in potential:
                potential.remove(p)
                checked.append(p)
                found = False
                for i in self.intersections_:
                    if i.coords_equal(p[0], p[1]):
                        closest_intersections.append(i)
                        for o in range(-1, 2):
                            for o2 in range(-1, 2):
                                if [p[0]+o, p[1]+o2] in potential:
                                    potential.remove([p[0]+o, p[1]+o2])
                                    checked.append([p[0]+o, p[1]+o2])
                        found = True
                        break
                if found:
                    continue
                for o in range(-1, 2):
                    for o2 in range(-1, 2):
                        if 0 <= p[0] + o < len(self.img_skeleton_) and 0 <= p[1] + o2 < len(self.img_skeleton_[0]) and \
                                self.img_skeleton_[p[0] + o][p[1] + o2] and \
                                [p[0] + o, p[1] + o2] not in checked:
                            potential.append([p[0] + o, p[1] + o2])

        if len(closest_intersections) == 2:
            for r in self.roads_:
                if r.get_int1() in closest_intersections and r.get_int2() in closest_intersections:
                    r.set_connection_flag(data_point)
                    return r
            print("Nie znaleziono połączenia pomiędzy skrzyżowaniami")
            for i in closest_intersections:
                print(i.to_string())
        elif len(closest_intersections) > 2:
            print("Znaleziono więcej niż dwa skrzyżowania (punkt prawdopodobnie znajduje się na skrzyżowaniu):")
            for i in closest_intersections:
                print(i.to_string())
        else:
            print("Nie znaleziono drogi w pobliżu (x = " + str(x) + ", y = " + str(y) + ")")

    def find_edges(self):
        min_x = 0
        min_y = 0
        max_x = 0
        max_y = 0
        for i in self.intersections_:
            if i.get_x() < min_x:
                min_x = i.get_x()
            elif i.get_x() > max_x:
                max_x = i.get_x()

            if i.get_y() < min_y:
                min_y = i.get_y()
            elif i.get_y() > max_y:
                max_y = i.get_y()
        return [[min_x, min_y], [max_x, max_y]]

    def load_from_image(self, image, dpi, start_lat, start_lng, end_lat, end_lng):
        self.img_ = image
        scale = self.get_scale(image, dpi, start_lat, start_lng, end_lat, end_lng)
        self.img_skeleton_ = self.inner_skeletonize(image)
        intrsc = self.find_intersections(self.img_skeleton_)
        #intrsc_obj = []
        for i in intrsc:
            lat, lng = self.get_real_map_coordinates(i[0], i[1], start_lat, start_lng, scale)
            new_intrsc = Intersection.Intersection(i[0], i[1], lat, lng)
            #intrsc_obj.append(new_intrsc)
            self.add_intersection(new_intrsc)
            # print("Co-ordX : ", lat, " Co-ordY : ", lng)

        for road in self.get_connections(self.img_skeleton_, self.intersections_):
            self.add_road(road)

    @staticmethod
    def inner_skeletonize(img):
        # Invert the image
        image = invert(io.imread(img, as_gray=True))
        image = image > 0
        # perform skeletonization
        skeleton = skeletonize(image)

        return skeleton

    @staticmethod
    def find_intersections(img):

        junctions = [
            [[True, False, True],
             [False, True, False],
             [False, True, False]],

            [[True, False, False],
             [False, True, True],
             [False, True, False]],

            [[True, False, False],
             [False, True, True],
             [True, False, False]],

            [[True, False, False],
             [False, True, False],
             [True, False, True]],

            [[True, False, True],
             [False, True, False],
             [True, False, False]],

            [[True, False, True],
             [False, True, False],
             [False, False, True]],

            [[False, True, False],
             [False, True, True],
             [True, False, False]],

            [[False, True, False],
             [False, True, False],
             [True, False, True]],

            [[False, True, False],
             [True, True, False],
             [False, False, True]],

            [[False, True, False],
             [False, True, True],
             [False, True, False]],

            [[False, True, False],
             [True, True, True],
             [False, False, False]],

            [[False, True, False],
             [True, True, False],
             [False, True, False]],

            [[False, False, True],
             [True, True, False],
             [False, False, True]],

            [[False, False, True],
             [True, True, False],
             [False, True, False]],

            [[False, False, True],
             [False, True, False],
             [True, False, True]],

            [[False, False, False],
             [True, True, True],
             [False, True, False]]
        ]

        intrsc = []

        for i in range(1, len(img) - 1):
            for j in range(1, len(img[0]) - 1):
                if img[i][j]:
                    # area = []
                    # for o in range(-1, 2):
                    #     area.append([])
                    #     for o2 in range(-1, 2):
                    #         area[o+1].append(img[i+o][j+o2])

                    for junct in junctions:
                        a = 0
                        for o in range(-1, 2):
                            for o2 in range(-1, 2):
                                if junct[1 + o][1 + o2] and junct[1 + o][1 + o2] == img[i + o][j + o2]:
                                    a += 1
                        if a == 4:
                            not_present = True
                            for o in range(-2, 3):
                                for o2 in range(-2, 3):
                                    if [i+o, j+o2] in intrsc:
                                        not_present = False
                                        break
                                if not not_present:
                                    break
                            if not_present:
                                intrsc.append([i, j])
                            break
        return intrsc

    @staticmethod
    def get_connections(img, intrsc):
        roads = []
        flags = []
        #checked = []
        for i in range(len(img)):
            flags.append([])
            for j in range(len(img[0])):
                flags[i].append(False)

        for i in intrsc:
            ix = i.get_x()
            iy = i.get_y()
            flags[ix][iy] = True
            #checked.append([ix, iy])
            out = RoadMap.find_closest_intersections([ix, iy], intrsc, img, flags)
            flags = out[1]
            for end in out[0]:
                roads.append(Road.Road(i, end))
        return roads

    @staticmethod
    def find_closest_intersections(start, intrsc, img, flags):
        ends = []

        ix = start[0]
        iy = start[1]
        potential = []
        for o in range(-1, 2):
            for o2 in range(-1, 2):
                if 0 <= ix + o < len(img) and 0 <= iy + o2 < len(img[0]) and img[ix + o][iy + o2] and \
                        not flags[ix + o][iy + o2]:
                    potential.append([ix + o, iy + o2])

        while len(potential) > 0:
            for p in potential:
                potential.remove(p)
                # checked.append(p)
                flags[p[0]][p[1]] = True
                found = False
                for i in intrsc:
                    if (not (i.coords_equal(ix, iy))) and (i not in ends) and i.coords_close(p[0], p[1]):
                        ends.append(i)
                        found = True
                        break
                if found:
                    continue

                for o in range(-1, 2):
                    for o2 in range(-1, 2):
                        if 0 <= p[0] + o < len(img) and 0 <= p[1] + o2 < len(img[0]) and img[p[0] + o][p[1] + o2] and \
                                not flags[p[0] + o][p[1] + o2]:
                            potential.append([p[0] + o, p[1] + o2])
            # for p in potential:
            #     potential.remove(p)
            #     flags[p[0]][p[1]] = True
            #     found = False
            #     for i in intrsc:
            #         if (not (i.coords_equal(ix, iy))) and i not in ends:
            #             if i.coords_close(p[0], p[1]):
            #                 ends.append(i)
            #                 found = True
            #                 break
            #     if found:
            #         continue
            #     for o in range(-1, 2):
            #         for o2 in range(-1, 2):
            #             if 0 <= p[0] + o < len(img) and 0 <= p[1] + o2 < len(img[0]) and img[p[0] + o][p[1] + o2] \
            #                     and not flags[p[0] + o][p[1] + o2]:
            #                 potential.append([p[0] + o, p[1] + o2])

        return [ends, flags]

from src.Traffic import Traffic
from tkinter import *
import math
import tkinter


class View(Tk):
    def __init__(self, map):
        Tk.__init__(self)
        self.map_ = map
        self.intersections_displayed_ = []
        self.roads_displayed_ = []
        mm = map.find_edges()
        canvas_width = 800
        canvas_height = 800
        self.x_offset_ = -mm[0][0]
        self.y_offset_ = -mm[0][1]
        self.scale_ = 1
        self.displayed_time = "Morning"
        x_size = mm[1][0] - mm[0][0]
        y_size = mm[1][1] - mm[0][1]
        if x_size > y_size:
            max = x_size
            self.scale_ = max / canvas_height
            self.y_offset_ += (x_size - y_size) / 2
        else:
            max = y_size
            self.scale_ = max / canvas_width
            self.x_offset_ += (y_size - x_size) / 2

        self.morning_button_ = Button(text="Morning", command=self.display_morning)
        # self.morning_button_.place(x=100, y=850)
        self.afternoon_button_ = Button(text="Afternoon", command=self.display_afternoon)
        # self.afternoon_button_.place(x=200, y=850)
        self.evening_button_ = Button(text="Evening", command=self.display_evening)
        # self.evening_button_.place(x=300, y=850)
        self.previous_day_button = Button(text="Previous Day", command=self.previous_day)
        # self.previous_day_button.place(x=400, y=850)
        self.next_day_button = Button(text="Next Day", command=self.next_day)
        # self.next_day_button.place(x=500, y=850)
        self.morning_button_.pack(padx=5, pady=5, side=RIGHT)
        self.afternoon_button_.pack(padx=5, pady=5, side=RIGHT)
        self.evening_button_.pack(padx=5, pady=5, side=RIGHT)
        self.previous_day_button.pack(padx=5, pady=5, side=RIGHT)
        self.next_day_button.pack(padx=5, pady=5, side=RIGHT)
        self.canvas_ = Canvas(width=canvas_width+150, height=canvas_height, bg="#AFEEEE")
        self.canvas_.pack()
        self.intrsc_size_ = 4
        self.road_thickness_ = 5
        self.connector_thickness_ = 6
        #
        # button_morning = self.canvas_.create_rectangle(850, 50,  950, 80, fill="grey40", outline="grey60")
        # button_morning_txt = self.canvas_.create_text(900, 65, text="Morning")
        # self.canvas_.tag_bind(button_morning, "<Button-1>", self.map_.get_morning_data)
        # self.canvas_.tag_bind(button_morning_txt, "<Button-1>", self.map_.get_morning_data)
        #
        # button_afternoon = self.canvas_.create_rectangle(850, 80,  950, 110, fill="grey40", outline="grey60")
        # button_afternoon_txt = self.canvas_.create_text(900, 95, text="Afternoon")
        # self.canvas_.tag_bind(button_afternoon, "<Button-1>", self.map_.get_afternoon_data)
        # self.canvas_.tag_bind(button_afternoon_txt, "<Button-1>", self.map_.get_afternoon_data)
        #
        # button_evening = self.canvas_.create_rectangle(850, 110,  950, 140, fill="grey40", outline="grey60")
        # button_evening_txt = self.canvas_.create_text(900, 125, text="Evening")
        # self.canvas_.tag_bind(button_evening, "<Button-1>", self.map_.get_evening_data)
        # self.canvas_.tag_bind(button_evening_txt, "<Button-1>", self.map_.get_evening_data)
        #
        # button_prev_day = self.canvas_.create_rectangle(850, 160,  950, 190, fill="grey40", outline="grey60")
        # button_prev_day_txt = self.canvas_.create_text(900, 175, text="Previous Day")
        # self.canvas_.tag_bind(button_prev_day, "<Button-1>", self.map_.previous_day)
        # self.canvas_.tag_bind(button_prev_day_txt, "<Button-1>", self.map_.previous_day)
        #
        # button_next_day = self.canvas_.create_rectangle(850, 190,  950, 220, fill="grey40", outline="grey60")
        # button_next_day_txt = self.canvas_.create_text(900, 205, text="Next Day")
        # self.canvas_.tag_bind(button_next_day, "<Button-1>", self.map_.next_day)
        # self.canvas_.tag_bind(button_next_day_txt, "<Button-1>", self.map_.next_day)

        self.draw_map()

    def display_morning(self):
        self.displayed_time = "Morning"
        self.update_roads()
        return self.map_.get_morning_data

    def display_afternoon(self):
        self.displayed_time = "Afternoon"
        self.update_roads()
        return self.map_.get_afternoon_data

    def display_evening(self):
        self.displayed_time = "Evening"
        self.update_roads()
        return self.map_.get_evening_data

    def clear_canvas(self):
        for i in self.intersections_displayed_:
            self.canvas_.delete(i)
        for i in self.roads_displayed_:
            self.canvas_.delete(i)

    def next_day(self):
        self.map_.next_day(self.displayed_time)
        self.update_roads()

    def previous_day(self):
        self.map_.previous_day(self.displayed_time)
        self.update_roads()

    def update_roads(self):
        for i in self.roads_displayed_:
            self.canvas_.delete(i)
        for r in self.map_.roads_:
            self.draw_road(r)

    def draw_map(self):
        for i in self.map_.intersections_:
            self.draw_intrsc(i, "gray", False)
        for r in self.map_.roads_:
            self.draw_road(r)
            # if r.connection_flag_ is not None:
            #     color = self.get_color(r)
            #     self.draw_road(r, color)
        for p in self.map_.data_points_:
            self.draw_intrsc(p, "red", True)
            print("Data point drawn")
        for r in self.map_.connectors_:
            self.draw_connectors(r)

    def get_color(self, road):
        if road.connection_flag_ is None:
            return "black"
        else:
            traffic, val = road.connection_flag_.get_traffic(self.displayed_time)
            if traffic is Traffic.free:
                return "green"
            elif traffic is Traffic.stable:
                return "yellow"
            else:
                return "black"

    @staticmethod
    def from_rgb(R, G, B):  # tłumaczenie koloru RGB na kolor dla tkinter
        return "#%02x%02x%02x" % (R, G, B)

    def draw_road(self, r):
        # if r.connection_flag_ is not None:
        #     color = "red"
        #     roadPlus = 4
        # else:
        #     roadPlus = 0
        self.roads_displayed_.append(self.canvas_.create_line((r.int1_.y_ + self.y_offset_) / self.scale_,
                                                              (r.int1_.x_ + self.x_offset_) / self.scale_,
                                                              [a for x in r.connection_details_ for a in x],
                                                              (r.int2_.y_ + self.y_offset_) / self.scale_,
                                                              (r.int2_.x_ + self.x_offset_) / self.scale_,
                                                              width=math.ceil(self.road_thickness_ / self.scale_),
                                                              smooth=True, fill=self.get_color(r)))

    def draw_connectors(self, r):
        self.roads_displayed_.append(self.canvas_.create_line((r.int1_.y_ + self.y_offset_) / self.scale_,
                                                              (r.int1_.x_ + self.x_offset_) / self.scale_,
                                                              [a for x in r.connection_details_ for a in x],
                                                              (r.int2_.y_ + self.y_offset_) / self.scale_,
                                                              (r.int2_.x_ + self.x_offset_) / self.scale_,
                                                              width=self.connector_thickness_, smooth=True, fill="red"))

    def draw_intrsc(self, intrsc, color, data_point):
        if data_point:
            print("Skala: " + str(self.scale_) + "\n(x, y) = (" + str(intrsc.y_ / self.scale_) +
                  ", " + str(intrsc.x_ / self.scale_) + ")")
            # self.roads_displayed_.append(self.canvas_.create_line(300, 300, (intrsc.y_ / self.scale_),
            #                                                       (intrsc.x_ / self.scale_), width=3, fill="blue"))
        # else:
        #     intrsc_size = self.intrsc_size_
        self.intersections_displayed_ \
            .append(self.canvas_.
                    create_oval((intrsc.y_ + self.y_offset_) / self.scale_ - math.ceil(self.intrsc_size_ / self.scale_),
                                (intrsc.x_ + self.x_offset_) / self.scale_ - math.ceil(self.intrsc_size_ / self.scale_),
                                (intrsc.y_ + self.y_offset_) / self.scale_ + math.ceil(self.intrsc_size_ / self.scale_),
                                (intrsc.x_ + self.x_offset_) / self.scale_ + math.ceil(self.intrsc_size_ / self.scale_),
                                fill=color))


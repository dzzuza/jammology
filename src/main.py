from src import View
from src import RoadMap
from src import DBConnection

rMap = RoadMap.RoadMap()
db = DBConnection.DBConnection()
# map data:
start_lat, start_lng = 50.0698, 19.9487
end_lat, end_lng = 50.0260, 20.0136
image_dpi = 59.05  # dpi in pix/cm
mapImage = 'M2.png'
scale = rMap.get_scale(mapImage, image_dpi, start_lat, start_lng, end_lat, end_lng)

# data points
point_7, point_21 = db.read_data()
point_7.set_map_coordinates(start_lat, start_lng, scale, image_dpi)
point_21.set_map_coordinates(start_lat, start_lng, scale, image_dpi)

rMap.add_data_point(point_7)
rMap.add_data_point(point_21)

rMap.load_from_image(mapImage, image_dpi, start_lat, start_lng, end_lat, end_lng)

rMap.find_closest_road(point_7)
rMap.find_closest_road(point_21)
print(point_7.get_traffic('Morning'))
print(point_7.get_traffic('Afternoon'))
print(point_7.get_traffic('Evening'))


view = View.View(rMap)
view.mainloop()
print("Finished")





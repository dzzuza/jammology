class TrafficCounter:

    def calculate_traffic(self, density, average_speed):
        if density is not None and average_speed is not None and average_speed != 0:
            density_per_hour = self.count_density_per_hour(density)
            cars_per_km = density_per_hour / average_speed
            return cars_per_km
        elif density == 0:
            return 0
        else:
            return None

    @staticmethod
    def count_density_per_hour(density):
        density_per_hour = density * 6
        return density_per_hour



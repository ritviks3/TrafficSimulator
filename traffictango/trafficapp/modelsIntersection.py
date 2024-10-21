class Intersection:
    def __init__(self, name):
        self.name = name
        self.traffic_lights = []  # List of traffic lights at the intersection
        self.vehicles = []  # List to store vehicles at the intersection

    def add_traffic_light(self, traffic_light):
        #Add a traffic light to the intersection.
        self.traffic_lights.append(traffic_light)

    def remove_traffic_light(self, traffic_light):
        #Remove a traffic light from the intersection
        self.traffic_lights.remove(traffic_light)

    def add_vehicle(self, vehicle):
        #Add a vehicle to the intersection
        self.vehicles.append(vehicle)

    def remove_vehicle(self, vehicle):
        #Remove a vehicle from the intersection
        self.vehicles.remove(vehicle)

    def update_traffic_lights(self):
        #Update the state of traffic lights at the intersection
        for traffic_light in self.traffic_lights:
            traffic_light.update()

    def handle_vehicles(self):
        #Handle the movement of vehicles at the intersection
        for vehicle in self.vehicles:
            if vehicle.can_move():
                vehicle.move()
            else:
                vehicle.stop()
                
    def set_entry_lane(self, traffic_light_name, entry_lane_state):
        #Set the state of the entry lane traffic light
        for traffic_light in self.traffic_lights:
            if traffic_light.name == traffic_light_name:
                traffic_light.change_state(entry_lane_state)

    def set_exit_lane(self, traffic_light_name, exit_lane_state):
        #Set the state of the exit lane traffic light
        for traffic_light in self.traffic_lights:
            if traffic_light.name == traffic_light_name:
                traffic_light.change_state(exit_lane_state)

    def simulate(self, num_iterations):
        #Simulate traffic at the intersection for a given number of iterations.
        for _ in range(num_iterations):
            self.update_traffic_lights()
            self.handle_vehicles()

    def __str__(self):
        return f"Intersection {self.name}: {len(self.vehicles)} vehicles, {len(self.traffic_lights)} traffic lights"

class Roundabout(Intersection):
    def __init__(self, name):
        super().__init__(name)
        self.roundabout_vehicles = []  # List to store vehicles within the roundabout

    def __str__(self):
        return f"Roundabout {self.name}: {len(self.vehicles)} vehicles, {len(self.traffic_lights)} traffic lights, {len(self.roundabout_vehicles)} vehicles in roundabout"

from .models import Vehicle, Car, Truck
import numpy as np
from decimal import Decimal, getcontext
class TrafficManager:
    def __init__(self):
        # Initialize a list to keep track of all vehicles in the simulation
        self.vehicles = []
        self.num_lanes = 4

    def add_vehicle(self, vehicle):
        # Add a vehicle to the simulation
        self.vehicles.append(vehicle)

    def remove_vehicle(self, vehicle):
        # Remove a vehicle from the simulation
        if vehicle in self.vehicles:
            self.vehicles.remove(vehicle)

    def update_simulation(self):
        # Update the simulation state, called in each simulation step
        for vehicle in self.vehicles:
            # #TODO: Need to put logic to update each vehicle's behavior based on lane changes etc -> call functions of the vehicle class
            vehicle.update()

    def start_simulation(self):
        # Start the traffic simulation
        while True:
            self.update_simulation()
            # Add logic to control the simulation speed and handle user input
    
    '''
    In the collision_model, we are implementing a collision avoidance system where:
    
    -   Each vehicle is queried, and if its euclidean distance with any of the other vehicles is below a certain tolerance,
        then we slow it down
        
    -   Planning to run some vehicle-system simulations to optimize for a good tolerance -> this would be to ensure that 
        our traffic flow simulator doesn't slow cars down for no reason, and at the same time doesn't miss potential collisions
        
    -   Currently, only deceleration is incorporated for collision avoidance, but in future iterations, we should probably 
        implement safe lane changes, as that would more realistically model traffic flow
        
    -   The logic for lane changes is simple - we will find car density per lane, and prefer to move to emptier lanes if the lane
        change is permitted by the euclidean distance after a few steps
    
    -   This function assumes that this function is being called 2 times per second -> change the value of to_decrease if this 
        is the case. The amount of speed to decrease is calculated such that the 2 cars have distance >= tolerance within 5 time steps
    '''
    
    def calc_euclidean(self, position_1, position_2):
        # 20 decimal places for higher precision as we're handling vehicular collisions
        getcontext().prec = 20  

        x1, y1 = Decimal(position_1[0]), Decimal(position_1[1])
        x2, y2 = Decimal(position_2[0]), Decimal(position_2[1])
        
        squared_diff = (x1 - x2) ** 2 + (y1 - y2) ** 2
        distance = squared_diff.sqrt()
        
        return distance

    def get_adjacencies(self, lane):
        adj = []
        if lane + 1 <= self.num_lanes:
            adj.append(lane + 1)
        if lane - 1 >= 0:
            adj.append(lane - 1)
        return adj
    
    def grid_position(self, position, lane, next_lane):
        # TODO: correctly update the position
        return (position[0] + 5, position[1])
    
    def collision_model(self):
        tolerance = 5   # Dummy value pre-testing -> optimize using simulations
        cars = np.array([vehicle for vehicle in self.vehicles if vehicle.get_vehicle_type() == 'car'])
        trucks = np.array([vehicle for vehicle in self.vehicles if vehicle.get_vehicle_type() == 'truck'])
        
        # Calculate densities of vehicles in each lane for smart collision avoidance described above
        total_vehicles = len(cars) + len(trucks)
        counts = np.zeros(self.num_lanes)
        car_counts = np.zeros(self.num_lanes)
        truck_counts = np.zeros(self.num_lanes)
        
        for i in range(self.num_lanes):
            counts[i] = 0
            for vehicle in list(set(np.concatenate((cars, trucks), axis = 0))):
                if vehicle.lane == i:
                    counts[i] += 1
                if vehicle.get_vehicle_type() == 'car':
                    car_counts[i] += 1
                elif vehicle.get_vehicle_type() == 'truck':
                    truck_counts[i] += 1
                    
        densities = np.array([counts[i]/total_vehicles for i in range(self.num_lanes)])
        car_densities = np.array([car_counts[i]/len(cars) for i in range(self.num_lanes)])
        truck_densities = np.array([truck_counts[i]/len(trucks) for i in range(self.num_lanes)])
        
        to_do_something = False
        
        '''
        For every vehicle, check every other vehicle in its lane for potential collision.
        Find the densities of vehicles in every lane
        Now, if there's any potential collisions, we will do the following:
            - Check if it is better to switch lanes or if it is better to decrease speed in the current lane itself
            - Do the chosen action
        Note: We would prefer to switch if it makes the distribution of vehicles in the different lanes more uniform
        
        - As collisions are vehicle agnostic, we will evaluate cars and trucks together
        - However, we also want to maintain relatively equal distributions of cars and trucks across lanes, so we will make
          lane switches in a way that ensures that
        '''
        
        all_vehicles = list(set(np.concatenate((cars, trucks), axis = 0)))
        
        for i in range(len(all_vehicles)):
            for vehicle in all_vehicles:
                if vehicle.lane != cars[i].lane:
                    continue
                curr_distance = self.calc_euclidean(vehicle.position, all_vehicles[i].position)
                if curr_distance <= tolerance:
                    to_do_something = True
            
            # If we aren't on track to collide, then we can move on to checking the next car
            if to_do_something == False:
                continue
            
            # Find whether it is better to decrease speed or to change lane and implement accordingly
            switched = False
            adj_lanes = self.get_adjacencies(vehicle.lane)
            
            for lane in adj_lanes:
                lane_density = densities[lane]
                current_lane_density = densities[cars[i].lane]
                possible_to_switch = True
                
                # Check if it is possible to move into this particular lane
                curr_position = (vehicle.x, vehicle.y)
                potential_position = self.grid_position(curr_position, all_vehicles[i].lane, lane)
                for vehicle in all_vehicles:
                    if vehicle.position == potential_position and vehicle.lane == lane:
                        possible_to_switch = False
                        break
                
                # Tolerances for proportions of cars and trucks in a given lane
                tol_car = 1/self.num_lanes + 0.2
                tol_truck = 1/self.num_lanes + 0.2
                
                # Checks to ensure that vehicular distributions are not getting too skewed
                if not (vehicle.get_vehicle_type() == 'car' and possible_to_switch == True and car_densities[lane] < tol_car):
                    possible_to_switch = False
                
                elif not (vehicle.get_vehicle_type() == 'truck' and possible_to_switch == True and truck_densities[lane] < tol_truck):
                    possible_to_switch = False
                
                # After all the checks, if it is fine to switch to that lane, then we switch
                if lane_density < current_lane_density and possible_to_switch == True:
                    switched = True
                    all_vehicles[i].lane = lane
                    # TODO: link this change across front-end/back-end
            
            if to_do_something == True and switched == False:
                # Slow down such that after 5 time steps, the distance will be greater than the tolerance
                amount_to_dec = (curr_distance - tolerance) / 5
                all_vehicles[i].decrease_speed(amount_to_dec)
                    
    
            
            
            
            
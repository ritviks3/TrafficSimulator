from django.test import TestCase
from trafficapp.models import Car, Truck
import numpy as np
from decimal import Decimal, getcontext
from manager import TrafficManager


# Class to write testcases for movement
class MovementTests(TestCase):
    def setUp(self):
        # Generate the speed, accel, truck_speed, truck_accel randomly
        self.gen = [np.random.randint(0, 60) for _ in range(4)]
        self.lane = np.random.randint(0, 4) 
        self.initial_position = (0, 0) # (x, y) in a 2 element tuple
        self.initial_position_truck = (0, 0) # (x, y) in a 2 element tuple
        
        # Generate the fuel consumption rate randomly. Here, the cars will of course have a lower rate than trucks.
        fc_rate = np.random.uniform(1.0, 2.0)
        t_fc_rate = np.random.uniform(2.0, 4.0)
        
        # Create the car and truck objects for testing
        self.car = Car.objects.create(speed = self.gen[0], acceleration = self.gen[1], fuel_consumption_rate = fc_rate, distance_travelled = 0)
        self.truck = Truck.objects.create(speed = self.gen[2], acceleration = self.gen[3], fuel_consumption_rate = t_fc_rate, distance_travelled = 0)
    
    # Function to test speed changes 
    def testSpeed(self):
        n = 100 # Test for 100 speed changes
        k = np.random.randint(-20, 20) # Value for speed increase
        curr_speed_car = self.gen[0]
        curr_speed_truck = self.gen[2]
        for i in range(0, n):
            if k > 0:
                self.car.increase_speed(k)
                self.truck.increase_speed(k)
            else:
                self.car.decrease_speed(k)
                self.truck.decrease_speed(k)
            self.assertEqual(self.car.speed, curr_speed_car + k)
            self.assertEqual(self.truck.speed, curr_speed_truck + k)
            curr_speed_car += k
            curr_speed_truck += k
            k += np.random.randint(-10, 10)
    
    # Function to test acceleration changes - basically the same as speed changes
    def testAccel(self):
        n = 100 # Test for 100 accel changes
        k = np.random.randint(-20, 20) # Value for accel increase
        curr_accel_car = self.gen[1]
        curr_accel_truck = self.gen[3]
        for i in range(0, n):
            if k > 0:
                self.car.increase_acceleration(k)
                self.truck.increase_acceleration(k)
            else:
                self.car.decrease_acceleration(k)
                self.truck.decrease_acceleration(k)
            self.assertEqual(self.car.acceleration, curr_accel_car + k)
            self.assertEqual(self.truck.acceleration, curr_accel_truck + k)
            curr_accel_car += k
            curr_accel_truck += k
            k += np.random.randint(-10, 10)
    
    # Function to test whether lane changes are working properly
    def testLaneChanges(self):
        n = 50 # Test for 50 lane changes
        k = np.random.randint(-1, 2) # Value for lane change: [-1 -> left, 0 -> no change, 1 -> right]
        change_dict = {0: "no change", 1: "right", -1: "left"}
        curr_lane = change_dict[k]
        for i in range(0, n):
            self.car.change_lane(change_dict[k])
            self.assertEqual(self.car.lane, curr_lane)
            k = np.random.randint(-1, 2)

    # Function to test whether the type of the vehicle is initialized correctly
    def testType(self):
        car_type = self.car.get_vehicle_type()
        truck_type = self.truck.get_vehicle_type()
        self.assertEqual(car_type, "Car")
        self.assertEqual(truck_type, "Truck")
    
    # Simulate some motion for the vehicles and test whether the positions are getting updated correctly
    def testPosition(self):
        n = 100 # Test for 100 speed changes
        k = np.random.randint(-20, 20) # Value for speed increase
        curr_speed_car = self.gen[0]
        curr_speed_truck = self.gen[2]
        curr_position = self.initial_position
        curr_position_truck = self.initial_position_truck
        for i in range(0, n):
            if k > 0:
                self.car.increase_speed(k)
                self.truck.increase_speed(k)
            else:
                self.car.decrease_speed(k)
                self.truck.decrease_speed(k)
            # Currently, only have 1-D positional changes
            # TODO: implement proper positional changes
            self.assertEqual(self.car.get_position()[0], curr_position[0] + curr_speed_car * (i + 1))
            self.assertEqual(self.truck.get_position()[0], curr_position_truck[0] + curr_speed_truck * (i + 1))
            
            curr_speed_car += k
            curr_speed_truck += k
            k += np.random.randint(-10, 10)
        

# Class to write testcases for collisions
class CollisionTests(TestCase):
    def setUp(self):
        # Create two vehicles for collision testing
        self.gen = [np.random.randint(0, 60) for _ in range(4)]
        self.lane = np.random.randint(0, 4)
        self.initial_position = (0, 0) # (x, y) in a 2 element tuple
        self.initial_position_truck = (0, 0) # (x, y) in a 2 element tuple
        self.num_lanes = 4
        
        # Generate the fuel consumption rate randomly. Here, the cars will of course have a lower rate than trucks.
        fc_rate = np.random.uniform(1.0, 2.0)
        t_fc_rate = np.random.uniform(2.0, 4.0)
        
        # Create the car and truck objects for testing - 20 cars and 20 trucks for now
        self.cars = []
        self.trucks = []
        for i in range(20):
            car = Car.objects.create(speed = self.gen[0], acceleration = self.gen[1], fuel_consumption_rate = fc_rate, distance_travelled = 0)
            self.cars.append(car)
            truck = Truck.objects.create(speed = self.gen[2], acceleration = self.gen[3], fuel_consumption_rate = t_fc_rate, distance_travelled = 0)
            self.trucks.append(truck)

    def calc_euclidean(self, position_1, position_2):
        # 20 decimal places for higher precision as we're handling vehicular collisions
        getcontext().prec = 20  

        x1, y1 = Decimal(position_1[0]), Decimal(position_1[1])
        x2, y2 = Decimal(position_2[0]), Decimal(position_2[1])
        
        squared_diff = (x1 - x2) ** 2 + (y1 - y2) ** 2
        distance = squared_diff.sqrt()
        
        return distance
    
    def testCollisionDetection(self):
        # Use a randomly generated tolerance for 100 tests to check if our collision detection model works
        for i in range(100):
            tolerance = np.random.randint(5, 15)
            
            # We will first test collisions with a randomly sampled vehicle
            curr_vehicle_index = np.random.randint(0, len(self.cars) + len(self.trucks))
            all_vehicles = list(set(np.concatenate((self.cars, self.trucks), axis = 0)))
            initial_distances = []
            for i in range(len(all_vehicles)):
                if i != curr_vehicle_index:
                    initial_distances.append(self.calc_euclidean(all_vehicles[curr_vehicle_index], all_vehicles[i]))
            
            # TODO: set these vehicles as the actual vehicles being tested - proper linking between the files
            TrafficManager.collision_model()
            
            # Checking for collisions
            for i in range(len(all_vehicles)):
                for j in range(len(all_vehicles)):
                    if i != j:
                        self.assertGreater(self.calc_euclidean(all_vehicles[i], all_vehicles[j]), tolerance)
            
            # Checking vehicular distributions after calling the model
            total_vehicles = len(self.cars) + len(self.trucks)
            counts = np.zeros(self.num_lanes)
            car_counts = np.zeros(self.num_lanes)
            truck_counts = np.zeros(self.num_lanes)
            
            for i in range(self.num_lanes):
                counts[i] = 0
                for vehicle in list(set(np.concatenate((self.cars, self.trucks), axis = 0))):
                    if vehicle.lane == i:
                        counts[i] += 1
                    if vehicle.get_vehicle_type() == 'car':
                        car_counts[i] += 1
                    elif vehicle.get_vehicle_type() == 'truck':
                        truck_counts[i] += 1
                        
            densities = np.array([counts[i]/total_vehicles for i in range(self.num_lanes)])
            car_densities = np.array([car_counts[i]/len(self.cars) for i in range(self.num_lanes)])
            truck_densities = np.array([truck_counts[i]/len(self.trucks) for i in range(self.num_lanes)])
            
            for i in range(self.num_lanes):
                self.assertLessEqual(car_densities[i], len(self.cars)/4)
                self.assertLessEqual(truck_densities[i], len(self.trucks)/4)
            
            

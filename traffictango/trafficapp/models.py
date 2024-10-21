from django.db import models
import numpy as np
import heapq


#Base class for both trucks and cars
class Vehicle(models.Model):
    x = models.FloatField(default = 0.0)
    y = models.FloatField(default = 0.0)
    speed = models.FloatField(default = 0.0)
    acceleration = models.FloatField(default = 0.0)
    id = models.IntegerField(primary_key=True,default = 0)
    lane = models.IntegerField(default = 2)

    def __str__(self):
        return f"{self.get_vehicle_type()} - Speed: {self.speed}, Acceleration: {self.acceleration}"

    def get_vehicle_type(self):
        pass
    
    # In this class, we would have several functions which would be common between the car and the truck models
    # Some functions which we have not implemented yet but could consider in the future (among several others) are:
    # 1. Detect Collision - useful considering that our app models flow of traffic
    # 2. Follow route - could pass in a predefined route for the car to follow, and then simulate following that route
    
    def increase_speed(self, speed_delta):
        self.speed += speed_delta
        self.save()

    def decrease_speed(self, speed_delta):
        self.speed -= speed_delta
        self.save()

    def increase_acceleration(self, acceleration_delta):
        self.acceleration += acceleration_delta
        self.save()

    def decrease_acceleration(self, acceleration_delta):
        self.acceleration -= acceleration_delta
        self.save()
    
    #TODO: Implement
    def change_lane(self, direction):
        self.save()
    
    def get_position(self):
        return (self.x, self.y)
    
    #Brake where the braking force would cause it to decrease speed
    def brake(self, decrease):
        self.speed = max(0, self.speed - decrease)
        self.save()
        

# The Car and Truck classes are subclasses of the Vehicle class, in which we are defining fields which only pertain to them
# One such field could be a speed limit - which is obviously going to be different for a car and a truck
# Certain constants for fuel consumption, etc would also be different for a car and a truck

class Car(Vehicle):
    
    fuel_consumption_rate = models.FloatField(default = 0.0) # Set an appropriate rate for fuel consumption after doing some research
    distance_travelled = models.FloatField(default = 0.0)
    
    def get_vehicle_type(self):
        return "Car"

    def calculate_fuel_consumption(self):
        rate = self.fuel_consumption_rate
        return rate * self.distance_travelled
class Truck(Vehicle):
    
    fuel_consumption_rate = models.FloatField(default = 0.0) # Set an appropriate rate for fuel consumption after doing further research
    distance_travelled = models.FloatField(default = 0.0)
    
    def get_vehicle_type(self):
        return "Truck"
    
    def calculate_fuel_consumption(self):
        rate = self.fuel_consumption_rate
        return rate * self.distance_travelled


class Piece(models.Model):
    position = (models.IntegerField(default = 0), models.IntegerField(default = 0))
    roadType = models.CharField(max_length = 10)

    def is_road(self):
        return self.roadType != "roadPLAZA"
    
    def set_roadtype(self, road):
        self.roadType = road
        self.save()
    
    def is_intersection(self):
        return self.roadType in ["roadNEWS", "roadTE", "roadTN", "roadTS", "roadTW"]
    
    def set_coordinate(self, position):
        self.position = position
    
class Board(models.Model):
    
    # This is how the grid will be stored in the back-end, as a JSONField
    # I believe this is a good approach because we can easily encode and decode to/from JSONs, and handling None values will also become quite simple
    board = models.JSONField()
    
    # Initializing the board
    def __init__(self):
        self.board = [[None for _ in range(10)] for _ in range(10)]
        for i in range(10):
            for j in range(10):
                piece = Piece()
                piece.set_roadtype("roadPLAZA")
                piece.set_coord((i,j))
                self.board[i][j] = piece
    
    # Change the type of piece at a given position in the board
    def change_piece(self, position, new_road_type):
        piece = self.board[position[0]][position[1]]
        piece.set_roadtype(new_road_type)
    
    # Set a piece at a given posiiton
    def set_piece(self, position, road_type):
        if self.board[position[0]][position[1]] is None:
            piece = Piece()
            piece.set_roadtype(road_type)
            piece.set_coord(position)
            self.board[position[0]][position[1]] = piece
        else:
            self.change_piece(position, road_type)
    
    # We want to find the number of "islands" of connected roads in our board
    # TODO: improve model
    def calc_components(self):
        unvisited_squares = set((r, c) for r in range(10) for c in range(10) if self.board[r][c] != 0)

        count = 0
        while unvisited_squares:
            count += 1
            stack = [unvisited_squares.pop()]
            while stack:
                r, c = stack.pop()
                adjs = [(r + 1, c), (r, c + 1), (r - 1, c), (r, c - 1), (r + 1, c + 1), (r + 1, c - 1), (r - 1, c + 1), (r - 1, c - 1)]
                for adj in adjs:
                    if adj in unvisited_squares:
                        stack.append(adj)
                        unvisited_squares.remove(adj)
        return count

    # Since we have implemented the board implementation, things like shortest paths naturally make sense to have as functionalities 
    # in a traffic simulation.
    def create_graph(self):
        graph = {}
        for r in range(10):
            for c in range(10):
                if self.board[r][c] is not None:
                    neighbors = []
                    if r + 1 < 10 and self.board[r + 1][c] is not None:
                        neighbors.append((r + 1, c))
                    if c + 1 < 10 and self.board[r][c + 1] is not None:
                        neighbors.append((r, c + 1))
                    if r - 1 >= 0 and self.board[r - 1][c] is not None:
                        neighbors.append((r - 1, c))
                    if c - 1 >= 0 and self.board[r][c - 1] is not None:
                        neighbors.append((r, c - 1))
                    graph[(r, c)] = neighbors
        return graph
                        
    def shortest_path(self, start, end):
        graph = self.create_graph()
        distances = {vertex: float('inf') for vertex in graph}
        distances[start] = 0
        priority_queue = [(0, start)]

        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)

            if current_distance > distances[current_vertex]:
                continue

            for neighbor in graph[current_vertex]:
                distance = current_distance + 1
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances[end]
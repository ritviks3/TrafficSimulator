import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 255, 255)
CAR_RADIUS = 20
CIRCLE_CENTER = (WIDTH // 2, HEIGHT // 2)
CIRCLE_RADIUS = 200

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Collisions on a Roundabout")

# Car class
class Car:
    def __init__(self, angle, speed, CAR_RADIUS):
        self.angle = angle
        self.radius = CAR_RADIUS
        self.color = (0, 0, 255)
        self.speed = speed

    def draw(self):
        x = CIRCLE_CENTER[0] + CIRCLE_RADIUS * math.cos(self.angle)
        y = CIRCLE_CENTER[1] + CIRCLE_RADIUS * math.sin(self.angle)
        pygame.draw.circle(screen, self.color, (int(x), int(y)), self.radius)

    def move(self):
        self.angle += self.speed

    def check_collision(self, other_car):
        if abs(self.angle - other_car.angle) < 0.2:
            return True
        return False

# Create cars with random speeds
NUM_CARS = 10
cars = [Car(random.uniform(0, 2 * math.pi), random.uniform(0.0001, 0.0003), CAR_RADIUS) for _ in range(NUM_CARS)]

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND_COLOR)

    for car in cars:
        car.draw()
        car.move()

    # Check for collisions and reset car colors
    for i in range(len(cars)):
        cars[i].color = (0, 0, 255)
        for j in range(i + 1, len(cars)):
            if cars[i].check_collision(cars[j]):
                cars[i].color = (255, 0, 0)
                cars[j].color = (255, 0, 0)

    pygame.display.update()

pygame.quit()
sys.exit()

import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 200
CAR_WIDTH, CAR_HEIGHT = 40, 20
BG_COLOR = (255, 255, 255)
CAR_COLOR = (255, 0, 0)
FPS = 60
ACCELERATION = 0.2  # Deceleration rate

# Create the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Deceleration")

# Car properties
car_x = 50
car_y = HEIGHT // 2 - CAR_HEIGHT // 2
car_speed = 2

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Decelerate the car gradually
    if car_speed > 0:
        car_speed -= ACCELERATION

    car_x += car_speed

    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, CAR_COLOR, (car_x, car_y, CAR_WIDTH, CAR_HEIGHT))
    pygame.display.flip()

    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()

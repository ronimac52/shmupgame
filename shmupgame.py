# Pygame template - skeleton for new pygame projects - from www.kidscancode.com.
import pygame
import random

WIDTH = 360 # width of new game window
HEIGHT = 480 # height ------------
FPS = 30 # frames per second

# define Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialise pygame and create window
pygame.init()
pygame.mixer.init()  # for sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

# Game Loop
running = True
while running:
    #keep loop running at correct speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    # Update
    all_sprites.update()

    # Render (draw)
    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # *after* drawing everything, flip the display
    pygame.display.flip()


pygame.quit()

# Pygame template - skeleton for new pygame projects - from www.kidscancode.org.
import pygame
import random

WIDTH = 480 # width of new game window
HEIGHT = 600 # height ------------
FPS = 60 # frames per second

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
pygame.display.set_caption("Shmup")
clock = pygame.time.Clock()
# set up Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)# Initiate sprite
        self.image = pygame.Surface((50, 40))# plain rectangle for now
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()# get rect from Pygame
        self.rect.centerx = WIDTH / 2# position middle of window
        self.rect.bottom = HEIGHT - 10# 10 px from bottom
        self.speedx = 0 # To move side to side (x axis)

    def update(self):# what happens every update in animation loop
        self.rect.x += self.speedx # move on x axis by whatever speed is set on self.speed.x

# spawn sprites
all_sprites = pygame.sprite.Group()
player = Player() #create new object in Player class
all_sprites.add(player) # add object to all_sprites so it gets updated and drawn

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

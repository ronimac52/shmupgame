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
YELLOW = (255, 255, 0)

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
        self.speedx = 0
        keystate = pygame.key.get_pressed() #returns dictionary of every key with a boolean True for each pressed key
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx # move on x axis by whatever speed is set on self.speed.x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width) # sprites appear randomly across screen
        self.rect.y = random.randrange(-100, -40) #spawn randomly vertically (off-screen)
        self.speedy = random.randrange(1, 8)  #sprite move down at different speeds
        self.speedx = random.randrange(-3, 3) # random sideways movement

    def update(self):
        self.rect.x += self.speedx # move sideways
        self.rect.y += self.speedy # move down
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20: #  if leaves screen, respawn randomly at top
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()
# spawn sprites
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player() #create new object in Player class
all_sprites.add(player) # add object to all_sprites so it gets updated and drawn
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    # Update
    all_sprites.update()

    # check to see if a mob hits the player
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False

    # Render (draw)
    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # *after* drawing everything, flip the display
    pygame.display.flip()


pygame.quit()

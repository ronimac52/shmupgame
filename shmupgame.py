# Pygame template - skeleton for new pygame projects - from www.kidscancode.org.
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# Art from Kenney.nl


# this comment is just a test to show Louie git and github
import pygame
import random
from os import path # so we can use local files on computer

img_dir = path.join(path.dirname(__file__), 'img') # img_dir variable will be path to img folder
snd_dir = path.join(path.dirname(__file__), 'snd') # snd_dir = path to sound folder

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
pygame.mixer.pre_init(44100, -16, 1, 256)
pygame.init()
pygame.mixer.init(frequency=44100)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup")
clock = pygame.time.Clock()

# Define function to draw text
# with parameters: surf = surface we want text drawn on,
# text = the text which will be a string,
# size = size of font,
# x and y = coordinates of where we want text to be
font_name = pygame.font.match_font('arial') # find an arial font on computer
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size) # font object
    text_surface = font.render(text, True, WHITE) # True = anti-aliased
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# set up Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)# Initiate sprite
        self.image = pygame.transform.scale(player_img, (50, 38)) #pygame.transform.scale()changed(reduced) size
        self.image.set_colorkey(BLACK) #made black around image transparent (not be blit)
        self.rect = self.image.get_rect()# get rect from Pygame
        self.radius = 20
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
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
        bullets.add(bullet)
        #shoot_sound.play()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy() # make self.image a copy of original (fresh copy each rotate)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width) # sprites appear randomly across screen
        self.rect.y = random.randrange(-150, -100) #spawn randomly vertically (off-screen)
        self.speedy = random.randrange(1, 8)  #sprite move down at different speeds
        self.speedx = random.randrange(-3, 3) # random sideways movement
        self.rot = 0 # variable to rotate sprite
        self.rot_speed = random.randrange(-8, 8) # random speed - rotates spries in different directions
        self.last_update = pygame.time.get_ticks() # variable to be updated everytime image is updated

    def rotate(self):
        now = pygame.time.get_ticks() # check time now
        if now - self.last_update > 50: # if its more than 50 milliseconds since last update
            self.last_update = now # rotate now
            self.rot = (self.rot + self.rot_speed) % 360 # ensure rotation loops back to 1
            new_image = pygame.transform.rotate(self.image_orig, self.rot) # new image rotated by value of self.rot
            old_center = self.rect.center # variable to hold position of current center of rect
            self.image = new_image
            self.rect = self.image.get_rect() # get new rectangle
            self.rect.center = old_center # center new rect on same spot as old rect

    def update(self):
        self.rotate() # everytime we update we check to see if its time to rotate
        self.rect.x += self.speedx # move sideways
        self.rect.y += self.speedy # move down
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20: #  if leaves screen, respawn randomly at top
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

# Load all game graphics
background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip2_orange.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
meteor_images = []
meteor_list =['meteorBrown_big1.png','meteorBrown_big2.png',
              'meteorBrown_med1.png','meteorBrown_med3.png',
              'meteorBrown_small1.png','meteorBrown_small2.png',
              'meteorBrown_tiny1.png']

for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

# Load all game sounds
#shoot_sound = pygame.mixer.Sound(path.join(img_dir, 'pew.wav'))
#expl_sounds = []
#for snd in ['expl3.wav', 'expl6.wav']:
    #expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))

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
score = 0 # initialise variable to add to and keep track of score

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

    # check to see if a bullet hits a mob and delete bullet and mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius # add 50 - radius of mob to score for each hit
        # random.choice(expl_sounds).play()
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

      # check to see if a mob hits the player
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    if hits:
        running = False

    # Render (draw)
    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect) # blit combines several bitmaps into one
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)

    # *after* drawing everything, flip the display
    pygame.display.flip()


pygame.quit()

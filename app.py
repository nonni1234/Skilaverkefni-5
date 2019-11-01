import pygame
import random
from pygame.locals import (
        RLEACCEL,
        K_UP,
        K_DOWN,
        K_LEFT,
        K_RIGHT,
        K_ESCAPE,
        K_w,
        K_a,
        K_s,
        K_d,
        KEYDOWN,
        QUIT,
    )

# Startar pygame
pygame.init()

# Variables fyrir leikinn
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
PLAYER_SPEED = 8
MISSILE_MIN = 8
MISSILE_MAX = 15

# Setur upp skjáinn
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/jet.png").convert() # Surface fyrir playerinn
        self.surf.set_colorkey((255, 255, 255), RLEACCEL) # Gerir það transparent fyrir png mynd
        self.rect = self.surf.get_rect() # notað fyrir staðsetningu og stuff

    # Hreyfir playerinn eftir inputti
    # Btw sesselja move_ip þýðir move in place :)
    def update(self, pressed_keys):
        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.rect.move_ip(0, -PLAYER_SPEED)
        if pressed_keys[K_DOWN] or pressed_keys[K_s]:
            self.rect.move_ip(0, PLAYER_SPEED)
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.rect.move_ip(-PLAYER_SPEED, 0)
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.rect.move_ip(PLAYER_SPEED, 0)

        # Heldur player á skjánum
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Óvinur Talvan
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("images/missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(MISSILE_MIN, MISSILE_MAX)

    # Hreyfir óvininn þangað til hann er kominn á enda skjáinn og drepur hann
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud,self).__init__()
        self.surf = pygame.image.load("images/cloud.png").convert()
        self.surf.set_colorkey((0,0,0),RLEACCEL)
        # Random byrjunarstaður
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0,SCREEN_HEIGHT)
            )
        )
    def update(self):
        self.rect.move_ip(-5,0)
        if self.rect.right < 0:
            self.kill()
# Aðal loopið
player = Player()

# Custom events sem vinna með að bæta við enemies og clouds á skjáinn á ákveðnum tímum (skil þetta ekki 100%)
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

clock = pygame.time.Clock() # Notað fyrir framerate (sjá lína 151)
running = True
while running:
    for event in pygame.event.get(): # Checkar fyrir keypresses og events
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        # Add a new enemy?
        elif event.type == ADDENEMY: # Triggerar þegar custom event timerinn triggerast
        # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == ADDCLOUD: # Triggerar þegar custom event timerinn triggerast
            # Create the new cloud and add it to sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
    pressed_keys = pygame.key.get_pressed()

    # Update fallið í klössunum updatear staðsetningu þeirra í hverju frame
    player.update(pressed_keys)
    enemies.update()
    clouds.update()
    screen.fill((90,0,255))

    for ent in all_sprites: # renderar alla spriteana á skjáinn með blit methodinu
        screen.blit(ent.surf, ent.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        player.kill()
        running = False
    #screen.blit(player.surf,player.rect)
    pygame.display.flip()
    clock.tick(30) # 30FPS
pygame.quit()
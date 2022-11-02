import pygame
import random
from os import path

WIDTH = 1480
HEIGHT = 900
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Арканоид')
clock = pygame.time.Clock()


game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'img')
snd_folder = path.join(game_folder, 'sound')
player_img = pygame.image.load(path.join(img_folder, 'playerShip.png'))
mob_img = pygame.image.load(path.join(img_folder, 'mob_blue.png'))
bullet_img = pygame.image.load(path.join(img_folder, 'laserRed01.png')) 

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_folder, filename)).convert()
    img.set_colorkey(BLACK)
    img_sm = pygame.transform.scale(img, (75, 75))
    explosion_anim['sm'].append(img_sm)
    img_lg = pygame.transform.scale(img, (162, 162))
    explosion_anim['lg'].append(img_lg)


shoot_sound = pygame.mixer.Sound(path.join(snd_folder, 'pew.wav'))
expl_sound = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sound.append(pygame.mixer.Sound(path.join(snd_folder, snd)))
pygame.mixer.music.load(path.join(snd_folder, 'tgfcoder-FrozenJam-SeamlessLoop.mp3'))
pygame.mixer.music.set_volume(1)    

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 25
        self.rect.centerx = (WIDTH/2)
        self.rect.bottom = (HEIGHT - 10)
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shoot = pygame.time.get_ticks()


    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()        
        self.rect.x += self.speedx

        if self.rect.right > WIDTH: 
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0   

    def shoot(self):
        now = pygame.time.get_ticks()
        if (now - self.last_shoot) > self.shoot_delay:
            self.last_shoot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()         

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(mob_img, (70, 48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width/2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -self.rect.width/2 or self.rect.right > WIDTH + self.rect.width:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            self.speedx = random.randrange(-3, 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -30

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill() 

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self) 
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if (now - self.last_update) > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center                

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def new_mobs():
    m = Mob()
    all_sprites.add(m) 
    mobs.add(m)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 200
    BAR_HEIGHT = 20
    fill = (pct/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)    


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
font_name = pygame.font.match_font('arial')
background_img = pygame.image.load(path.join(img_folder, 'sky.jpg')).convert()
background_rect = background_img.get_rect()

for i in range(31):
    new_mobs()

score = 0
pygame.mixer.music.play(loops=-1)

        
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= 25
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        new_mobs()
        if player.shield <= 0:
            running = False
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits.items():
        score += 10
        expl = Explosion(hit[0].rect.center, 'sm')
        all_sprites.add(expl)
        random.choice(expl_sound).play()

    screen.fill(WHITE)
    screen.blit(background_img, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 36, WIDTH/2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    pygame.display.flip()

pygame.quit()                

import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), "img")
wav_dir = path.join(path.dirname(__file__), "wav")

WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000
score = 0

# Définis des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialise le jeu
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test!")
clock = pygame.time.Clock()

font_name = pygame.font.match_font("arial")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # Pour voir le cercle de "collision"
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timmer = pygame.time.get_ticks()
        self.power = 1
        self.power_timmer = pygame.time.get_ticks()

    def update(self):
        # Temps des powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        # Montre si le joueur est caché
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
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

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def difficulty(self):
        self.difficulty += 1

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top - 7)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
            if self.power >= 3 and score >= 5000:
                bullet3 = Bullet(self.rect.centerx, self.rect.top - 7)
                all_sprites.add(bullet3)
                bullets.add(bullet3)
                shoot_sound.play()
            if self.power >= 4 and score >= 10000:
                bullet4 = Bullet(self.rect.left + 12, self.rect.top)
                all_sprites.add(bullet4)
                bullets.add(bullet4)
                shoot_sound.play()
            if self.power >= 5 and score >= 15000:
                bullet5 = Bullet(self.rect.right - 12, self.rect.top)
                all_sprites.add(bullet5)
                bullets.add(bullet5)
                shoot_sound.play()

    def hide(self):
        # Cache le joueur temporairement
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # Pour voir le cercle de "collision"
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 50:
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

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["Shield", "Gun"])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
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
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Score = ", 50, WIDTH / 2.8, HEIGHT / 4)
    draw_text(screen, str(score), 50, WIDTH / 1.5, HEIGHT / 4)
    draw_text(screen, "Touches de directions pour bouger", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Espace pour tirer", 22, WIDTH / 2, HEIGHT / 1.8)
    draw_text(screen, "Presser une touche pour commencer", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# Charges les graphiques
background = pygame.image.load(path.join(img_dir, "Space.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip2_blue.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir, "laserBlue01.png")).convert()
meteor_images = []
meteor_list = ["meteorBrown_big1.png", "meteorBrown_big2.png", "meteorBrown_med1.png",
               "meteorBrown_med1.png", "meteorBrown_small1.png", "meteorBrown_small2.png",
               "meteorBrown_tiny1.png"]
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
explosion_anim = {}
explosion_anim["lg"] = []
explosion_anim["sm"] = []
for i in range(9):
    filename = "regularExplosion0{}.png".format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim["lg"].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim["sm"].append(img_sm)
powerup_images = {}
powerup_images["Shield"] = pygame.image.load(path.join(img_dir, "Shield.png"))
powerup_images["Gun"] = pygame.image.load(path.join(img_dir, "Gun.png"))

# Charge les sons du jeu
gun_sound = pygame.mixer.Sound(path.join(wav_dir, "Gun.wav"))
shield_sound = pygame.mixer.Sound(path.join(wav_dir, "Shield.wav"))
shoot_sound = pygame.mixer.Sound(path.join(wav_dir, "Laser.wav"))
expl_sound = pygame.mixer.Sound(path.join(wav_dir, "Explosion.wav"))
player_die_sound = pygame.mixer.Sound(path.join(wav_dir, "Death.wav"))





# Game loop
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(10):
            newmob()
        difficulty = 1
        score = 0


    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False


    # Update
    all_sprites.update()

    # Vérifie si un laser a touché une météorite
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hits in hits:
        score += 55 - hits.radius
        expl_sound.play()
        expl = Explosion(hits.rect.center, "lg")
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hits.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

	# Vérifie si une météorite a touché le joueur
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hits in hits:
        player.shield -= hits.radius * 2
        expl = Explosion(hits.rect.center, "sm")
        expl_sound.play()
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, "lg")
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    # Vérifie si le joueur a un powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == "Shield":
            player.shield += random.randrange(10, 30)
            shield_sound.play()
            if player.shield >= 100:
                player.shield = 100
        if hit.type == "Gun":
            player.powerup()
            gun_sound.play()

    # Ajoute de la difficulté par rapport au score
    if score >= 1000 and score <= 1050 and difficulty == 1:
        for i in range(1):
            newmob()
        difficulty += 1
    if score >= 2000 and score <= 2050 and difficulty == 2:
        for i in range(2):
            newmob()
        difficulty += 1
    if score >= 3000 and score <= 3050 and difficulty == 3:
        for i in range(3):
            newmob()
        difficulty += 1
    if score >= 4000 and score <= 4050 and difficulty == 4:
        for i in range(4):
            newmob()
        difficulty += 1
    if score >= 5000 and score <= 5050 and difficulty == 5:
        for i in range(5):
            newmob()
        difficulty += 1
    if score >= 6000 and score <= 6050 and difficulty == 6:
        for i in range(6):
            newmob()
        difficulty += 1
    if score >= 7000 and score <= 7050 and difficulty == 7:
        for i in range(7):
            newmob()
        difficulty += 1
    if score >= 8000 and score <= 8050 and difficulty == 8:
        for i in range(8):
            newmob()
        difficulty += 1
    if score >= 9000 and score <= 9050 and difficulty == 9:
        for i in range(9):
            newmob()
        difficulty += 1
    if score >= 10000 and score <= 10050 and difficulty == 10:
        for i in range(10):
            newmob()
        difficulty += 1
    if score >= 11000 and score <= 11050 and difficulty == 11:
        for i in range(11):
            newmob()
        difficulty += 1
    if score >= 12000 and score <= 12050 and difficulty == 12:
        for i in range(12):
            newmob()
        difficulty += 1
    if score >= 13000 and score <= 13050 and difficulty == 13:
        for i in range(13):
            newmob()
        difficulty += 1
    if score >= 14000 and score <= 14050 and difficulty == 14:
        for i in range(14):
            newmob()
        difficulty += 1
    if score >= 15000 and score <= 15050 and difficulty == 15:
        for i in range(15):
            newmob()
        difficulty += 1

    # Lorsque le joueur est mort, et que l'explosion du joueur a fini
    if player.lives == 0 and not death_explosion.alive():
        game_over = True

    # Partie Graphique
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    pygame.display.flip()

pygame.quit()
import pygame
import os, time, random, math

from pygame import mixer as sound

# ------ Variables -------
prev_time = time.time()

# gamerstats
score = 0
num_of_bullets = 5
finished = False

# paths
imagefolder_path = "D:\Programming\Learnings\Pygame\MyFirstGame\Images"
soundfolder_path = "D:\Programming\Learnings\Pygame\MyFirstGame\Sounds"

# images
icon = pygame.image.load(os.path.join(imagefolder_path, "ufo.png"))
plr_image = pygame.image.load(os.path.join(imagefolder_path, "spaceship.png"))

background_image = pygame.image.load(os.path.join(imagefolder_path, "background.png"))
laser_image = pygame.image.load(os.path.join(imagefolder_path, "laser.png"))

# playerstats
plrX = 370
plrY = 480
plr_speed = 1000
left = False
right = False

# enemystats
num_of_enemies = 5

enemies_images = []
enemiesX = []
enemiesY = []
directions = []

enemy_speed = 500
step_value = 50

# adds the enemies in the game
for i in range(num_of_enemies):
    enemies_images.append(
        pygame.image.load(os.path.join(imagefolder_path, "enemy.png"))
    )
    enemiesX.append(random.randint(0, 800))
    enemiesY.append(random.randint(50, 150))
    directions.append(random.choice([True, False]))


# bulletstats

bulletX = 0
bulletY = plrY
in_motion = False
bullet_speed = 5000

# ------ Functions -------


def player(x, y):

    # draw the player on the screen
    screen.blit(plr_image, (x, y))


def enemy(x, y, i):

    # draw the enemy on the screen
    screen.blit(enemies_images[i], (x, y))


def fire_laser(x, y):

    # draw the laser on the screen
    screen.blit(laser_image, (x, y - 20))


def collided(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(
        (math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2))
    )

    return True if distance < 50 else False


def show_score(x, y):
    font = pygame.font.Font("freesansbold.ttf", 32)
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (x, y))


def show_bullets(x, y):
    font = pygame.font.Font("freesansbold.ttf", 20)
    text = font.render(f"Bullets: {num_of_bullets}", True, (255, 255, 255))
    screen.blit(text, (x, y))

def game_over():
    global finished
    global left
    global right


    for i in range(num_of_enemies):
        enemiesY[i] = -4000

    left = right = False
    finished = True

def game_over_text():
    font = pygame.font.Font("freesansbold.ttf", 64)
    text = font.render(f"GAME OVER", True, (255, 255, 255))

    screen.blit(text, (200, 250))

    font = pygame.font.Font("freesansbold.ttf", 32)
    text = font.render(f"PRESS R TO RETRY", True, (255, 255, 255))

    screen.blit(text, (232, 350))

def retry():
    global finished
    global num_of_bullets
    global score

    finished = False
    num_of_bullets = 5
    score = 0

    for i in range(num_of_enemies):
        enemiesX[i] = random.randint(0, 800)
        enemiesY[i] = random.randint(50, 150)

    
# -------- Setting Up -----------

# initialize the pygame
pygame.init()

# create a screen (width,height)
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(icon)


# Background Music
sound.music.load(os.path.join(soundfolder_path, "background.wav"))
sound.music.play(-1)

# --------------- Game Loop ---------------
running = True
while running:

    # make the game frame independent
    now = time.time()
    delta_time = now - prev_time
    prev_time = now

    # change the background screen  
    screen.fill((0, 0, 0))

    # add background_image
    screen.blit(background_image, (0, 0))
    # check if the game has been closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

        # ------- Player Input ----------

        # Movement
        if event.type == pygame.KEYDOWN:
            if event.key == 97 and finished == False:
                left = True
            elif event.key == 100 and finished == False:
                right = True

        if event.type == pygame.KEYUP:

            if event.key == 97:
                left = False

            if event.key == 100:
                right = False

            if finished == True:
                if event.key == 114:
                    retry()

        # Bullets

        if event.type == pygame.MOUSEBUTTONUP:
            if in_motion == False and finished == False:
                bullet_sound = sound.Sound(os.path.join(soundfolder_path, "laser.wav"))
                bullet_sound.play()
                in_motion = True
                bulletX = plrX

    # Update Player Position

    if right == True and plrX < 730:
        plrX += plr_speed * delta_time

    if left == True and plrX > 10:
        plrX -= plr_speed * delta_time

    # move the enemy
    for i in range(num_of_enemies):
        if directions[i] == True:
            enemiesX[i] += enemy_speed * delta_time
        else:
            enemiesX[i] -= enemy_speed * delta_time

    # move the bullet

    if in_motion == True:
        fire_laser(bulletX, bulletY)
        bulletY -= bullet_speed * delta_time

    if bulletY < 0:
        num_of_bullets -= 1
        in_motion = False
        bulletY = plrY

    # set the boundary for the enemy
    for i in range(num_of_enemies):
        if enemiesX[i] > 740:
            enemiesY[i] += step_value
            enemiesX[i] = 740
            directions[i] = False

        if enemiesX[i] < 0:
            enemiesY[i] += step_value
            enemiesX[i] = 0
            directions[i] = True

        if enemiesY[i] > 460:
            game_over()
            

    # collission
    for i in range(num_of_enemies):
        has_collided = collided(enemiesX[i], enemiesY[i], bulletX, bulletY)

        if has_collided == True and in_motion == True:
            explosion_sound = sound.Sound(
                os.path.join(soundfolder_path, "explosion.wav")
            )
            explosion_sound.play()
            score += 1
            in_motion = False
            bulletY = plrY 

            # reposition the enemy
            enemiesX[i] = random.randint(0, 800)
            enemiesY[i] = random.randint(50, 150)

    # add the player to the game
    player(plrX, plrY)

    # add enemy to the game
    for i in range(num_of_enemies):
        enemy(enemiesX[i], enemiesY[i], i)

    # show the score
    show_score(10, 10)

    if num_of_bullets == 0:
        game_over()

    if finished == True:
        game_over_text()


    # show bullets
    show_bullets(10, 45)

    # update the screen on iteration
    pygame.display.update()

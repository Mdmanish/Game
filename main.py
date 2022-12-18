import pygame
import random
import math
from pygame import mixer

# pygame initialization.
pygame.init()

# Creating screen.
screen = pygame.display.set_mode((800, 600))

# Backgroud
background = pygame.image.load('background2.png')

# Backgroud sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption('Manish')
icon = pygame.image.load('game_image.png')
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load('space-invaders.png')
player_img = pygame.transform.scale(player_img, (50, 35))
player_x_coordinat = 370
player_y_coordinat = 480
player_x_change = 0
player_y_change = 0

# Enemy
enemy_image = pygame.image.load('alien.png')
enemy_image = pygame.transform.scale(enemy_image, (50, 35))

enemy_img, enemy_x_coordinat, enemy_y_coordinat, enemy_x_change, enemy_y_change = [], [], [], [], []
no_of_enemy = random.randint(2, 9)
for i in range(no_of_enemy):
    enemy_img.append(enemy_image)
    enemy_x_coordinat.append(random.randint(0, 750))
    enemy_y_coordinat.append(random.randint(50, 250))
    enemy_x_change.append(6)
    enemy_y_change.append(30)


# Bullet
# Ready - You can't see the bullet on screen
# Fire - The bullet is currently moving
bullet_img = pygame.image.load('bullet.png')
bullet_img = pygame.transform.scale(bullet_img, (50, 35))
bullet_x_coordinat = player_x_coordinat
bullet_y_coordinat = player_y_coordinat
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"


def player(x, y):
    """This function shows the player in (x, y) co-ordinate."""

    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    """This function shows the enemy in (x, y) co-ordinate."""

    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    """This function used to change the bullet state from ready to fire state
    and shows the bullet on screen.
    """

    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x, y))


def is_collision(bullet_x, bullet_y, enemy_x, enemy_y):
    """This function calculates distance between bullet and enemy and 
    if distance is <= 27 then collision happens.
    """

    distance = math.sqrt((math.pow(bullet_x - enemy_x, 2)) +
                         (math.pow(bullet_y - enemy_y, 2)))
    if distance <= 27:
        return True


# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10


# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    """This function is used to show the text and pause the music after ending the game."""

    over_text = over_font.render("GAME OVER ", True, (255, 255, 255))
    screen.blit(over_text, (240, 270))
    score = font.render("Scores: " + str(score_value), True, (255, 0, 255))
    screen.blit(score, (340, 350))
    mixer.music.pause()


def show_score(x, y):
    """This function is used to show the current score on top left corner of window."""

    score = font.render("Scores: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


running = True

# Game loop
while running:
    # set the background image.
    screen.blit(background, (0, 0))
    # handles the all the event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change -= 5
            if event.key == pygame.K_RIGHT:
                player_x_change += 5
            if event.key == pygame.K_UP:
                player_y_change -= 5
            if event.key == pygame.K_DOWN:
                player_y_change += 5
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                bullet_x_coordinat = player_x_coordinat
                bullet_y_coordinat = player_y_coordinat
                fire_bullet(bullet_x_coordinat, bullet_y_coordinat)

        if event.type == pygame.KEYUP:
            player_x_change = 0
            player_y_change = 0

    # Checking of boundries so space ship does not go outside.
    player_x_coordinat += player_x_change
    player_y_coordinat += player_y_change
    if player_x_coordinat >= 750:
        player_x_coordinat = 750
    if player_x_coordinat <= 0:
        player_x_coordinat = 0
    if player_y_coordinat >= 565:
        player_y_coordinat = 565
    if player_y_coordinat <= 0:
        player_y_coordinat = 0
    player(player_x_coordinat, player_y_coordinat)

    # Moving enimies increasing and decreasing enimies y axis.
    # This loop is because of we have multiple enemies.
    for i in range(no_of_enemy):
        enemy_x_coordinat[i] += enemy_x_change[i]
        if enemy_x_coordinat[i] >= 750:
            enemy_x_change[i] = -6
            enemy_x_coordinat[i] = 750
            enemy_y_coordinat[i] += enemy_y_change[i]

        if enemy_x_coordinat[i] <= 0:
            enemy_x_change[i] = 6
            enemy_x_coordinat[i] = 0
            enemy_y_coordinat[i] += enemy_y_change[i]

        enemy(enemy_x_coordinat[i], enemy_y_coordinat[i], i)

        # Game over condition and updated the player and bullet position.
        if enemy_y_coordinat[i] > 565:
            for j in range(no_of_enemy):
                enemy_y_coordinat[j] = 1500
            game_over_text()
            player_x_coordinat = 370
            player_y_coordinat = 480
            bullet_x_coordinat = -100
            bullet_y_coordinat = -100
            break

        # Bullet enemy collision
        if is_collision(bullet_x_coordinat, bullet_y_coordinat, enemy_x_coordinat[i], enemy_y_coordinat[i]):
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            score_value += 1
            bullet_x_coordinat = -100
            bullet_y_coordinat = -100
            bullet_state = "ready"
            enemy_x_coordinat[i] = random.randint(0, 750)
            enemy_y_coordinat[i] = random.randint(50, 250)

    # Bullet movement
    if bullet_state == "fire":
        bullet_y_coordinat -= bullet_y_change
        fire_bullet(bullet_x_coordinat, bullet_y_coordinat)
        if bullet_y_coordinat <= -50:
            bullet_state = "ready"

    show_score(text_x, text_y)
    pygame.display.update()
    
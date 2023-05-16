import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((800,600))

# Title and icon
pygame.display.set_caption("Space Invasion")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
background = pygame.image.load("Background.jpg")

# Add music
mixer.music.load("background_music.mp3")
mixer.music.play(-1)

# player variables
img_player = pygame.image.load("spaceship.png")
player_x = 368
player_y = 536
player_x_change = 0
player_y_change = 0

# Enemy variable
img_enemy = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
number_of_enemies = 8

for e in range(number_of_enemies):
    img_enemy.append(pygame.image.load("enemy_ship.png"))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(40,200))
    enemy_x_change.append(0.2)
    enemy_y_change.append(40)


# Missile variable
img_missile = pygame.image.load("missile.png")
missile_x = 0
missile_y = 500
missile_x_change = 0
missile_y_change = 0.5
visible_missile = False

# Score
score = 0
my_font = pygame.font.Font('space age.ttf', 32)
text_x = 10
text_y = 10

# Enemy speed text
enemy_speed = pygame.font.Font('space age.ttf', 32)
enemy_score_text_x = 300
enemy_score_text_y = 10

# End of game text
end_font = pygame.font.Font("space age.ttf", 40)

def final_text():
    my_final_font = end_font.render("GAME OVER", True, (255,255,255))
    screen.blit(my_final_font, (200,200))

# Show score function
def show_score(x,y):
    text = my_font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(text,(x,y))

# Show enemy speed
def show_enemy_speed(x,y):
    text = enemy_speed.render(f"Enemy Speed: {enemy_x_change}", True, (255,255,255))
    screen.blit(text,(x,y))

# Detect collision function
def there_is_a_collision(x_1, y_1, x_2, y_2):
    distance = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1 , 2))
    if distance < 27:
        return True
    else:
        return False


# Player function
def player(x, y):
    screen.blit(img_player, (x, y))

# Enemy function
def enemy(x, y, en):
    screen.blit(img_enemy[en], (x, y))

# Shoot missile function
def shoot_missile(x,y):
    global visible_missile
    visible_missile = True
    screen.blit(img_missile, (x + 16, y + 10))


# Game loop
is_running = True
while is_running:
    # Background image
    screen.blit(background, (0,0))

    # Event iteration
    for event in pygame.event.get():

        # Closing event
        if event.type == pygame.QUIT:
            is_running = False

        # Press keys event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -0.3
            if event.key == pygame.K_RIGHT:
                player_x_change = 0.3
            if event.key == pygame.K_UP:
                player_y_change = -0.3
            if event.key == pygame.K_DOWN:
                player_y_change = 0.3
            if event.key == pygame.K_SPACE:
                missile_sound = mixer.Sound("shot.mp3")
                missile_sound.play()
                if not visible_missile:
                    missile_x = player_x
                    missile_y = player_y
                    shoot_missile(missile_x, missile_y)

        # Release key event
        if event.type == pygame.KEYUP:
            if event.type == pygame.KEYUP or event.key == pygame.K_RIGHT:
                player_x_change = 0
            if event.type == pygame.KEYUP or event.key == pygame.K_DOWN:
                player_y_change = 0

        if score != 0 and score % 5 == 0:
            score_sound = mixer.Sound("mixkit-fast-small-sweep-transition-166.wav")
            score_sound.play()
            enemy_x_change.append(0.5)

    # Modify player location
    player_x += player_x_change
    player_y += player_y_change

    # Keep player inside screen
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736
    elif player_y <= 0:
        player_y = 0
    elif player_y >= 536:
        player_y = 536

    # Modify enemy location
    for enem in range(number_of_enemies):
        # End of game
        if enemy_y[enem] > 500:
            for k in range(number_of_enemies):
                enemy_y[k] = 1000
            final_text()
            break
        enemy_x[enem] += enemy_x_change[enem]
        if enemy_x[enem] <= 0:
            enemy_x_change[enem] = 0.2
            enemy_y[enem] += enemy_y_change[enem]
        elif enemy_x[enem] >= 736:
            enemy_x_change[enem] = -0.2
            enemy_y[enem] += enemy_y_change[enem]

        # Collision
        collision = there_is_a_collision(enemy_x[enem], enemy_y[enem], missile_x, missile_y)
        if collision:
            collision_sound = mixer.Sound("punch.mp3")
            collision_sound.play()
            missile_y = 500
            visible_missile = False
            score += 1
            enemy_x[enem] = random.randint(0, 736)
            enemy_y[enem] = random.randint(40, 200)

        enemy(enemy_x[enem], enemy_y[enem], enem)



    # Bullet movement
    if missile_y <= -64:
        missile_y = player_y
        visible_missile = False
    if visible_missile:
        shoot_missile(missile_x, missile_y)
        missile_y -= missile_y_change


    player(player_x, player_y)

    show_score(text_x,text_y)
    show_enemy_speed(enemy_score_text_x, enemy_score_text_y)


    # Update
    pygame.display.update()





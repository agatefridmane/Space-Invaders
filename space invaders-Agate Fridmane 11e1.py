import pygame
import random
import math
import time
from collections import deque


##### Spēles inicializācija###########################################
pygame.init()

### Game Window
## Uztaisit spēles ekranu ar noteiktu izmeru (W x H)
screen = pygame.display.set_mode((800, 600))

### Background img
background = pygame.image.load('background.jpg')
### Nosaukums un Ikona
pygame.display.set_caption("Space Invaders")
## https://www.flaticon.com/search?word=spaceship&type=icon&order_by=4
## Ikonas izmers 32x32
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

### Player
playerX_change = 0
## Priekš šī loga izmēra 'player.png' - 64x64 px
playerImg = pygame.image.load('player.png')
# playerImg = pygame.draw.rect(screen, (0,255,0), pygame.Rect(0,0, 64, 64)) # taisntūra placehoder ar pareizo izmēru
playerX = 370
playerY = 480

### Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append( pygame.image.load('enemy.png') )
    enemyX.append( random.randint(0,735) )
    enemyY.append( random.randint(50,150) )
    enemyX_change.append(0.3)
    enemyY_change.append(40)

start_time = time.time()

current_time = time.time()
if current_time - start_time >= 2:
    for i in range(num_of_enemies):
        # Generate a random factor to change the movement speed
        speed_factor = random.uniform(0.01, 1.0)  # You can adjust the range of speed change

        # Apply the random factor to the current movement speed
        enemyX_change[i] *= speed_factor

    # Reset the start time
    start_time = current_time

## Priekš šī loga izmēra 'enemy.png' - 64x64 px
# enemyImg = pygame.image.load('enemy.png')

### Boss
bossImg = pygame.image.load('boss.png')
bossX = random.randint(0,735)
bossY = 150
bossX_change = 0.3  # Adjust this value as per your desired boss movement speed
bossY_change = 0
boss_health = 15
boss_appear_score = 50
boss_state = "ready"
boss_win = False

boss_textx = 10
boss_texty = 35

if bossX <= 0:
    bossX_change = abs(bossX_change)  # Ensure positive speed
elif bossX >= 736:
    bossX_change = -abs(bossX_change)  # Ensure negative speed

# bossX += bossX_change

### Boss bullets
bossbulletImg = pygame.image.load('bossbullet.png')
boss_bullet_state = "ready"
bossbulletX = 0
bossbulletY = 480
bossbulletX_change = 0
bossbulletY_change = 0.8  



### Obsticle
obstacleImg = pygame.image.load('obstacle.png')
obstacleX = random.randint(50, 750)
obstacleY = random.randint(200, 400)

### Bullet
## priekš šī loga izmēra 'bullet.png' - 32x32 px
## 'ready' - nevar redzēt lodi uz ekrāna
## 'fire' - lode šobrīd kustās
# bulletImg = pygame.image.load('bullet.png')

# bulletImg = pygame.draw.rect(screen, (255,255,0), pygame.Rect(0, 0, 32, 32)) # taisntūra placehoder ar pareizo izmēru
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 3     

bullet_state = "ready"

### Rezultāts (Font)
score = 49
## Lai pievienot savu fontu, lejupieladēt un ievietot projekta mapē
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10  
textY = 10

### Game Over text
over_font = pygame.font.Font('defused.ttf', 64)

##### Funkcijas#####################################################

def player(x,y):
    ## .blit() - zīmēt uz ekrana
    screen.blit(playerImg, (x, y))
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def boss(x, y):
    screen.blit(bossImg, (x, y))

def obstacle(x, y):
    screen.blit(obstacleImg, (x, y))

def fire_bullet(x, y):
 ## bullet_state ir nepieciešams definēt kā globālo, laifunkcija varētu mainīt to vertību
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def boss_actions():
    global boss_state, boss_bullet_state, bossX, bossY, boss_health, bossbulletX, bossbulletY, bossX_change

    if score >= boss_appear_score and boss_state == "ready":
        boss_state = "appear"
        bossX = 0
        bossY = 50

    if boss_state == "appear":
        # Move boss horizontally
        bossX += bossX_change
        if bossX <= 0:
            bossX = 0
            bossX_change = 0.3  # Move right
        elif bossX >= 736:
            bossX = 736
            bossX_change = -0.3  # Move left

        # Boss shooting logic
        if boss_bullet_state == "ready":
            bossbulletX = bossX + 16  # Set bullet's initial X position to boss's center
            bossbulletY = bossY + 30  # Set bullet's initial Y position to slightly below the boss's top
            boss_bullet_state = "fire"
# Function to handle boss's bullets
def boss_fire(x, y):
    global boss_bullet_state
    screen.blit(bossbulletImg, (x + 16, y + 10))

# Function to check collision between player and boss's bullets
def isPlayerHitByBossBullet(playerX, playerY, bossbulletX, bossbulletY):
    distance = math.sqrt(math.pow(playerX - bossbulletX, 2) + math.pow(playerY - bossbulletY, 2))
    if distance < 27:
        return True
    else:
        return False

def isCollisionBoss(bossX, bossY, bulletX, bulletY):
    distance = math.sqrt((math.pow(bossX - bulletX, 2)) + (math.pow(bossY - bulletY, 2)))
    if distance < 40:
        return True
    else:
        return False

def isCollision(enemyX, enemyY, bulletX, bulletY):
## distance between two coordinates mathplanet
## https://www.mathplanet.com/education/algebra-2/conicsections/distance-between-two-points-and-the-midpoint
    distance = math.sqrt( math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY,2) )
    if distance < 27:
        return True
    else:
        return False
    

    
# def enemy(x, y, i):
#     screen.blit(enemyImg[i], (x, y))

def show_score(x, y):
    ## Sakumā tekstu ir jānorenderē, un pēc tam uzzīmēt ar .blit()
    scoreValue = font.render("Score : " + str(score), True, (0, 255, 230) )
    screen.blit(scoreValue, (x, y) )

def show_boss_health(x, y):
    scoreValue = font.render("Boss health : " + str(boss_health), True, (204, 153, 255) )
    screen.blit(scoreValue, (x, y) )

def game_over_text():
    over_text = over_font.render( "GAME OVER", True, (255, 255, 255) )
    screen.blit( over_text, (200, 250) )

def boss_fire(x, y):
    global boss_bullet_state
    screen.blit(bossbulletImg, (x + 16, y + 10))




## Visas darbības spēlē (notikumi) saucas par Events
## Loga aizvēršana arī ir events - Quit event

boss_battle = False

##### Game Loop#####################################################
running = True
while running:
    ### Background fill
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
######################################################################
        ### Spēlētāja pārzīmēšana
    
        ### Keyboard sensing
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        ### Pogas palaišana
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Move player
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Draw player
    player(playerX, playerY)

    # Draw enemies and handle their collision with bullets
    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            # running = False
            break
        if boss_win == True:
            boss_battle = False
            game_over_text()    
            break


        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = abs(enemyX_change[i])
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -abs(enemyX_change[i])
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i], enemyY[i], i)

    # Draw obstacle
    obstacle(obstacleX, obstacleY)

    # Draw boss
      

    if score % 50 == 0 and score != 0:
        boss_battle = True
        
    
    if boss_battle:
        boss(bossX, bossY)
        # Boss actions
        boss_actions()
        show_boss_health(boss_textx, boss_texty)

        # Handle boss bullets
        if boss_bullet_state == "fire":
            boss_fire(bossbulletX, bossbulletY)
            bossbulletY += bossbulletY_change
            # Check collision with player
            hit = isPlayerHitByBossBullet(playerX, playerY, bossbulletX, bossbulletY)
            if hit:
                
                boss_win = True
                # running = False
                # break
            if bossbulletY >= 600:
                bossbulletY = bossY
                boss_bullet_state = "ready"

        # Check collision between player bullet and boss
        bullet_hit_boss = isCollisionBoss(bossX, bossY, bulletX, bulletY)
        if bullet_hit_boss and bullet_state == "fire":  # Check if bullet is fired
            bulletY = 480
            bullet_state = "ready"
            boss_health -= 1
            if boss_health == 0:
                score += 15  
                boss_health = 15# Increment the score if the boss is defeated
                # boss_state = "ready"  # Reset boss state
                boss_battle = False

    # Handle bullet movement and collision with obstacle
    if bulletY <= 0 :
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if bulletY <= obstacleY + 64 and bulletY >= obstacleY:
        if bulletX + 20 >= obstacleX and bulletX + 20 <= obstacleX + 64:  
            bulletY = 480
            bullet_state = "ready"

    if bossbulletY <= obstacleY + 64 and bossbulletY >= obstacleY:
        if bossbulletX + 30 >= obstacleX and bossbulletX + 30 <= obstacleX + 64: 
            bulbossbulletYletY = 480
            boss_bullet_state = "ready"

    

    # Show score
    show_score(textX, textY)
    

    # Refresh display
    pygame.display.update()

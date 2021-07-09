# Bismillah - AbubakarQ

import pygame
import os # Helps find the path for operation system
pygame.font.init() # imports fonts into the system
pygame.mixer.init() # imports sounds

# Window size
WIDTH, HEIGHT = 900, 500
# Establishes window size
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# Establishes Window Title
pygame.display.set_caption("Abubakar's First Game!")

# Window Background
WHITE = (255, 255, 255)
# Border Color
BLACK = (0, 0, 0)
# Bullet color
RED = (255, 64, 64)
BLUE = (21, 244, 238)
# Winner Color
N_GREEN = (57, 255, 20)
# Velocity of speed change
VEL = 7
# Frames per Second
FPS = 60
# Border between spaceships
BORDER = pygame.Rect((WIDTH//2)-5, 0, 10, HEIGHT)
# Bullet Velocity
BULLET_VEL = 10
# Bullet Ammo
MAX_BULLET = 3
# Font
HEALTH_FONT = pygame.font.SysFont('OCR A Std', 20)
WINNER_FONT = pygame.font.SysFont('OCR A Std', 90)
EE_FONT = pygame.font.SysFont('Assassin$', 30)

### SOUND EFFECTS ### 
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'hit.wav'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'shoot.wav'))
WINNER_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'gameover.mp3'))

# Creating bullet events to cause hit
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


# spaceship size
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

### IMPORTING IMAGES ###
# import yellow (Left) spaceship 
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
# import red (Right) spaceship
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
# import space background
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))
EE_IMAGE = pygame.image.load(os.path.join('Assets', 'EE.png'))
EE = pygame.transform.scale(EE_IMAGE, (300, 300))

# Draws the window function
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # Function to refresh within each loop: WIN.fill(WHITE) - set to white background
    # Function for background image: 
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    # Drawing font under spaceships
    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    # blit spaceships
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    # Bullet drawing
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, BLUE, bullet)
    pygame.display.update()

def yellow_handle_movment(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # LEFT
            yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: # RIGHT
            yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # UP
            yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT: # DOWN
            yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # LEFT
            red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # RIGHT
            red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # UP
            red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT: # DOWN
            red.y += VEL
    
# Handling bullets function
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    # Creating bullet function for shooting FROM yellow
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    # Creating bullet function for shooting FROM Red
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

# Drawing winnner
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, N_GREEN)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT/2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

# Drawing Easter Egg
def draw_EE(text):
    draw_text = EE_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, 10))
    draw_text = EE_FONT.render(text, 1, RED)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, 20))
    draw_text = EE_FONT.render(text, 1, BLUE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, 30))
    WIN.blit(EE, (WIDTH//2 - EE.get_width()//2, HEIGHT//2 - EE.get_height()//2))

    pygame.display.update()
    pygame.time.delay(3000)


    
# main loop 
def main():
    yellow = pygame.Rect(100, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock() # CLock object 
    run = True # While true game will run 
    while run:
        clock.tick(FPS) # Sets up frames per second
        for event in pygame.event.get(): 

            # If statment to neutralize game window
            if event.type == pygame.QUIT:
                run = False
                pygame.quit() 

            # Shooting bullets
            if event.type == pygame.KEYDOWN:
                # Yellow bullet
                if event.key == pygame.K_LSHIFT and len(yellow_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                # Red Bullet
                if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                # Easter Egg button Activate
                if event.key == pygame.K_7:
                    EE_text = "EASTER EGG FOUND! :)"
                    draw_EE(EE_text)

                    

            # Red Health
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            
            # Yellow Health
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        # Scoreboard 
        winner_text = ""
        if red_health  <= 0:
            winner_text = "Yellow Wins!"
            WINNER_SOUND.play()

        if yellow_health <= 0:
            winner_text = "Red Wins!"
            WINNER_SOUND.play()
        
        if winner_text != "":
            draw_winner(winner_text)
            break

        # Mapping keyboard to game
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movment(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()

if __name__ == "__main__":
    main()
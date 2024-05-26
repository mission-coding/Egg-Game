import pygame
import random
import sys

# Initialize Pygame modules
pygame.init()
pygame.mixer.init()

# Screen setup
screen_w = 800
screen_h = 600
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("Egg Game")

# Colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
skyblue = (135, 206, 235)
brown = (150, 75, 0)

# Load images and transform their size
bg_img = pygame.image.load("gallery/bg.jpg").convert_alpha()
bg_img = pygame.transform.scale(bg_img, (screen_w, screen_h))

egg_img = pygame.image.load("gallery/egg.png").convert_alpha()
egg_img = pygame.transform.scale(egg_img, (30, 40))

basket_img = pygame.image.load("gallery/basket.png").convert_alpha()
basket_img = pygame.transform.scale(basket_img, (90, 60))

hen_img = pygame.image.load("gallery/hen.png").convert_alpha()
hen_img = pygame.transform.scale(hen_img, (110, 110))

egg_cracked_img = pygame.image.load("gallery/egg_cracked.png").convert_alpha()
egg_cracked_img = pygame.transform.scale(egg_cracked_img, (90, 65))

life_img = pygame.image.load("gallery/life.png").convert_alpha()
life_img = pygame.transform.scale(life_img, (35, 45))

# Load sounds
catch_sound = pygame.mixer.Sound("gallery/egg_catched.wav")
crack_sound = pygame.mixer.Sound("gallery/egg_cracked.mp3")
over_sound = pygame.mixer.Sound("gallery/game_over.wav")

# Function to draw text on the screen
def draw_text(text, color, size, x, y):
    font = pygame.font.Font(None, size)
    display_text = font.render(text, True, color)
    screen.blit(display_text, [x, y])

# Player class to manage player attributes and actions
class Player():
    def __init__(self) -> None:
        self.w = 90
        self.h = 50
        self.x = screen_w / 2 - self.w / 2
        self.y = screen_h - 80
        self.speed = 15

    def draw(self):
        self.hitbox = (self.x, self.y, self.w, self.h)
        screen.blit(basket_img, [self.x, self.y])

    def move(self):
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_LEFT]:
            self.x -= self.speed
        if self.keys[pygame.K_RIGHT]:
            self.x += self.speed

        # Prevent the player from moving out of screen bounds
        if self.x <= 0:
            self.x = 0
        if self.x >= screen_w - self.w:
            self.x = screen_w - self.w

# Egg class to manage egg attributes and actions
class Egg():
    def __init__(self, x) -> None:
        self.w = 30
        self.h = 40
        self.x = x
        self.y = 100
        self.speed = 5
        self.cracked = False
        self.crack_time = 0

    def draw(self):
        if not self.cracked:
            self.hitbox = (self.x, self.y, self.w, self.h)
            screen.blit(egg_img, [self.x, self.y])
        else:
            screen.blit(egg_cracked_img, [self.x - 40, self.y])

    def move(self):
        if not self.cracked:
            self.y += self.speed

# Main game loop
def game_loop():
    # Global variables
    player = Player()
    clock = pygame.time.Clock()
    fps = 30
    count = 0
    eggs = []
    distances = [114 * i for i in range(0, 7)]
    score = 0
    lives = 5
    over = False

    # Play background music
    pygame.mixer.music.load("gallery/bgsound.mp3")
    pygame.mixer.music.play(-1)

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        with open("gallery/hiscore.txt", "r") as f:
            hiscore = int(f.read())

        screen.blit(bg_img, [0, 0])

        count += 1
        # Add new eggs at intervals
        if count > 40:
            eggs.append(Egg(random.choice(distances) + 40))
            count = 0

        for egg in eggs[:]:
            egg.draw()
            egg.move()
            if egg.cracked:
                if pygame.time.get_ticks() - egg.crack_time >= 2000:
                    eggs.remove(egg)
            else:
                if player.hitbox[1] + player.hitbox[3] > egg.hitbox[1] > player.hitbox[1]:
                    if player.hitbox[0] < egg.hitbox[0] < player.hitbox[0] + player.hitbox[2]:
                        eggs.remove(egg)
                        score += 1
                        catch_sound.play()
                    else:
                        egg.cracked = True
                        egg.crack_time = pygame.time.get_ticks()
                        lives -= 1
                        crack_sound.play()

        player.draw()
        player.move()

        # Draw the ground line
        pygame.draw.rect(screen, brown, [0, 140, screen_w, 13])

        # Draw hens on the screen
        for i in distances:
            screen.blit(hen_img, [i, 60])

        if score >= hiscore:
            hiscore = score

        draw_text(f"Hi-score: {hiscore}   Score: {score}", black, 30, 15, 15)

        # Draw lives on the screen
        for i in range(1, 6):
            if lives == i or i < lives <= 5:
                screen.blit(life_img, [screen_w- 40*i, 8])

        if lives == 0:
            over = True
            # over_sound.play()
        
        if over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.mixer.music.stop()
            player.speed = 0
            for egg in eggs:
                egg.speed = 0
            draw_text("Game Over!", red, 40, screen_w/2-80, screen_h/2-40)
            draw_text("Press enter to play again", black, 30, screen_w/2-127, screen_h/2)
            
            with open("gallery/hiscore.txt", "w") as f:
                f.write(str(hiscore))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_loop()
        clock.tick(fps)
        pygame.display.update()

# Start the game
game_loop()

import pygame
from random import randint
from os.path import join

bounce_off_flag = 0
kill_count = 0

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, 100), randint(0, 100)))
        self.direction = pygame.math.Vector2()
        self.speed = 400
        self.can_jump = True
        self.is_jumping = False
        self.jump_start = 0
        self.jump_lifespan = 1000
    
    def update(self, dt, player_x, player_y):
        global bounce_off_flag
        keys = pygame.key.get_pressed()
        recent_keys = pygame.key.get_just_pressed()
        if self.rect.left < 0:
            self.rect.left = 0
            self.rect.left += 1
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
            self.rect.right -= 1
        if self.rect.top < 0:
            self.rect.top = 0
            self.rect.top += 1
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.rect.bottom -= 1
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        if not self.is_jumping:
            self.direction.y = 2
        if recent_keys[pygame.K_SPACE] and self.can_jump:
            self.can_jump = False
            self.is_jumping = True
            self.jump_start = pygame.time.get_ticks()
        if self.is_jumping:
            self.direction.y = 1.75 * (2 * (pygame.time.get_ticks() - self.jump_start) / self.jump_lifespan - 1)
            if pygame.time.get_ticks() - self.jump_start > self.jump_lifespan:
                self.is_jumping = False
                self.can_jump = True
        if bounce_off_flag == 1:
            self.can_jump = False
            self.is_jumping = True
            self.jump_start = pygame.time.get_ticks()
            self.direction.y = (2 * (pygame.time.get_ticks() - self.jump_start) / (self.jump_lifespan / 2) - 1)
            if pygame.time.get_ticks() - self.jump_start > self.jump_lifespan:
                self.is_jumping = False
                self.can_jump = True
            bounce_off_flag = 0
        self.rect.center += self.direction * self.speed * dt

class Goomba(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2 * (pow(-1, randint(0, 1)) + 1), randint(0, WINDOW_HEIGHT - 50)))
        self.direction = pygame.math.Vector2()
        self.speed = 100
    
    def update(self, dt, player_x, player_y):
        global bounce_off_flag
        global kill_count
        if player_x <= self.rect.right + 1 and player_x >= self.rect.left - 1 and player_y >= self.rect.top and player_y <= self.rect.center[1]:
            self.kill()
            bounce_off_flag = 1
            kill_count += 1
        if self.rect.left < 0:
            self.rect.left = 0
            self.rect.left += 1
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
            self.rect.right -= 1
        if self.rect.top < 0:
            self.rect.top = 0
            self.rect.top += 1
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.rect.bottom -= 1
        if player_x != self.rect.center[0]:
            self.direction.x = (player_x - self.rect.center[0]) / abs(player_x - self.rect.center[0])
        self.direction.y = 10
        self.rect.center += self.direction * self.speed * dt

# General Setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Murder Game")
running = True
clock = pygame.time.Clock()

# Imports
player_surf = pygame.image.load(join("mario.png")).convert_alpha()
player_surf = pygame.transform.scale(player_surf, (100, 100))
goomba_surf = pygame.image.load(join("goomba.png")).convert_alpha()
goomba_surf = pygame.transform.scale(goomba_surf, (50, 50))
font = pygame.font.SysFont('Arial', 36)


# Sprites
all_sprites = pygame.sprite.Group()
goomba_sprites = pygame.sprite.Group()    
player = Player(all_sprites, player_surf)

running = True
while running:
    dt = clock.tick() / 1000

    # Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    goomps = 1
    if randint(0, 1000) % 500 == 0:
        for i in range(int(goomps)):
            goomba = Goomba(all_sprites, goomba_surf)
        goomps += 1

    all_sprites.update(dt, player.rect.center[0], player.rect.bottom)
    
    text = font.render(f"Kill Count: {kill_count}", True, (255, 255, 255))  # White color
    text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, 20))

    # Draw the Game
    display_surface.fill("#3A2E3F")
    all_sprites.draw(display_surface)
    display_surface.blit(text, text_rect)

    pygame.display.update()
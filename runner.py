import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load(
            'graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load(
            'graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load(
            'graphics/player/jump.png').convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_frame_1 = pygame.image.load(
                'graphics/fly/fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load(
                'graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 210
        else:
            snail_frame_1 = pygame.image.load(
                'graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load(
                'graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.coin = pygame.image.load('graphics/coin.png').convert_alpha()
        self.image = self.coin
        self.rect = self.image.get_rect(midbottom=(
            randint(900, 1100), randint(200, 300)))

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        while self.spawn_coins():
            self.rect.midbottom = (randint(900, 1200), 300)
        self.rect.x -= 6
        self.destroy()

    def spawn_coins(self):
        for obstacle in obstacle_group:
            if self.rect.colliderect(obstacle.rect):
                return True
        return False


def display_score():
    global coinscore
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    totalscore = current_time + coinscore
    score_surf = test_font.render(f'Score: {totalscore}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)

    coins_amount_surf = test_font.render(
        str(coinscore // 5), False, (111, 196, 169))
    coins_amount_rect = coins_amount_surf.get_rect(center=(730, 35))
    screen.blit(coins_amount_surf, coins_amount_rect)
    coin_icon_surf = pygame.image.load('graphics/coin.png').convert_alpha()
    coin_icon_rect = coin_icon_surf.get_rect(center=(770, 30))
    screen.blit(coin_icon_surf, coin_icon_rect)

    return totalscore


def collisions():
    global coinscore
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        coin_group.empty()
        return False
    elif pygame.sprite.spritecollide(player.sprite, coin_group, True):
        coinscore += 5
        return True
    return True


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
coinscore = 0

# GROUPS
# player
player = pygame.sprite.GroupSingle()
player.add(Player())

# obstacles
obstacle_group = pygame.sprite.Group()

# coins
coin_group = pygame.sprite.Group()

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()


# INTRO SCREEN
player_stand = pygame.image.load(
    'graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = test_font.render('Runner-game', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render('Press space to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 330))

# TIMERS
# timer for obstacles
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# timer for coins
coin_timer = pygame.USEREVENT + 2
pygame.time.set_timer(coin_timer, 3000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(
                    Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))

            if event.type == coin_timer:
                coin_group.add(Coin())

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
                coinscore = 0


# Peli päällä
    if game_active:
        screen.blit(ground_surf, (0, 300))
        screen.blit(sky_surf, (0, 0))

        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        coin_group.draw(screen)
        coin_group.update()

        game_active = collisions()

# Game over
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        score_message = test_font.render(
            f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 80))
        screen.blit(game_message, game_message_rect)

        if score == 0:
            screen.blit(game_name, game_name_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)

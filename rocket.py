import sys
import pygame
import random
from pygame.sprite import Sprite

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        pygame.display.set_caption('Moving Rocket')
        self.rocket = Rocket(self)
        self.obstacles = pygame.sprite.Group()
        self.obstacles_list = self.generate_obstacles()

    def run(self):
        while True:
            self._check_events()
            self.rocket.update()
            self._update_screen()
            self.clock.tick(60)

    def generate_obstacles(self):
        MARGIN = 50
        base_obstacle = Obstacles(self)
        x = base_obstacle.rect.x + 10
        while x < self.screen_width:
            new_obstacle = Obstacles(self)
            new_obstacle.rect.x = x
            new_obstacle.rect.y = new_obstacle.starting_position
            self.obstacles.add(new_obstacle)
            x += MARGIN
        
    def shit(self):
        obstacles_list = []
        MARGIN = 50
        image = pygame.image.load('assets/Bullet_1.bmp')
        x = image.get_rect().x
        while x < self.screen_width:
            obs = {
                'img': 'assets/Bullet_1.bmp',
                'x': x + 10,
                'y': 50
            }
            obstacles_list.append(obs)
            x += MARGIN
        return obstacles_list

    def _update_screen(self):
        self.screen.fill(self.bg_color)
        self.rocket.blitme()
        self.obstacles.draw(self.screen)
        self.obstacles.update()
        pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_key_down(event)
            elif event.type == pygame.KEYUP:
                self._check_key_up(event)
    
    def _check_key_down(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
            self.rocket.horizontal_movement = event.key
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            self.rocket.vertical_movement = event.key
    
    def _check_key_up(self, event):
        if event.key == self.rocket.horizontal_movement:
            self.rocket.horizontal_movement = ''
        if event.key == self.rocket.vertical_movement:
            self.rocket.vertical_movement = ''

class Rocket:
    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.image = pygame.image.load('assets/player.bmp')
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        self.vertical_movement = ''
        self.horizontal_movement = ''
        self.speed = 3

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.horizontal_movement == pygame.K_RIGHT:
            self.rect.x += self.speed
        if self.horizontal_movement == pygame.K_LEFT:
            self.rect.x -= self.speed
        if self.vertical_movement == pygame.K_UP:
            self.rect.y -= self.speed
        if self.vertical_movement == pygame.K_DOWN:
            self.rect.y += self.speed

class Obstacles(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.screen_height = game.screen_height
        self.image_index = 0
        self.image = pygame.image.load(f'assets/Bullet_{self.image_index}.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.starting_position = random.randint(-abs(self.screen_height), 0)
        self.fall_speed = 2
    
    def update(self):
        if self.image_index == 7:
            self.image_index = 0
        self.image = pygame.image.load(f'assets/Bullet_{self.image_index}.bmp')
        self.image_index += 1

        if self.rect.y > self.screen_height:
            self.rect.y = 0 - self.image.get_rect().height
        else:
            self.rect.y += self.fall_speed


if __name__ == '__main__':
    game = Game()
    game.run()
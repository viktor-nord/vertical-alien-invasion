import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = pygame.image.load('images/enemyShip.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.y = float(self.rect.y)
    
    def update(self):
        self.y += self.settings.alien_speed * self.settings.fleet_dir
        self.rect.y = self.y
    
    def check_edges(self):
        return (self.rect.bottom >= self.settings.screen_height) or (self.rect.top <= 0)
    
    def center_ship(self):
        self.rect.midleft = self.screen.midleft
        self.y = float(self.rect.y)

    def blitme(self):
        self.screen.blit(self.image, self.rect)
    
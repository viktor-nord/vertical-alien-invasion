import sys
import pygame
from random import randint, choice
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.game_active = True
        if self.settings.fullscreen:
            wh = (0, 0)
            f = pygame.FULLSCREEN
        else:
            wh = (self.settings.screen_width, self.settings.screen_height)
            f = 0
        self.screen = pygame.display.set_mode(wh, f)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Target Practice')
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.star_pattern = self._generate_star_pattern()
        self.alien = Alien(self)
        self.stars = pygame.sprite.Group()

    def run_game(self):
        while True:
            if self.game_active:
                self._check_events()
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_screen()
                self.clock.tick(60)

    def reset(self):
        if self.stats.lives > 0:
            sleep(0.5)
            self.stats.lives -= 1
            self.bullets.empty()
            sleep(0.5)
        else:
            self.game_active = False

    #Helper Methods
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self._add_stars()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.alien.blitme()
        self.ship.blitme()
        pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_key_events(event.key, True)
            elif event.type == pygame.KEYUP:
                self._check_key_events(event.key, False)
                 
    def _generate_star_pattern(self):
        pattern = []
        MARGIN = 100
        star_image = pygame.image.load('images/starBig.bmp')
        # star_image.get_rect() = (0, 0, 23, 21)
        x_count, y_count, width, height = star_image.get_rect()
        while y_count < self.settings.screen_height:
            while x_count < self.settings.screen_width:
                star = {
                    'img': choice(['images/starBig.bmp', 'images/starSmall.bmp']), 
                    'x': randint(x_count, x_count + MARGIN - width),
                    'y': randint(y_count, y_count + MARGIN - height)
                }
                pattern.append(star)
                x_count += MARGIN
            y_count += MARGIN
            x_count = 0
        return pattern

    def _add_stars(self):
        for star in self.star_pattern:
            img = pygame.image.load(star['img'])
            self.screen.blit(img, (star['x'], star['y']))

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens) or self._check_alien_left():
            self.reset()
    
    def _check_fleet_edges(self):
        if self.alien.check_edges():
            self.settings.fleet_dir *= -1

    def _check_alien_left(self):
        is_game_over = False
        for alien in self.aliens:
            if alien.rect.left <= 0:
                is_game_over = True
        return is_game_over

    def _check_key_events(self, key, is_key_down):
        if key == pygame.K_RIGHT:
            self.ship.moving_right = is_key_down
        elif key == pygame.K_LEFT:
            self.ship.moving_left = is_key_down
        elif key == pygame.K_q:
            sys.exit()
        elif key == pygame.K_SPACE and is_key_down: 
            self._fire_bullet()

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, self.settings.not_super_bullet, True
        )
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()


    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        fleet_width = alien_width * 2
        fleet_height = alien_height
        while fleet_height < (self.settings.screen_height - 2 * alien_height):
            while fleet_width < (self.settings.screen_width - alien_width):
                self._create_alien(fleet_width, fleet_height)
                fleet_width += 2 * alien_width
            fleet_width = alien_width * 2
            fleet_height +=2 * alien_height

    def _create_alien(self, x, y):
        new_alien = Alien(self)
        new_alien.y = y
        new_alien.rect.x = x
        new_alien.rect.y = y
        self.aliens.add(new_alien)


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
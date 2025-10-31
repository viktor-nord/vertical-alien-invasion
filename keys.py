import sys
import pygame

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.clock = pygame.time.Clock()
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        pygame.display.set_caption('Key Display')
        self.text = ''
        self.title_screen = self.my_font.render('Press Any Key', False, (0, 0, 0))
        self.text_screen = self.my_font.render(self.text, False, (0, 0, 0))

    def run(self):
        while True:
            self._check_events()
            self._update_screen()
            self.clock.tick(60)

    def _update_screen(self):
        self.screen.fill(self.bg_color)
        self.screen.blit(self.title_screen, (0,0))
        self.screen.blit(self.text_screen, (0,50))
        pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.text += event.dict['unicode'] + ' '
                self.text_screen = self.my_font.render(self.text, False, (0, 0, 0))
    

if __name__ == '__main__':
    game = Game()
    game.run()
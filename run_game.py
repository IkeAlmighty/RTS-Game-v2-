import pygame_boilerplate.engine as engine
import pygame


class Game(engine.Engine):

    def preload(self):
        """"""

    def loop(self):
        """"""

        for event in pygame.event.get():
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                self.running = False

    def cleanup(self):
        """"""


game = Game()
game.start([800, 600])
import pygame_boilerplate.engine as engine
import pygame


class Game(engine.Engine):

    def preload(self):
        self.eventcache = engine.EventCache()

    def loop(self):
        self.eventcache.update()

        if self.eventcache.key_up(pygame.K_ESCAPE):
            self running = False

    def cleanup(self):
        """"""

def main():
    game = Game()
    game.start([800, 600])

main()
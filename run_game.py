import pygame_boilerplate.engine as engine
import pygame, components.renders


class Game(engine.Engine):

    def preload(self):
        self.ui = components.renders.RenderGroup()

        self.ui.add(engine.Button(topleft=(0, 0), text="Quit"), "quit_button")
        
        button = engine.Button(text="HELLO")
        button.rect.topleft = (self.screen_size[0] - button.rect.width, 0)
        self.ui.add(button, "hello_button")

    def loop(self):
        
        #UPDATING:
        self.eventcache.update()
        self.ui.update()


        #CONTROL LOGIC:
        if self.eventcache.key_up(pygame.K_ESCAPE):
            self.running = False

        if self.ui.get_by_id("quit_button").is_pressed():
            self.running = False
        

        #RENDERING:
        for button in self.ui:
            self.render_later(button)

    def cleanup(self):
        """"""

def main():
    game = Game()
    game.start([800, 600])

main()
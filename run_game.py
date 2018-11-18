import pygame_boilerplate.engine as engine
import pygame, components.renders, gamemap


class Game(engine.Engine):

    def preload(self):
        self.ui = components.renders.RenderGroup()
        
        button = engine.Button(text="QUIT GAME")
        button.rect.topleft = (self.screen_size[0] - button.rect.width, 0)
        self.ui.add(button, "quit_button")

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
        self.ui.render_later(self)


    def cleanup(self):
        print("GOODBYE!")

def main():
    game = Game()
    game.start([800, 600])

main()
import pygame_boilerplate.engine as engine
import pygame, components.renders, gamemap


class Game(engine.Engine):

    def preload(self):
        self.ui = components.renders.RenderGroup()
        
        button = engine.Button(text="QUIT GAME")
        button.rect.topleft = (self.screen_size[0] - button.rect.width, 0)
        self.ui.add(button, "quit_button")

        self.gamemap = gamemap.GameMap(size=(1000, 1000))
        self.scrollmap = components.renders.ScrollMapRender(self.gamemap, pygame.Rect((100, 100), self.screen_size), square_width=1, scrollspeed=8)

    def loop(self):
        
        #UPDATING:
        self.eventcache.update()
        self.ui.update()
        self.scrollmap.update()


        #CONTROL LOGIC:
        if self.eventcache.key_up(pygame.K_ESCAPE):
            self.running = False

        if self.ui.get_by_id("quit_button").is_pressed():
            self.running = False
        

        #RENDERING:
        self.ui.render_later(self)
        self.render_later(self.scrollmap)


    def cleanup(self):
        print("GOODBYE!")

def main():
    game = Game()
    game.start([400, 300], pygame.FULLSCREEN)

main()
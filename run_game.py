import pygame_boilerplate.engine as engine
import pygame, components.renders, gamemap


class Game(engine.Engine):

    def preload(self):
        self.gamemap = gamemap.GameMapGenerator(size=(1000, 1000), percent_water=0.4, percent_mountain=0.4)

        square_width = 3
        self.bscrollmap = components.renders.BufferedScrollMap((0, 0), self.gamemap, square_width, scrollspeed=15)

        #UI Stuff
        self.ui = components.renders.RenderGroup()
        
        button = engine.Button(text="QUIT GAME")
        button.rect.topleft = (self.screen_size[0] - button.rect.width, 0)

        minimap_pos = (0, self.screen_size[1] - 200)
        minimap = components.renders.MiniMap(self.bscrollmap, pygame.Rect(minimap_pos, (200, 200)))
        
        self.ui.add(button, "quit_button")
        self.ui.add(minimap, "minimap")

    def loop(self):
        
        #UPDATING:
        self.eventcache.update()
        self.ui.update()
        self.bscrollmap.update()


        #CONTROL LOGIC:
        if self.eventcache.key_up(pygame.K_ESCAPE):
            self.running = False

        if self.ui.get_by_id("quit_button").is_pressed():
            self.running = False
        

        #RENDERING:
        self.render_later(self.bscrollmap) #this is the base tile, so it needs rendered first
        self.ui.render_later(self)

        #position of the scrollmap
        self.render_later(components.renders.SurfRender(self.font.render(self.bscrollmap.get_pos().__str__(), True, (255, 255, 255), (0, 0, 0)), (0, 0)))
        

    def cleanup(self):
        print("Goodbye")

def main():
    game = Game()
    game.start([800, 600], pygame.FULLSCREEN, font_size=16)

main()
import pygame_boilerplate.engine as engine
import pygame, components.renders, gamemap, entities


class Game(engine.Engine):

    def preload(self):
        self.gamemap = gamemap.GameMapGenerator(size=(1000, 1000), percent_water=0.4, percent_mountain=0.4)

        self.square_width = 3
        self.bscrollmap = components.renders.BufferedScrollMap((0, 0), self.gamemap, self.square_width, scrollspeed=15)

        #UI Stuff
        self.ui = components.renders.RenderGroup()
        
        exit_button = engine.Button(text="QUIT GAME")
        exit_button.rect.topleft = (self.screen_size[0] - exit_button.rect.width, 0)

        minimap_pos = (0, self.screen_size[1] - 200)
        minimap = components.renders.MiniMap(self.bscrollmap, pygame.Rect(minimap_pos, (200, 200)))
        
        self.ui.add(exit_button, "quit_button")
        self.ui.add(minimap, "minimap")

        self.entity_factory = entities.EntityFactory()
        self.entity_factory.add_class("tree")

    def loop(self):
        
        #UPDATING:
        self.eventcache.update()
        self.ui.update()
        self.bscrollmap.update()

        #CONTROL LOGIC:
        #rel mouse position update:
        rel_mouse_pos = (pygame.mouse.get_pos()[0] - self.bscrollmap.get_pos()[0], pygame.mouse.get_pos()[1] - self.bscrollmap.get_pos()[1])

        if self.eventcache.key_up(pygame.K_ESCAPE):
            self.running = False

        if self.ui.get_by_id("quit_button").is_pressed():
            self.running = False

        #for testing TODO: remove later
        if self.eventcache.mouse_pressed(0):
            e = self.entity_factory.create("tree", rel_mouse_pos)
            entities.add_entity(e)

        #RENDERING:
        self.render_later(self.bscrollmap) #this is the base tile, so it needs rendered first
        #should be noted that gamebox provides render_to_scrollmap to render entities
        self.ui.render_later(self)

        #position of mouse on the the scrollmap
        pos = rel_mouse_pos
        self.render_later(components.renders.SurfRender(self.font.render(pos.__str__(), True, (255, 255, 255), (0, 0, 0)), (0, 0)))
        

    def cleanup(self):
        pass

def main():
    import gamebox
    game = Game()
    gamebox.set_game(game)
    game.start([800, 600], 0, font_size=16)

main()
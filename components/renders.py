import sys
sys.path.append(".")
import pygame_boilerplate.engine as engine
import pygame


class RenderGroup:

    def __init__(self):
        self.__components = {}

    def add(self, renderable_component, id):
        self.__components[id] = renderable_component

    def update(self):
        for key in self.__components:
            self.__components[key].update()

    def get_by_id(self, id):
        return self.__components[id]

    def render_later(self, engine):
        for component in self.__components.values():
            engine.render_later(component)

    def __iter__(self):
        return self.__components.values().__iter__()

class ScrollMapRender(engine.RenderableComponent):

    def __init__(self, game_map, map_rect, square_width, scrollspeed=10):
        """Scroll speed is in pixels, map_rect is in squares as defined by square_width"""
        self.__map_rect = map_rect #this is in squares, not pixels
        self.__game_map = game_map #needed for the GameMap.get_rendering() method
        self.square_width = square_width

        self.__blit_surface = game_map.get_rendering(self.__map_rect, self.square_width)

        self.scrollspeed = scrollspeed #scroll speed in pixels, not squares

    def move_right(self):
        return
    
    def move_left(self):
        print("moveing left!")
        screen_size = pygame.display.get_surface().get_size()

        
        

    def move_up(self):
        return

    def move_down(self):
        return

    def get_image(self):
        return self.__blit_surface

    def get_pos(self):
        return (0, 0)

    def update(self):
        if pygame.mouse.get_pos()[0] < 5:
            self.move_right()

        if pygame.mouse.get_pos()[0] > pygame.display.get_surface().get_width() - 5:
            self.move_left()

        if pygame.mouse.get_pos()[1] < 5:
            self.move_down()

        if pygame.mouse.get_pos()[1] > pygame.display.get_surface().get_height() - 5:
            self.move_up()


def test():

    import gamemap

    game_map = gamemap.GameMap()

    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    rect = pygame.Rect(0, 0, 800, 600)
    scroll_map = ScrollMapRender(game_map, rect, square_width=5)

    screen.blit(scroll_map.get_image(), scroll_map.get_pos())

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type is pygame.KEYDOWN and event.key is pygame.K_ESCAPE:
                running = False
        
        scroll_map.update()

        screen.fill((0, 0, 0))
        screen.blit(scroll_map.get_image(), scroll_map.get_pos())
        pygame.display.flip()

test()
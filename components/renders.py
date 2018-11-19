import sys
sys.path.append(".")
import pygame_boilerplate.engine as engine
import pygame, numpy


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

    def __init__(self, game_map, map_rect, square_width, scrollspeed=15):
        """Scroll speed is in pixels, map_rect is in squares as defined by square_width"""
        self.__map_rect = map_rect #this is in squares, not pixels
        self.__game_map = game_map #needed for the GameMap.get_rendering() method
        self.square_width = square_width

        self.__blit_surface = game_map.get_rendering(self.__map_rect, self.square_width)

        self.scrollspeed = scrollspeed #scroll speed is in pixels, not squares

    def move_left(self):
        
        #roll the pixels on the __blit_surface
        surf_array = pygame.surfarray.pixels3d(self.__blit_surface)
        surf_array = numpy.roll(surf_array, -1*self.scrollspeed, axis=0)
        pygame.surfarray.blit_array(self.__blit_surface, surf_array)
        del surf_array

        #update map rect
        self.__map_rect.move_ip(self.scrollspeed//self.square_width, 0)

        #get the sliver surface for the new part of the screen.
        sliver_rect = pygame.Rect(
            self.__map_rect.topright[0] - self.scrollspeed//self.square_width, 
            self.__map_rect.topright[1], 
            self.scrollspeed//self.square_width,
            self.__map_rect.height
            )
        sliver = self.__game_map.get_rendering(sliver_rect, self.square_width)
        # import random
        # sliver.fill((random.randint(0, 255), 0, random.randint(0, 255)))

        #blit the sliver in the appropiate place, overwriting the pixels that rolled
        #around to the other side.
        pos = (pygame.display.get_surface().get_rect().topright[0] - self.scrollspeed, 0)
        self.__blit_surface.blit(sliver, pos)
    
    def move_right(self):

        #roll the pixels on the __blit_surface
        surf_array = pygame.surfarray.pixels3d(self.__blit_surface)
        surf_array = numpy.roll(surf_array, self.scrollspeed, axis=0)
        pygame.surfarray.blit_array(self.__blit_surface, surf_array)
        del surf_array

        #update map rect
        self.__map_rect.move_ip(-1*self.scrollspeed//self.square_width, 0)

        #get the sliver surface for the new part of the screen.
        sliver_rect = pygame.Rect(
            self.__map_rect.topleft[0], 
            self.__map_rect.topleft[1], 
            self.scrollspeed//self.square_width,
            self.__map_rect.height
            )
        sliver = self.__game_map.get_rendering(sliver_rect, self.square_width)
        # import random
        # sliver.fill((random.randint(0, 255), 0, random.randint(0, 255)))

        #blit the sliver in the appropiate place, overwriting the pixels that rolled
        #around to the other side.
        self.__blit_surface.blit(sliver, self.get_pos())

    def move_up(self):
        
        #roll the pixels on the __blit_surface
        surf_array = pygame.surfarray.pixels3d(self.__blit_surface)
        surf_array = numpy.roll(surf_array, -1*self.scrollspeed, axis=1)
        pygame.surfarray.blit_array(self.__blit_surface, surf_array)
        del surf_array

        #update map rect
        self.__map_rect.move_ip(0, self.scrollspeed//self.square_width)

        #get the sliver surface for the new part of the screen.
        sliver_rect = pygame.Rect(
            self.__map_rect.bottomleft[0], 
            self.__map_rect.bottomleft[1] - self.scrollspeed//self.square_width, 
            self.__map_rect.width,
            self.scrollspeed//self.square_width
            )
        sliver = self.__game_map.get_rendering(sliver_rect, self.square_width)
        # import random
        # sliver.fill((random.randint(0, 255), 0, random.randint(0, 255)))

        #blit the sliver in the appropiate place, overwriting the pixels that rolled
        #around to the other side.
        pos = (0, pygame.display.get_surface().get_height() - self.scrollspeed)
        self.__blit_surface.blit(sliver, pos)

    def move_down(self):
        
        #roll the pixels on the __blit_surface
        surf_array = pygame.surfarray.pixels3d(self.__blit_surface)
        surf_array = numpy.roll(surf_array, self.scrollspeed, axis=1)
        pygame.surfarray.blit_array(self.__blit_surface, surf_array)
        del surf_array

        #update map rect
        self.__map_rect.move_ip(0, -1*self.scrollspeed//self.square_width)

        #get the sliver surface for the new part of the screen.
        sliver_rect = pygame.Rect(
            self.__map_rect.topleft[0], 
            self.__map_rect.topleft[1], 
            self.__map_rect.width,
            self.scrollspeed//self.square_width
            )
        sliver = self.__game_map.get_rendering(sliver_rect, self.square_width)
        # import random
        # sliver.fill((random.randint(0, 255), 0, random.randint(0, 255)))

        #blit the sliver in the appropiate place, overwriting the pixels that rolled
        #around to the other side.
        pos = (0, 0)
        self.__blit_surface.blit(sliver, pos)

    def get_image(self):
        return self.__blit_surface

    def get_pos(self):
        return (0, 0)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        scr_width = pygame.display.get_surface().get_width()
        scr_height = pygame.display.get_surface().get_height()

        if mouse_pos[0] < 5:
            self.move_right()

        if mouse_pos[0] > scr_width - 5:
            self.move_left()

        if mouse_pos[1] < 5:
            self.move_down()

        if mouse_pos[1] > scr_height - 5:
            self.move_up()

def test():

    import gamemap

    game_map = gamemap.GameMap()

    pygame.init()
    screen = pygame.display.set_mode((400, 300), pygame.FULLSCREEN)

    rect = pygame.Rect(0, 0, 400//5, 300//5) #divide by the square width to get the actual pixel width
    scroll_map = ScrollMapRender(game_map, rect, square_width=5, scrollspeed=20)

    screen.blit(scroll_map.get_image(), scroll_map.get_pos())

    pygame.display.flip()

    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type is pygame.KEYDOWN and event.key is pygame.K_ESCAPE:
                running = False
        
        scroll_map.update()
        
        screen.blit(scroll_map.get_image(), scroll_map.get_pos())
        pygame.display.flip()
        
        clock.tick(60)


test()
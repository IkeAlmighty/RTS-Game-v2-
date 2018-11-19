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

    def __init__(self, game_map, map_rect, square_width, scrollspeed=5):
        """Scroll speed is in pixels, map_rect is in squares as defined by square_width"""
        self.__map_rect = map_rect #this is in squares, not pixels
        self.__game_map = game_map #needed for the GameMap.get_rendering() method
        self.square_width = square_width

        map_size = game_map.size
        
        self.__constr_x = self.__map_rect.center[0] - map_size[0]//2
        self.__constr_y = self.__map_rect.center[1] - map_size[1]//2

        self.__constr_w = self.__map_rect.center[0] + map_size[0]//2
        self.__constr_h = self.__map_rect.center[1] + map_size[1]//2

        self.__blit_surface = game_map.get_rendering(self.__map_rect, self.square_width)

        self.scrollspeed = scrollspeed #scroll speed is in pixels, not squares

    def __shift(self, scrollspeed, axis):
        #don't bother to call the method if the scrollspeed is 0
        if scrollspeed is 0:
            return 

        #return if the map has reached its bounds in a scroll direction.

        if axis is 0: #x axis
            if scrollspeed > 0: #aka shifting pixels left.
                if self.__map_rect.left < self.__constr_x: return
            else: #aka shifting pixels right
                if self.__map_rect.right > self.__constr_w: return
        else: #y axis
            if scrollspeed > 0: #aka shifting pixels up
                if self.__map_rect.top < self.__constr_y: return
            else: #aka shifting pixels down
                if self.__map_rect.bottom > self.__constr_h: return
        
        #roll the pixels on the __blit_surface
        surf_array = pygame.surfarray.pixels3d(self.__blit_surface)
        surf_array = numpy.roll(surf_array, scrollspeed*self.square_width, axis)
        pygame.surfarray.blit_array(self.__blit_surface, surf_array)
        del surf_array

        #update map rect
        if axis is 0: #(aka x axis)
            self.__map_rect.move_ip(-1*scrollspeed, 0)
        else: #axis is 1, aka y axis
            self.__map_rect.move_ip(0, -1*scrollspeed)

        #get the sliver surfaces for the new part(s) of the screen.
        sliver_rect = None
        if axis is 0: #x-axis
            if scrollspeed < 0:
                sliver_rect = pygame.Rect(
                    self.__map_rect.topright[0] - self.scrollspeed, 
                    self.__map_rect.topright[1], 
                    abs(scrollspeed),
                    self.__map_rect.height
                    )
            else: #scrollspeed must be > 0 (==0 returned already)
                sliver_rect = pygame.Rect(
                    self.__map_rect.topleft[0], 
                    self.__map_rect.topleft[1], 
                    scrollspeed,
                    self.__map_rect.height
                    )
        else: #y axis
            if scrollspeed < 0:
                sliver_rect = pygame.Rect(
                    self.__map_rect.bottomleft[0], 
                    self.__map_rect.bottomleft[1] - scrollspeed, 
                    self.__map_rect.width,
                    abs(scrollspeed)
                    )
            else: #scrollspeed must be > 0 (==0 returned already)
                sliver_rect = pygame.Rect(
                    self.__map_rect.topleft[0], 
                    self.__map_rect.topleft[1], 
                    self.__map_rect.width,
                    scrollspeed
                    )
        sliver = self.__game_map.get_rendering(sliver_rect, self.square_width)

        #find the blitting position based on what kind of scroll operation we did.
        pos = None
        if axis is 0:
            if scrollspeed < 0:
                pos = (pygame.display.get_surface().get_rect().topright[0] - abs(scrollspeed*self.square_width), 0)
            else:
                pos = (0, 0)
        else: #axis is 1 (aka the y axis)
            if scrollspeed < 0:
                pos = (0, pygame.display.get_surface().get_height() - abs(scrollspeed*self.square_width))
            else:
                pos = (0, 0)
        
        #blit the sliver in the appropiate place, overwriting the pixels that rolled
        #around to the other side.
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
            self.__shift(self.scrollspeed, axis=0)

        if mouse_pos[0] > scr_width - 5:
            self.__shift(-1*self.scrollspeed, axis=0)

        if mouse_pos[1] < 5:
            self.__shift(self.scrollspeed, axis=1)

        if mouse_pos[1] > scr_height - 5:
            self.__shift(-1*self.scrollspeed, axis=1)

def test():

    import gamemap

    game_map = gamemap.GameMap(size=(1000, 1000))

    pygame.init()
    squ_width = 1
    pysize = (400, 300)
    screen = pygame.display.set_mode(pysize)

    rect = pygame.Rect(0, 0, pysize[0]//squ_width, pysize[1]//squ_width) #divide by the square width to get the actual pixel width
    scroll_map = ScrollMapRender(game_map, rect, squ_width, (600, 600), scrollspeed=7)

    screen.blit(scroll_map.get_image(), scroll_map.get_pos())

    pygame.display.flip()

    running = True
    clock = pygame.time.Clock()
    while running:
        start_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type is pygame.KEYDOWN and event.key is pygame.K_ESCAPE:
                running = False
        
        scroll_map.update()
        
        screen.blit(scroll_map.get_image(), scroll_map.get_pos())
        pygame.display.flip()
        
        # print(pygame.time.get_ticks() - start_time)

        clock.tick(60)
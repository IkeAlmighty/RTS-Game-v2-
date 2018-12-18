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

class BufferedScrollMap(engine.Renderable):
    """This scroll map loads an entire finitely large map, to allow for faster scrolling."""

    def __init__(self, pos, game_map, square_width, scrollspeed):
        self.__game_map = game_map
        
        self.scrollspeed = scrollspeed

        self.__image_pos = [0, 0]

        rect = pygame.Rect(pos, game_map.size)

        self.__image = game_map.get_rendering(rect, square_width)

    def get_image(self):
        return self.__image

    def get_pos(self):
        return self.__image_pos.copy()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        screen_size = pygame.display.get_surface().get_size()

        if mouse_pos[0] < 5 and self.get_pos()[0] <= 0 - self.scrollspeed:
            self.__image_pos[0] += self.scrollspeed
        if mouse_pos[0] > screen_size[0] - 5 and self.get_pos()[0] >= 0 - (self.get_image().get_width() - screen_size[0] - self.scrollspeed):
            self.__image_pos[0] -= self.scrollspeed
        if mouse_pos[1] < 5 and self.get_pos()[1] <= 0 - self.scrollspeed: 
            self.__image_pos[1] += self.scrollspeed
        if mouse_pos[1] > screen_size[1] - 5 and self.get_pos()[1] >= 0 - (self.get_image().get_height() - screen_size[1] - self.scrollspeed):
            self.__image_pos[1] -= self.scrollspeed

    def blit(self, surface, pos):
        self.__image.blit(surface, pos)

class MiniMap(engine.Renderable):

    def __init__(self, scrollmap, rect):
        """passed: scrollmap - either a buffered scroll map or a ScrollMap Object
        rect - the position and size of the minimap in pixels"""

        self.__scrollmap = scrollmap
        self.__size = rect.size
        self.__pos = rect.topleft

        self.__visible = True

        self.update() #Called once on init to create the first frame to be rendered

    def hide(self):
        self.__visible = False

    def show(self):
        self.__visible = True

    def update(self):
        """Makes a new copy of the map each frame"""
        self.__image = pygame.transform.scale(self.__scrollmap.get_image(), self.__size)
        border = pygame.Surface((self.__image.get_size()[0] + 10, self.__image.get_size()[1] + 10))
        border.blit(self.__image, (5, 5))
        self.__image = border

        #create the frame for where you are looking right now:
        # frame = pygame.Surface()

    def get_image(self):
        return self.__image

    def get_pos(self):
        return self.__pos

class SurfRender(engine.Renderable):

    def __init__(self, surf, pos):
        self.surf = surf
        self.pos = pos

    def get_pos(self):
        return self.pos
    
    def get_image(self):
        return self.surf

    def update(self):
        pass
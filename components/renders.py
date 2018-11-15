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

    def __iter__(self):
        return self.__components.values().__iter__()
import sys, inspect, gamebox, pygame

def create_object(class_name, entity, center):
    """creates an object given a string of the class name, 
    returns None if the class type is not defined in this module"""
    
    physics_obj = None
    for name, obj_name in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if name == class_name: physics_obj = obj_name(entity, center)
    
    return physics_obj

#super class
class PhysicsComponent:
    """"""

    def __init__(self, entity, center):
        """"""
        self.entity = entity

        self.__rect = pygame.Rect(0, 0, 0, 0)
        self.__rect.center = center

    def update(self):
        """"""

    def get_pos(self):
        """"""
        return self.__rect.topleft

    def get_rect(self):
        """gets pygame.Rect object for this component"""
        size = self.entity.graphics.get_image().get_rect().size
        self.__rect = pygame.Rect(self.__rect.topleft, size)
        return self.__rect.copy()

##########DEFINE THE PHYSICS COMPONENT CLASSES AFTER THIS LINE##############
##All physics components must subclass entities.ControlComponent

class TreePhysics(PhysicsComponent):

    def __init__(self, entity, center):
        super().__init__(entity, center)
    
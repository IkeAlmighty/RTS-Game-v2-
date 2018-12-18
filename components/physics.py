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

        self.__center = center
        self.__rect = None

    def update(self):
        """"""

    def get_pos(self):
        """"""
        if self.__rect == None: self.get_rect()
        else: self.__center = self.__rect.center #makes sure the physicscomponent's center value is updated
        return self.__rect.topleft

    def get_rect(self):
        """gets pygame.Rect object for this component"""
        size = self.entity.graphics.get_image().get_rect().size

        if self.__rect == None:
            self.__rect = pygame.Rect((0, 0), size)    
            self.__rect.center = self.__center #then set the center! This is done because of lazy init,
            #the idea being that none of the class methods are called until all the entity components
            #are created.
        else:
            self.__rect = pygame.Rect(self.__rect.topleft, size)
            self.__center = self.__rect.center #make sure the physicscomponent's center value is updated!

        return self.__rect.copy()

##########DEFINE THE PHYSICS COMPONENT CLASSES AFTER THIS LINE##############
##All physics components must subclass entities.ControlComponent

class TreePhysics(PhysicsComponent):

    def __init__(self, entity, center):
        super().__init__(entity, center)
    
import sys, inspect, entities, gamebox

def create_object(class_name, entity):
    """creates an object given a string of the class name, 
    returns None if the class type is not defined in this module"""
    
    physics_obj = None
    for name, obj_name in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if name is class_name: physics_obj = obj_name(entity)
    
    return physics_obj

##########DEFINE THE PHYSICS COMPONENT CLASSES AFTER THIS LINE##############
##All physics components must subclass entities.ControlComponent

class TreePhysics(entities.PhysicsComponent):

    def __init__(self, entity):
        super().__init__(entity)
        

    
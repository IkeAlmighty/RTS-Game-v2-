import sys, inspect

def create_object(class_name):
    """creates an object given a string of the class name, 
    returns None if the class type is not defined in this module"""
    
    physics_obj = None
    for name, obj_name in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if name is class_name: physics_obj = obj_name()
    
    return physics_obj

class PhysicsComponent:

    def update(self):
        raise NotImplementedError("Concrete PhysicsComponent must overwrite update(self)")

    def get_pos(self):
        raise NotImplementedError("Concrete PhysicsComponent must overwrite get_pos(self)")

##########DEFINE THE PHYSICS COMPONENT CLASSES AFTER THIS LINE##############
    
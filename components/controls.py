import sys, inspect

def create_object(class_name):
    """creates an object given a string of the class name, 
    returns None if the class type is not defined in this module"""

    control_obj = None
    for name, obj_class in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if name is class_name: control_obj = obj_class()
    
    return control_obj

class ControlComponent:

    def __init__(self, entity):
        self.entity = entity

    def update(self):
        raise NotImplementedError("Concrete ControlComponent must overwrite update() method")

##########DEFINE THE CONTROL COMPONENT CLASSES AFTER THIS LINE##############
    
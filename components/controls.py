import sys, inspect, entities, gamebox

def create_object(class_name, entity):
    """creates an object given a string of the class name, 
    returns None if the class type is not defined in this module"""

    control_obj = None
    for name, obj_class in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if name is class_name: control_obj = obj_class(entity)
    
    return control_obj

##########DEFINE THE CONTROL COMPONENT CLASSES AFTER THIS LINE##############
#All ControlComponents must subclass entities.ControlComponent
    

class TreeControls(entities.ControlComponent):

    def __init__(self):
        super().__init__(entity)
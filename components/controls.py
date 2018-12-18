import sys, inspect, gamebox

def create_object(class_name, entity):
    """creates an object given a string of the class name, 
    returns None if the class type is not defined in this module"""

    control_obj = None
    for name, obj_class in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if name == class_name: control_obj = obj_class(entity)
    
    return control_obj

#super class:
class ControlComponent:

    def __init__(self, entity):
        """"""
        self.entity = entity

    def update(self):
        """"""

##########DEFINE THE CONTROL COMPONENT CLASSES AFTER THIS LINE##############
#All ControlComponents must subclass entities.ControlComponent
    

class TreeControls(ControlComponent):

    def __init__(self, entity):
        super().__init__(entity)
import json, components, pygame

class EntityFactory:

    def __init__(self):
        self.__class_dicts = {} #stores class properties in inner dictionaries,
        # with each dictionary keyed to the class name

        self.__class_control_components = {} # maps class names to concrete control component classes

        self.__class_physics_components = {} # maps class names to concrete physics component classes

    def add_class(self, entity_class_name):
        """Adds an and entity class by parsing the class info
        from a json file"""
        #parse json file:
        class_dict = json.loads("entity_classes/" + entity_class_name + ".json")

        #insert a new dictionary in the self.__class_dicts keyed to the class name
        try:
            self.__class_dicts[class_dict.name] = class_dict
        except Exception:
            print("no key called 'name' in " + class_dict.__str__())
            return

    def create(self, entity_class):
        """entity_class_name is a string that matches the class name
        of a file previosly read in using the add_class method"""
        # create and entity:
        entity = Entity(self.__class_dicts[entity_class]["spritesheet"], entity_class)
        
        # edit entity properties based on the dictionary entry that matches the
        # class name, if it exists:
        for instance_var in self.__class_dicts[entity_class]:
            entity.instance_vars[instance_var] = self.__class_dicts[entity_class][instance_var]

        control_class =  self.__class_control_components.get(entity_class)
        if control_class is not None:
            entity.control_component = components.controls.create_object(control_class) 

        physics_class = self.__class_physics_components.get(entity_class)
        if phyics_class is not None:
            entity.physics_component = components.physics.create_object(physics_class)

        return entity

    class Entity:

        def __init__(self, spritesheet, class_name):
            """spritesheet encapsulates an array of images in a SpriteSheet object.
            It gets all it's values from externally defined json files"""
            self.instance_vars = {}

            #physics and control components are defined elsewhere and then set by the create method
            #the EntityFactory class. If no 
            self.physics_component = None
            self.control_component = None

            self.render_component = components.renders.EntityRender(spritesheet, self)
            self.class_name = class_name

        def get_property(property_name):
            """returns the property value as a string"""
            return self.instance_vars.get(property_name)

        def update(self):
            self.render_component.update()
            if self.physics_component is not None: self.physics_component.update()
            if self.control_component is not None: self.control_component.update()

        def get_image(self):
            return self.render_component.get_image()

        def get_pos(self):
            self.physics_component.get_pos()
            
def test():

    efactory = EntityFactory()
    efactory.add_class("test_entity")
    efactory.create("test_entity")
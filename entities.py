import gamebox, spritesheets, pygame, json
import pygame_boilerplate.engine as engine
import components.controls, components.physics

__entity_set = []

def add_entity(entity):
    """Adds the entity to the entities module's entity list, and also
    draws the entity to screen"""

    global __entity_set

    if entity not in __entity_set:
        __entity_set.append(entity)
        draw(entity)

def remove_entity(entity):
    """Removes the entity from entities module's entity list, and also 
    erases the entity from the screen"""

    global __entity_set

    for e in __entity_set:
        if e == entity:
            __entity_set.remove(e)
            erase(e)

def draw(entity):
    """erases the entity from the screen and redraws it, redrawing
    any entities that were partially erased in the process."""

    erase(entity)

    gamebox.render_later(entity.graphics)

def erase(entity):
    """erases the entity from the screen, then redraws all entities
    that were erased in the process."""

    rect = entity.physics.get_rect()
    gamebox.render_later(components.renders.SurfRender(rect.size, rect.topleft))

    global __entity_set

    for e in __entity_set:
        if e.physics.get_rect().colliderect(rect):
            gamebox.render_later(e.graphics)


class PhysicsComponent:
    """"""

    def __init__(self, entity):
        """"""
        self.entity = entity

    def update(self):
        """"""

    def get_pos(self):
        """"""
        return self.get_rect().topleft

    def get_rect(self):
        """gets pygame.Rect object for this component"""
        return self.entity.graphics.get_image().get_rect()

class GraphicsComponent(engine.Renderable):
    """GhaphicsComponent for an entity. Entities with procedurally generated graphics
    should contain a GraphicsComponent that subclasses this class and overwrites the 
    update() and get_image() methods."""

    def __init__(self, entity):
        """Takes a RenderableComponent with a spritesheet filepath set to the passed 
        entity's 'spritesheet' property"""
        self.__spritesheet = spritesheets.SpriteSheet(entity.get_property("spritesheet"))
        self.__entity = entity

    def update(self):
        """updates the image to reflect the next image on the spritesheet"""
        self.__spritesheet.next()

    def get_image(self):
        return self.__spritesheet.get_image()

class ControlComponent:

    def __init__(self, entity):
        """"""
        self.entity = entity

    def update(self):
        """"""

class EntityFactory:

    def __init__(self):
        self.__class_dicts = {} #stores class properties in inner dictionaries,
        # with each dictionary keyed to the class name

    def add_class(self, entity_class_name):
        """Adds an and entity class by parsing the class info
        from a json file"""
        #parse json file:
        file_content = open("entity_classes\\" + entity_class_name + ".json")
        file_string = ""
        for line in file_content:
            file_string += line

        class_dict = json.loads(file_string)

        #insert a new dictionary in the self.__class_dicts keyed to the class name
        try:
            self.__class_dicts[class_dict["name"]] = class_dict
        except Exception:
            print("no key called 'name' in " + class_dict.__str__())
            return

    def create(self, entity_class):
        """entity_class_name is a string that matches the class name
        of a file previosly read in using the add_class method"""
        # create and entity:
        entity = EntityFactory.Entity(self.__class_dicts[entity_class]["spritesheet"])
        
        # edit entity properties based on the dictionary entry that matches the
        # class name, if it exists:
        for instance_var in self.__class_dicts[entity_class]:
            entity.instance_vars[instance_var] = self.__class_dicts[entity_class][instance_var]
        entity.graphics = GraphicsComponent(entity)

        control_class = entity.get_property("control-class")
        if control_class is not None:
            entity.controls = components.controls.create_object(control_class) 

        physics_class = entity.get_property("physics-class")
        if physics_class is not None:
            entity.physics = components.physics.create_object(physics_class)

        return entity

    class Entity:

        def __init__(self, spritesheet):
            """spritesheet encapsulates an array of images in a SpriteSheet object.
            It gets all it's values from externally defined json files"""
            self.instance_vars = {}

            #physics and control components are defined elsewhere and then set by the create method
            #the EntityFactory class. If no 
            self.physics = None
            self.controls = None
            self.graphics = None

        def get_property(self, property_name):
            """returns the property value as a string"""
            return self.instance_vars.get(property_name)

        def update(self):
            self.graphics.update()
            if self.physics is not None: self.physics.update()
            if self.controls is not None: self.controls.update()

        def get_image(self):
            return self.graphics.get_image()

        def get_pos(self):
            self.physics.get_pos()

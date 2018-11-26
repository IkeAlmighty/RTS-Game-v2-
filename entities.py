import gamebox, spritesheets, pygame, json

__entity_set = []

def add_entity(entity):
    """Adds the entity to the entities module's entity list, and also
    draws the entity to screen"""

    global __entity_set

    if entity not in __entity_set:
        __entity_set.append(entity)
        entities.draw(entity)

def remove_entity(entity):
    """Removes the entity from entities module's entity list, and also 
    erases the entity from the screen"""

    global __entity_set

    for e in __entity_set:
        if e == entity:
            __entity_set.remove(e)
            entities.erase(e)

def draw(entity):
    """erases the entity from the screen, redrawing
    any entities that were partially erased in the process."""

    entities.erase(entity)

    gamebox.render_later(entity.graphics)

def erase(entity):
    """erases the entity from the screen, then redraws all entities
    that were erased in the process."""

    global __entity_set

    for e in __entity_set:
        if e.physics.get_rect().colliderect(entity.physics.get_rect()):
            gamebox.render_later(e.graphics)


class PhysicsComponent:

    def __init__(self, entity):
        """"""

    def update(self):
        """"""

    def get_pos(self):
        """"""

    def get_rect(self):
        """gets pygame.Rect object for this component"""

class GraphicsComponent(engine.Renderable):
    """RenderComponent for an entity. Entities with procedurally generated graphics
    should contain a RenderComponent that subclasses this class and overwrites the 
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

    def update(self):
        """"""

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
            entity.controls = components.controls.create_object(control_class) 

        physics_class = self.__class_physics_components.get(entity_class)
        if phyics_class is not None:
            entity.physics = components.physics.create_object(physics_class)

        return entity

    class Entity:

        def __init__(self, spritesheet, class_name):
            """spritesheet encapsulates an array of images in a SpriteSheet object.
            It gets all it's values from externally defined json files"""
            self.instance_vars = {}

            #physics and control components are defined elsewhere and then set by the create method
            #the EntityFactory class. If no 
            self.physics = None
            self.controls = None

            self.graphics = components.renders.EntityRender(spritesheet, self)
            self.class_name = class_name

        def get_property(property_name):
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

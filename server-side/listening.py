import noise, random

class WorldInstance:
    """
    A world instance contains the seed for the immutable parts of
    the world, and also contains all info for the mutable parts 
    (entities) as well.

    Entity data is grouped and accessed by passing the unique entity 
    id and the position of the entity to the world instance.

    A world instance is randomely generated at first, 
    but entities change over time in various ways, which is why
    the WorldInstance class has its own update loop that calls
    updates on chunks imbetween taking requests from users... IDK
    """

    def __init__(self, seed, size, square_width):
        #place all the initial entities in the world using
        #various noise functions
        
    
        
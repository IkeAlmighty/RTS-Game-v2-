import random, noise, math, pygame

class GameMapGenerator:
    """This GameMap Generator can be used for getting values of points and renderings of sections
    of a gamemap."""

    WATER = 0
    LAND = 1
    MOUNTAIN = 2

    def __init__(self, seed = None, size = (300, 300), octaves = 7, percent_water = 0.3, percent_mountain = 0.1):
        self.size = size

        random.seed(seed)

        self.x_off = random.randint(0, size[0]*10000)
        self.y_off = random.randint(0, size[1]*10000)

        self.octaves = octaves

        self.percent_land = 1.0 - percent_water - percent_mountain
        if self.percent_land < 0.0 or self.percent_land + percent_mountain + percent_water != 1.0: 
            #TODO: insert error into logs instead of printing:
            print("gamemap land type percentages do not add up to 1.0")
            import sys
            sys.exit(-1)
        self.percent_water = percent_water
        self.percent_mountain = percent_mountain

        #Got to make a game, can't always spend time figuring things like
        #range out. So the following code sacrifices some time to determine
        #the approximate min and max values generated from the pnoise function, 
        #so that they can be corrected to fit the map when get_val is called:

        sample = []

        #save 10000 values
        for i in range(0, 50000):
            #get a random position:
            x = random.randint(0, size[0])
            y = random.randint(0, size[1])
            pos = (x, y)

            val = noise.pnoise2(
                (pos[0] + self.x_off)/self.size[0], 
                (pos[1] + self.y_off)/self.size[1], 
                octaves=self.octaves, 
                repeatx=self.size[0], 
                repeaty=self.size[1]
                )

            sample.append(val)

        #save the min and max of the 10000 values for later use:
        self.min_value = min(sample)
        self.max_value = max(sample)


    def get_land_type(self, pos):
        """
        Gets the land type of and x, y position of the gamemap.
        Land types are defined at the top of the gamemap module.
        """

        val = self.get_val(pos)
        if val is None: return None

        if val >= 0 and val <= self.percent_water + self.min_value:
            return GameMapGenerator.WATER
        if val > self.percent_water + self.min_value and val <=  self.min_value + self.percent_water + self.percent_land:
            return GameMapGenerator.LAND
        if val > self.min_value + self.percent_water + self.percent_land and val <= 1.0:
            return GameMapGenerator.MOUNTAIN

        return None

    def get_val(self, pos):
        """Gets the noise value of this particular position on the map,
        returns None if the value is outside the map"""
        size = self.size

        # if outside of the bounds of the map, return None
        if pos[0] < 0 or pos[0] > size[0] or pos[1] < 0 or pos[1] > size[1]:
            return  None

        x_off = self.x_off
        y_off = self.y_off

        val = noise.pnoise2((pos[0] + x_off)/size[0], (pos[1] + y_off)/size[1], octaves=self.octaves, repeatx=size[0], repeaty=size[1])
    
        # The approximate min and max values for the pnoise function (determined in __init__)
        # are used to distribute the values between 0 and 1
        val = abs(val/(self.max_value - self.min_value))

        #adjust values that are not between 0 and 1:
        if val < 0.0: val = 0.0
        if val > 1.0: val = 1.0

        val = int(val*10000000)/10000000 #truncate some digits

        return val

    def get_rendering(self, rect, square_width)->pygame.Surface:
        rendering = pygame.Surface((rect.width*square_width, rect.height*square_width))
        filler = pygame.Surface((square_width, square_width))

        for x in range(rect.topleft[0], rect.topleft[0] + rect.width):
            for y in range(rect.topleft[1], rect.topleft[1] + rect.height):
                land_type = self.get_land_type((x, y))

                if land_type is None: 
                    continue

                color = (255, 0, 255) #error color

                if land_type is GameMapGenerator.WATER: color = (50, 50, 160)
                elif land_type is GameMapGenerator.LAND: color = (50, 160, 50)
                elif land_type is GameMapGenerator.MOUNTAIN: color = (76, 60, 3) #TODO make a better color

                filler.fill(color)
                rendering.blit(filler, ((x - rect.topleft[0])*square_width, (y - rect.topleft[1])*square_width))

        return rendering


def test():
    game_map = GameMapGenerator(None, percent_water=0.4, percent_mountain=0.3)

    print(game_map.get_val((1000, 1000)))
    
    import pygame
    pygame.init()
    scr_size = (800, 600)
    square_width = 5
    screen = pygame.display.set_mode(scr_size)

    start_time = pygame.time.get_ticks()
    rect = pygame.Rect(100, 100, scr_size[0]//square_width, scr_size[1]//square_width)
    render_chunk = game_map.get_rendering(rect, square_width)
    print(pygame.time.get_ticks() - start_time)

    pygame.display.flip()

    print("press escape to end")
    x = 100 
    y = 100
    clock = pygame.time.Clock()
    pos = (0, 0)
    while(True):

        start_render = pygame.time.get_ticks()

        screen.blit(render_chunk, (0, 0))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        # print(pygame.time.get_ticks() - start_render, " ", 1000/60)

        clock.tick(60)
import random, noise, math

WATER = 0
LAND = 1
MOUNTAIN = 2

class GameMap:

    def __init__(self, seed, size = (10000, 10000), octaves = 12, percent_water = 0.3, percent_land = 0.1, percent_mountain = 0.6):
        self.size = size

        random.seed(seed)

        self.x_off = random.randint(0, size[0]*10000)
        self.y_off = random.randint(0, size[1]*10000)

        self.octaves = octaves

        self.percent_water = percent_water
        self.percent_land = percent_land
        self.percent_mountain = percent_mountain

        #Got to make a game, can't always spend time figuring things like
        #range out. So the following code sacrifices some time to determine
        #the approximate min and max values generated from the pnoise function, 
        #so that they can be corrected to fit the map when get_val is called:

        sample = []

        #save 10000 values
        for i in range(0, 10000):
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
        global WATER
        global LAND
        global MOUNTAIN

        val = self.get_val(pos)

        if val >= 0 and val <= self.percent_water:
            return WATER
        if val > self.percent_water and val <=  self.percent_water + self.percent_land:
            return LAND
        if val > self.percent_water + self.percent_land and val <= 1.0:
            return MOUNTAIN

        return None

    def get_val(self, pos):
        """Gets the noise value of this particular position on the map,
        returns None if the value is outside the map"""
        size = self.size

        #if outside of the bounds of the map, return None:
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

    def get_chunk(self, rect):
        """WARNING: this function can take a long time with large chunks."""
        x_i = rect[0]
        y_i = rect[1]
        width = rect[2]
        height = rect[3]

        value_map = [0.0 for i in range(width*height)]
        for x in range(0, width):
            for y in range(0, height):
                value_map[x*height + y] = self.get_val((x_i + x, y_i + y))

        return value_map
                

#test:

game_map = GameMap(None)

print(game_map.get_val((100, 100)))

for i in range(0, 1000):
    pos = (0, i)
    print(game_map.get_land_type(pos))

chunk = game_map.get_chunk((100, 400, 500, 500))
print(chunk)


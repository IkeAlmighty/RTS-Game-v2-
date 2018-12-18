import pygame

class SpriteSheet:

    alpha = (255, 0, 255)

    def __init__(self, filepath):
        """Parses all sprites from a spritesheet and stores it in an encapsulated array.
        sprites should be seperated by rgb color (255, 0, 255) and be placed horizontally
        relative to one another. rgbh color should not be present on top or bottom edges 
        of image."""
        self.__index = 0

        #open file
        large_image = pygame.image.load("assets\\" + filepath)

        #parse out images, store in array
        self.__images = []
        last_x_start = 0
        
        for x in range(0, large_image.get_width() - 1):
            if large_image.get_at((x, 0)) == SpriteSheet.alpha: 
                last_x_start = x + 1
                continue
            
            elif large_image.get_at((x + 1, 0)) == SpriteSheet.alpha or x + 1 >= large_image.get_width() - 1:
                sprite_rect = pygame.Rect(last_x_start, 0, x - last_x_start, large_image.get_height())
                image = large_image.subsurface(sprite_rect).copy()
                self.__images.append(image)

    def next(self):
        self.__index += 1

        if self.__index >= len(self.__images):
            self.__index = 0

        return self.get_image()

    def get_image(self):
        return self.__images[self.__index]


    

    
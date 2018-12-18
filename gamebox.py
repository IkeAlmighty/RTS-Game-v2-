"""A sandbox module for accessing and calling important parts of the game engine."""

__game = None

def set_game(game):
    global __game
    __game = game

def screen_size():
    global __game
    return __game.screen_size

def erase_scrollmap(rect):
    """Takes a pygame rect describing a space in the scrollmap,
    and fills that space with only the pixels associated with the 
    height values of the map (no entities)"""
    global __game
    surf = __game.bscrollmap.get_image().subsurface(rect).copy()
    __game.bscrollmap.blit(surf, rect.topleft)

def render_to_scrollmap(renderable_component):
    global __game
    __game.bscrollmap.blit(renderable_component.get_image(), renderable_component.get_pos())
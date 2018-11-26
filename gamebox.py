"""A sandbox module for accessing and calling important parts of the game engine."""

__game = None

def set_game(game):
    global __game
    __game = game

def render_later(renderable_component):
    global __game
    __game.render_later(renderable_component)

def screen_size():
    global __game
    return __game.screen_size
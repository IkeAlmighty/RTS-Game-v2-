def test_renders():

    import gamemap
    from components.renders import *

    game_map = gamemap.GameMapGenerator(None, percent_water=0.4, percent_mountain=0.3)

    pygame.init()
    squ_width = 5
    pysize = (400, 300)
    screen = pygame.display.set_mode(pysize)

    rect = pygame.Rect(0, 0, pysize[0]//squ_width, pysize[1]//squ_width) #divide by the square width to get the actual pixel width
    scroll_map = ScrollMapRender(game_map, rect, squ_width, scrollspeed=7)

    screen.blit(scroll_map.get_image(), scroll_map.get_pos())

    pygame.display.flip()

    running = True
    clock = pygame.time.Clock()
    while running:
        start_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type is pygame.KEYDOWN and event.key is pygame.K_ESCAPE:
                running = False
        
        scroll_map.update()
        
        screen.blit(scroll_map.get_image(), scroll_map.get_pos())
        pygame.display.flip()
        
        # print(pygame.time.get_ticks() - start_time)

        clock.tick(60)
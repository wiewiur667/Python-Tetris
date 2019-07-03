import sys, pygame

def start():
    pygame.init()
    pygame.display.set_caption("Test")
    size = width, height = 640, 480
    screen = pygame.display.set_mode(size)
    background = pygame.Surface(screen.get_size())
    background.fill((255,255,255))
    background = background.convert()
    
    screen.blit(background, (0,0))

    running = True

    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


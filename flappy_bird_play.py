import sys
import pygame
import neat
import pickle
from pygame.locals import *
from parameters import *
from bird import Bird
from pipe import Pipe

def game():
    FPSCLOCK = pygame.time.Clock()

    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    
    bird = Bird(None)

    pipes = []
    pipes.append(Pipe())

    screen = pygame.display.set_mode(size)

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_UP:
                bird.flap()

        # Background
        screen.fill(BLACK)

        # Draw pipe(s)
        for pipe in reversed(pipes):
            pipe.update()
            pipe.show(screen)

            if bird.is_alive() and pipe.has_collided(bird):
                bird.die()

            if pipe.x < -PIPE_WIDTH:
                pipes.remove(pipe)

        # Draw bird(s)
        if bird.is_alive():
            bird.update()
            bird.show(screen)

        if pipes[-1].x == ADD_PIPE_POS:
            pipes.append(Pipe())
            # print(len(pipes))

        # Change frames
        pygame.display.flip()
        FPSCLOCK.tick(FPS_PLAY)

if __name__ == "__main__":

    pygame.init()
    pygame.display.set_caption('Flappy White-circle thing')
    game()
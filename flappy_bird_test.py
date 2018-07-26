import sys
import pygame
import neat
import pickle
import visualize
from pygame.locals import *
from parameters import *
from bird import Bird
from pipe import Pipe
from functions import *


def game(genome, config):
    FPSCLOCK = pygame.time.Clock()

    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    
    brain = neat.nn.FeedForwardNetwork.create(genome, config)
    bird = Bird(brain)

    pipes = []
    pipes.append(Pipe())

    screen = pygame.display.set_mode(size)

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        closest = closest_pipe([bird], pipes)
        if closest != None:
            brain_input = (bird.y / SCREEN_HEIGHT, 
                            closest.x / SCREEN_WIDTH,
                            closest.upper_pipe_len / SCREEN_HEIGHT,
                            closest.bottom_pipe_y / SCREEN_HEIGHT)

            output = bird.brain.activate(brain_input)

            if output[0] >= 0.5:
                bird.flap()

        # Background
        screen.fill(BLACK)

        # Draw pipe(s)
        for pipe in reversed(pipes):
            pipe.update()
            pipe.show(screen)

            if bird.is_alive() and pipe.has_collided(bird):
                bird.die()
                print(bird.fitness_score())

            if pipe.x < -PIPE_WIDTH:
                pipes.remove(pipe)

        # Draw bird(s)
        if bird.is_alive():
            bird.update()
            bird.show(screen)

        if pipes[-1].x == ADD_PIPE_POS:
            pipes.append(Pipe())

        # Change frames
        pygame.display.flip()
        FPSCLOCK.tick(FPS_PLAY)

if __name__ == "__main__":

    pygame.init()
    pygame.display.set_caption('Flappy White-circle thing')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, 
                            neat.DefaultSpeciesSet, neat.DefaultStagnation, 
                            'config')

    trained_bird = pickle.load(open('winner', 'rb'))
    node_names = {-1:'birdY', -2: 'PipeX', -3:'UpperY', -4: 'LowerY', 0: 'Flap'}
    visualize.draw_net(config, trained_bird, True, node_names=node_names)

    game(trained_bird, config)
    
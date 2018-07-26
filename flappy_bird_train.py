import sys
import pygame
import neat
import pickle
from pygame.locals import *
from parameters import *
from bird import Bird
from pipe import Pipe
from functions import *
from decimal import Decimal

def game(genomes, config):

    # Used to control the frame rate of the game
    FPSCLOCK = pygame.time.Clock()

    # Setup the game window with the given dimensions
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Array used to store birds
    birds = []

    # Variable keeps track of the dead birds
    # Once all the birds are dead the function game() 
    # terminates and retruns the birds array
    num_dead_birds = 0

    # A library specific way to loop through all genomes
    for genome_id, genome in genomes:

        # Create a network based on a given genome and the config file
        brain = neat.nn.FeedForwardNetwork.create(genome, config)

        # Create a bird which uses the previously created network
        bird = Bird(brain)

        # Add bird to the birds array
        birds.append(bird)

    # Array used to store the pipes in the game
    pipes = []

    # Add initial pipe 
    pipes.append(Pipe())

    # The pyame drawable surface used to render objects
    screen = pygame.display.set_mode(size)

    # Execute the code below until all birds die
    while num_dead_birds != len(genomes):

        # Handle game events
        for event in pygame.event.get():
            # Terminate game if escape key is pressed or window is closed
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        # Find pipe closest to bird
        closest = closest_pipe(birds, pipes)
        if closest != None:

            # Query for each bird
            for bird in birds:

                # Inputs to network:
                # bird.y - Y-location of a given bird
                # closest.x - X-location of the pipe closest to the bird
                # closest.upper_pipe_len - Y-location of the top of pipe gap
                # closest.bottom_pipe_y - Y-location of the bottom of pipe gap
                # Inputs are normalized accordingly
                brain_input = (bird.y / SCREEN_HEIGHT, 
                                closest.x / SCREEN_WIDTH,
                                closest.upper_pipe_len / SCREEN_HEIGHT,
                                closest.bottom_pipe_y / SCREEN_HEIGHT)

                # Query the netwrok of a given bird with the input
                output = bird.brain.activate(brain_input)

                # If output significant bird flaps up
                # otherwise it does nothing
                if output[0] >= 0.5:
                    bird.flap()

        # Draw Background
        screen.fill(BLACK)

        # Draw pipe(s)
        for pipe in reversed(pipes):

            # Update pipe location and render
            pipe.update()
            pipe.show(screen)

            for bird in birds:
                # If bird collides with pipe it dies.
                # If the bird has reached the goal fitness it also dies
                # So that the game() function can terminate
                if bird.is_alive() and (pipe.has_collided(bird) or bird.fitness_score() > 10000):
                    bird.die()
                    num_dead_birds += 1

            # If a pipe has exited the screen it get deleted from the array
            if pipe.x < -PIPE_WIDTH:
                pipes.remove(pipe)

        # Draw bird(s)
        for bird in birds:
            if bird.is_alive():
                # Update bird location and render on screen
                bird.update()
                bird.show(screen)

                # Print additional information once a bird can play the game
                # for an extended period of time
                if Decimal(str(bird.fitness_score())) % Decimal('500.0') == Decimal('0.0'):
                    print("A Genome has reached a fitness of %f" % bird.fitness_score())

        # Once last pipe has reached a predefined position on the screen
        # a new pipe gets added to the array
        if pipes[-1].x == ADD_PIPE_POS:
            pipes.append(Pipe())

        # Change frames
        pygame.display.flip()
        # Set frame rate for faster training
        FPSCLOCK.tick(FPS_TRAIN)

    # Returns the birds array to evolve networks based on
    # birds fitness
    return birds

def eval_genomes(genomes, config):
    # Array of birds returned from game()
    # each bird having a fitness value
    birds = game(genomes, config)

    bird_index = 0
    for genome_id, genome in genomes:
        # Assing bird fitness value to genome accordingly
        genome.fitness = birds[bird_index].fitness_score()
        bird_index += 1


if __name__ == "__main__":

    # Initialize pygame and set window caption
    pygame.init()
    pygame.display.set_caption('Flappy White-circle thing')

    # Load the configuration file used for the genomes
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, 
                            neat.DefaultSpeciesSet, neat.DefaultStagnation, 
                            'config')

    # Create population as specified in config
    population = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    # Returns the best performing genomes
    # i.e genome with heighest fitness
    winner = population.run(eval_genomes, 300)

    # Save best genome
    with open('winner', 'wb') as fid:
        pickle.dump(winner, fid)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))
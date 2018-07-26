from parameters import *

def closest_pipe(birds, pipes):

    # All of the birds are located at the same x-location
    # so only the first bird x-location can be used
    bird_x = birds[0].x

    # Closest pipe is unknown to begin with.
    # The value of None can also be used for
    # debuging in case something goes wrong.
    closest = None

    # Min distance should be infinity or the max
    # value for int. However, a pipe is not
    # rendered unless it is on the screen. So the
    # parameter SCREEN_WIDTH can be used.
    min_distance = SCREEN_WIDTH

    # Loop through all pipes
    for pipe in pipes:

        # Calculate distance between bird and current pipe
        # by also taking into account the width of the pipe
        # and the radius (width) of the bird.
        distance = pipe.x + PIPE_WIDTH + BIRD_R - bird_x

        # Keep track of smallest distance
        if distance > 0 and distance < min_distance:
            min_distance = distance
            closest = pipe

    return closest
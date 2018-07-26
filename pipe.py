import pygame
import random
from parameters import *

class Pipe:
    def __init__(self):
        self.upper_pipe_len = random.randint(MAX_GAP_FROM_EDGE, SCREEN_HEIGHT - MAX_GAP - MAX_GAP_FROM_EDGE)
        self.bottom_pipe_y = self.upper_pipe_len + random.randint(MIN_GAP, MAX_GAP)
        self.x = SCREEN_WIDTH

    def show(self, screen):
        top = pygame.Rect(self.x, 0, PIPE_WIDTH, self.upper_pipe_len)
        bottom = pygame.Rect(self.x, self.bottom_pipe_y, PIPE_WIDTH, SCREEN_HEIGHT - self.bottom_pipe_y)
        pygame.draw.rect(screen, WHITE, top)
        pygame.draw.rect(screen, WHITE, bottom)

    def update(self):
        self.x -= PIPE_SPEED

    def has_collided(self, bird):
        if (bird.x + bird.r < self.x or 
            (bird.x - bird.r > self.x + PIPE_WIDTH) or 
            (bird.y - bird.r > self.upper_pipe_len and bird.y + bird.r < self.bottom_pipe_y)):
            return False

        return True


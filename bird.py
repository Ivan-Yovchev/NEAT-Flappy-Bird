import pygame
from parameters import *

class Bird:
    def __init__(self, brain):
        self.x = BIRD_x
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.r = BIRD_R
        self.alive = True
        self.time_alive = 0
        if brain != None:
            self.brain = brain

    def show(self, screen):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.r * 2)

    def update(self):
        self.velocity += GRAVITY
        self.velocity *= AIR_RESISTANCE
        self.y += self.velocity
        self.check_boundaries()
        if self.alive:
            self.time_alive += 1

        

    def flap(self):
        self.velocity = max(MAX_LIFT, self.velocity + FLAP_LIFT)

    def check_boundaries(self):
        if self.y > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT
            self.velocity = 0

        if self.y < OUT_OF_TOP_SCREEN_ALLOWANCE:
            self.y = OUT_OF_TOP_SCREEN_ALLOWANCE
            self.velocity = 0

        self.y = int(round(self.y))

    def die(self):
        self.alive = False

    def fitness_score(self):
        return self.time_alive / 10.0

    def is_alive(self):
        return self.alive

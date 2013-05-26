import pygame
import tmx
import sys

class Sword(pygame.sprite.Sprite):
    image = pygame.image.load('data/images/sprites/Player/SwordPixel.png')
    def __init__(self, location, direction, *groups):
        super(Sword, self).__init__(*groups)
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.direction = direction
        self.directionx = direction[0]
        self.directiony = direction[1]
        self.lifespan = 0.5

    def update(self, dt, game):
        # decrement the lifespan of the sword swing
        # remove it if the time runs out
        self.lifespan -= dt
        if self.lifespan < 0:
            self.kill()
            return

        # why is one times 10 why 10? NO IDEA! but 1 didn't work and 10 does
        self.rect.x += self.direction[0] * 10 * dt
        self.rect.y += self.direction[1] * 10 * dt



        # check for collision with any of the enemy sprites; we pass the "kill
        # if collided" flag as True so any collided enemies are removed from the
        # game
        if pygame.sprite.spritecollide(self, game.enemies, True):
            # we also remove the bullet from the game or it will continue on
            # until its lifespan expires
            self.kill()


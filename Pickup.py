import pygame
import tmx
import sys


class HpUp(pygame.sprite.Sprite):
    image = pygame.image.load('data/images/sprites/Pickups/heart_container.png')
    def __init__(self, location, *groups):
        super(HpUp, self).__init__(*groups)
        self.rect = pygame.rect.Rect(location, self.image.get_size())

    def update(self, dt, game):
        if self.rect.colliderect(game.player.rect):
            game.player.maxlife += 1
            game.player.currentlife = game.player.maxlife
            self.kill()


class Pickup(pygame.sprite.Sprite):
    image = pygame.image.load('data/images/sprites/Pickups/pixel-heart-50.png')
    def __init__(self, location, *groups):
        super(Pickup, self).__init__(*groups)
        self.rect = pygame.rect.Rect(location, self.image.get_size())

    def update(self, dt, game):
        if self.rect.colliderect(game.player.rect) and (
        game.player.currentlife!= game.player.maxlife):
            game.player.currentlife += 1
            self.kill()

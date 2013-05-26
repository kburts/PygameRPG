import pygame
import tmx
import sys
from main 004 import *

class Player(pygame.sprite.Sprite):

    def __init__(self, location, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load('data/images/sprites/Player/new player.png')
        self.rect = pygame.rect.Rect(location, self.image.get_size())

        self.is_dead = False
        self.maxlife = 3
        self.currentlife = self.maxlife


    def update(self, dt, game):
        last = self.rect.copy()

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x -= 300 * dt
        if key[pygame.K_RIGHT]:
            self.rect.x += 300 * dt
        if key[pygame.K_UP]:
            self.rect.y -= 300 * dt
        if key[pygame.K_DOWN]:
            self.rect.y += 300 * dt


        new = self.rect

        for cell in game.tilemap.layers['triggers'].collide(new, 'blockers'):
            if last.right <= cell.left and new.right > cell.left:
                new.right = cell.left
            if last.left >= cell.right and new.left < cell.right:
                new.left = cell.right
            if last.bottom <= cell.top and new.bottom > cell.top:
                self.resting = True
                new.bottom = cell.top
                self.dy = 0
            if last.top >= cell.bottom and new.top < cell.bottom:
                new.top = cell.bottom
                self.dy = 0


        #Map/Level Handler
        for cell in game.tilemap.layers['triggers'].collide(new, 'levelend'):
            Game.level += 1

        if self.currentlife == 0:
            print 'YOU DIED'
            pygame.quit()
            sys.exit()

        game.tilemap.set_focus((new.x), (new.y))

    def draw_hearts(self, screen):
        self.heart = pygame.image.load('data/images/sprites/Player/pixel-heart-50.png')
        self.empty_heart = pygame.image.load('data/images/sprites/Player/heart_container.png')
        for x in range(self.currentlife):
            screen.blit(self.heart, ((25 * x), 25))
        for y in range(self.maxlife):
            screen.blit(self.empty_heart, ((25*y), 25))

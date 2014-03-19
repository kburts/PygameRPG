import pygame
import tmx
import sys
import random
import os


class Enemy_rat(pygame.sprite.Sprite):
    image = pygame.image.load('data/images/sprites/NPC/enemy_rat1.png')
    def __init__(self, location, *groups):
        super(Enemy_rat, self).__init__(*groups)
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.direction = 1
        self.damage_cooldown = 0

    def update(self, dt, game):
        self.rect.x += self.direction * 100 * dt
        for cell in game.tilemap.layers['triggers'].collide(self.rect, 'reverse'):
            if self.direction > 0:
                self.rect.right = cell.left
            else:
                self.rect.left = cell.right
            self.direction *= -1
            break

        if self.rect.colliderect(game.player.rect) and not self.damage_cooldown:
            game.player.currentlife -= 1
            self.damage_cooldown = 1
        self.damage_cooldown = max(0, self.damage_cooldown -dt)

class Boss_elmo(pygame.sprite.Sprite):
    image = pygame.image.load('data/images/sprites/NPC/Elmo.png')
    def __init__(self, location, *groups):
        super(Boss_elmo, self).__init__(*groups)
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.dx = 1
        self.dy = 1

        self.damage_cooldown = 0

    def update(self, dt, game):
        self.rect.x += self.dx * 50 * dt
        self.rect.y += self.dy * 50 * dt

#        self.rect.x += self.dx * random.randrange(25,200) * dt
#        self.rect.y += self.dy * random.randrange(25,200) * dt


        for cell in game.tilemap.layers['triggers'].collide(self.rect, 'bossblock'):
            if (self.rect.right == cell.left) or (self.rect.left == cell.right):
                self.dx *= -1
            elif (self.rect.top == cell.bottom) or (self.rect.bottom == cell.top):
                self.dy *= -1


        if self.rect.colliderect(game.player.rect) and not self.damage_cooldown:
            game.player.currentlife -= 1
            self.damage_cooldown = 1
        self.damage_cooldown = max(0, self.damage_cooldown -dt)



import pygame
import tmx
import sys

from Pickup import *
from NPC import *
from Wepons import *


'''NOTE: I did not make any sprites, they are taken off the AngbandTK website
where they have many free pixel art images for download
Tilests can be found at: http://pousse.rapiere.free.fr/tome/'''

''' Maps created with Tiled map editor (it's awesome!)'''

class Player(pygame.sprite.Sprite):

    def __init__(self, location, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load('data/images/sprites/Player/new player.png')
        self.rect = pygame.rect.Rect(location, self.image.get_size())

        self.is_dead = False

        self.maxlife = 3
        self.currentlife = self.maxlife

        self.sword_cooldown = 0


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

        # handle the player shooting key
        if key[pygame.K_d] and not self.sword_cooldown:
            Sword(self.rect.topright, [10,0], game.sprites)
            self.sword_cooldown = 0.4
        if key[pygame.K_a] and not self.sword_cooldown:
            Sword(self.rect.topleft, [-10,0], game.sprites)
            self.sword_cooldown = 0.4
        if key[pygame.K_w] and not self.sword_cooldown:
            Sword(self.rect.midtop, [0,-10], game.sprites) # remember -10 is actually up... crazy
            self.sword_cooldown = 0.4
        if key[pygame.K_s] and not self.sword_cooldown:
            Sword(self.rect.midbottom, [0,10], game.sprites)
            self.sword_cooldown = 0.1

        self.sword_cooldown = max(0, self.sword_cooldown - dt)

        #Drop a bomb... maybe?
        if key[pygame.K_q] and not self.sword_cooldown:
            Bomb(self.rect.topleft, Bomb.image, 0, game.sprites)
            self.sword_cooldown = 0.4



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

    def draw_hearts(self):
        self.heart = pygame.image.load('data/images/sprites/Player/pixel-heart-50.png')
        self.empty_heart = pygame.image.load('data/images/sprites/Player/heart_container.png')
        for x in range(self.currentlife):
            screen.blit(self.heart, ((25 * x), 25))
        for y in range(self.maxlife):
            screen.blit(self.empty_heart, ((25*y), 25))

class Game(object):
    level = 0
    def LevelManager(self):
        if self.level == 0:
            print'Weldome to level 1, find yourself a wepon'
            self.Level01(screen)
#        elif self.level == 1:
#            print'Level 2 is slightly spookier'
#            self.level02(screen)

    def Level01(self, screen):
        self.tilemap = tmx.load('map v4.tmx', screen.get_size())

        self.sprites = tmx.SpriteLayer()
        start_cell = self.tilemap.layers['triggers'].find('player')[0]
        end_cell = self.tilemap.layers['triggers'].find('levelend')[0]

        self.player = Player((start_cell.px, start_cell.py), self.sprites)

        self.Appendtotilemap()

        self.mainloop()

    def Level02(self, screen):
        print 'got into level 2! It is a little more spooky in here.'
        self.tilemap = tmx.load('level02.tmx', screen.get_size())

        self.sprites = tmx.SpriteLayer()
        start_cell = self.tilemap.layers['triggers'].find('player')[0]
        end_cell = self.tilemap.layers['triggers'].find('levelend')[0]

        self.player = Player((start_cell.px, start_cell.py), self.sprites)

        self.Appendtotilemap()

        self.mainloop()

    def Level03(self, screen):
        print 'First town, how exciting!'
        self.tilemap = tmx.load('Town01.tmx', screen.get_size())

        self.sprites = tmx.SpriteLayer()
        start_cell = self.tilemap.layers['triggers'].find('player')[0]
        end_cell = self.tilemap.layers['triggers'].find('levelend')[0]

        self.player = Player((start_cell.px, start_cell.py), self.sprites)

        self.Appendtotilemap()

        self.mainloop()

    def Appendtotilemap(self):
        ####### Append PICKUPS #######
        self.pickups = tmx.SpriteLayer()
        for pickup in self.tilemap.layers['pickups'].find('heart'):
            Pickup((pickup.px, pickup.py), self.pickups)
        self.tilemap.layers.append(self.pickups)

        for pickup in self.tilemap.layers['pickups'].find('heart_container'):
            HpUp((pickup.px, pickup.py), self.pickups)
        self.tilemap.layers.append(self.pickups)


        ####### Append ENEMIES #######
        self.enemies = tmx.SpriteLayer()
        for enemy in self.tilemap.layers['triggers'].find('enemy'):
            Enemy_rat((enemy.px, enemy.py), self.enemies)
        self.tilemap.layers.append(self.enemies)

        for enemy in self.tilemap.layers['triggers'].find('boss_elmo'):
            Boss_elmo((enemy.px, enemy.py), self.enemies)
        self.tilemap.layers.append(self.enemies)

        ####### Append SPRITES #######
        self.tilemap.layers.append(self.sprites)

    def mainloop(self):
        clock = pygame.time.Clock()
        checklevel = Game.LevelManager
        while 1:
            dt = clock.tick(30) # 30 is standard, 60 makes you dizzy

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            self.tilemap.update(dt / 1000., self)
            self.tilemap.draw(screen)

            self.player.draw_hearts()
#            self.player.attack()

            #Render the clock.get_fps(), 2 digits, antialiased
            screen.blit(smallFont.render(str(round(clock.get_fps(),2))+" FPS",
                                    1,(255,255,255)),(5,460))

            #Level Check:
            if Game.level == 1:
                Game.level = 2
                break
            if Game.level == 3:
                Game.level = 4
                break

            pygame.display.flip()


if __name__ == '__main__':
    pygame.font.init()
    smallFont = pygame.font.Font("data/other/Overhaul.otf",15) #From the cave, because it looked cool
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    Game().LevelManager()
    print ' got past level 1'
    Game().Level02(screen)
    Game().Level03(screen)
    pygame.quit()
    sys.exit()



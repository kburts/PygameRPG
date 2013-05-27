import pygame
import tmx
import sys
import os

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

class Bomb(pygame.sprite.Sprite):
    image = pygame.image.load(os.path.join("data/images/sprites/Player/Bomb/" + "BombExploding0.png"))
    fullimage = pygame.image.load('data/images/sprites/Player/Bomb/BombExploding.png')
    def __init__(self, location, image, startframe, *groups):
        super(Bomb, self).__init__(*groups)
        self.imagepath = "data/images/sprites/Player/Bomb"
        self.rectsize = (36,64)
        self.bombsheet = ('BombExploding0.png', 'BombExploding1.png', 'BombExploding2.png', 'BombExploding3.png',
                          'BombExploding4.png', 'BombExploding5.png', 'BombExploding6.png', 'BombExploding7.png',
                          'BombExploding8.png', 'BombExploding9.png'
                          )
        self.startframe = startframe

        
        self.location = location
        self.spritesheet = Bomb.fullimage

        self.rect = pygame.rect.Rect(location, self.rectsize)

        self.frames = []
        self.frame_inds = [[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0]]
                                    #loc of frames on sheet
        self.lifespan = 0.5
        self.get_images()

    def get_images(self):
        """Get the desired images from the sprite sheet."""
        for cell in self.frame_inds:
            loc = ((36*cell[0],64*cell[1]),self.rect.size)
            self.frames.append(self.spritesheet.subsurface(loc))

    def update(self, dt, game):
#        Bomb(self.rect.topleft, Bomb.image, (self.startframe+1), game.sprites)
#        for frame in self.bombsheet[self.startframe:]:
#            print frame
#            print (len(self.bombsheet))
#            print self.startframe
#            self.kill()
#            image = (os.path.join(self.imagepath + "/" + (frame)), (self.location))

        for x in range(len(self.bombsheet[self.startframe:])):
            print x
            if x == 9:
                break
            if self.startframe == x:
                Bomb(self.rect.topleft, Bomb.image, (self.startframe+1), game.sprites)



        self.lifespan -= dt
        if self.lifespan < 0:
            self.kill()
            return
        if pygame.sprite.spritecollide(self, game.enemies, True):
            self.kill()


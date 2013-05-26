import pygame
import tmx
import sys

'''NOTE: I did not make any sprites, they are taken off the AngbandTK website
where they have many free pixel art images for download
Tilests can be found at: http://pousse.rapiere.free.fr/tome/'''

''' Maps created with Tiled map editor (it's awesome!)'''

class Player(pygame.sprite.Sprite):

    #Player related Constants
    heart = pygame.image.load('data/images/sprites/pixel-heart-50.png')
    empty_heart = pygame.image.load('data/images/sprites/heart_container.png')
#    maxlife = 3
#    currentlife = maxlife
    def __init__(self, location, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load('data/images/sprites/new player.png')
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



        if self.currentlife == 0:
            print 'YOU DIED'
            pygame.quit()
            sys.exit()

        
        
        game.tilemap.set_focus((new.x), (new.y))

    def draw_hearts(self):
        for x in range(self.currentlife):
            screen.blit(Player.heart, ((25 * x), 25))
        for y in range(self.maxlife):
            screen.blit(Player.empty_heart, ((25*y), 25))


class Pickup(pygame.sprite.Sprite):
    image = pygame.image.load('data/images/sprites/pixel-heart-50.png')
    def __init__(self, location, *groups):
        super(Pickup, self).__init__(*groups)
        self.rect = pygame.rect.Rect(location, self.image.get_size())
#        self.image = pygame.image.load('data/images/sprites/pixel-heart-50.png')


    def heart(self, dt, game):
        self.image = pygame.image.load('data/images/sprites/pixel-heart-50.png')
        
    def update(self, dt, game):
        if self.rect.colliderect(game.player.rect) and (
        game.player.currentlife!= game.player.maxlife):
            game.player.currentlife += 1
            self.kill()
        

class Enemy(pygame.sprite.Sprite):
    image = pygame.image.load('data/images/sprites/enemy_rat1.png')
    def __init__(self, location, *groups):
        super(Enemy, self).__init__(*groups)
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

class Game(object):
    def main(self, screen):

        clock = pygame.time.Clock()

        self.tilemap = tmx.load('map v4.tmx', screen.get_size())

        self.sprites = tmx.SpriteLayer()
        start_cell = self.tilemap.layers['triggers'].find('player')[0]
        self.player = Player((start_cell.px, start_cell.py), self.sprites)


        self.pickups = tmx.SpriteLayer()
        for pickup in self.tilemap.layers['pickups'].find('heart'):
            Pickup((pickup.px, pickup.py), self.pickups)
        self.tilemap.layers.append(self.pickups)
        


        self.enemies = tmx.SpriteLayer()
        for enemy in self.tilemap.layers['triggers'].find('enemy'):
            Enemy((enemy.px, enemy.py), self.enemies)
        self.tilemap.layers.append(self.enemies)

        self.tilemap.layers.append(self.sprites)
        
        while 1:
            dt = clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            self.tilemap.update(dt / 1000., self)
#            screen.blit(background, (0, 0))
            self.tilemap.draw(screen)

            self.player.draw_hearts()


            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    Game().main(screen)



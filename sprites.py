import pygame
from settings import JUMP, WATER_JUMP, GRAV, WIN_WIDTH
from os import path

#load images
bg = [pygame.image.load('images/bg1.jpg'), pygame.image.load('images/bg2.jpg'), pygame.image.load('images/bg3.jpg')]
idle = [pygame.image.load('images/idle1.png'), pygame.image.load('images/idle2.png'), pygame.image.load('images/idle3.png'), pygame.image.load('images/idle4.png')]
walk = [pygame.image.load('images/walk1.png'), pygame.image.load('images/walk2.png'), pygame.image.load('images/walk3.png'), pygame.image.load('images/walk4.png'), pygame.image.load('images/walk5.png')] 
jumping = pygame.image.load('images/jump.png')
falling = pygame.image.load('images/fall.png')
block = pygame.image.load('images/block_green.png')
water = pygame.image.load('images/water.png')
spike = [pygame.image.load('images/spikeup.png'), pygame.image.load('images/spikedown.png'), pygame.image.load('images/spikeleft.png'), pygame.image.load('images/spikeright.png')]
cherry = [pygame.image.load('images/cherry1.png'), pygame.image.load('images/cherry2.png')]
easyportal = pygame.image.load('images/easyportal.png')
normalportal = pygame.image.load('images/normalportal.png')
hardportal = pygame.image.load('images/hardportal.png')
exitportal = pygame.image.load('images/exitportal.png')
demoportal = pygame.image.load('images/demoportal.png')
saveblock = pygame.image.load('images/saveblock.png')
gameover = pygame.image.load('images/gameover.png')
nothing = pygame.image.load('images/nothing.png')

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Player(Entity):
    def __init__(self, game, x, y):
        Entity.__init__(self)
        self.game = game
        self.xvel = 0
        self.yvel = 0
        self.faceright = True
        self.onGround = True
        self.airborne = True
        self.space = True
        self.jump_state = 'on_ground'
        self.falling = False
        self.idlecount = 0
        self.walkcount = 0
        self.image = idle[0]
        self.rect = pygame.Rect(x, y, 30, 30)
        self.in_air = True

    def update(self, jump, jump_cut, left, right, platforms, water):
        if self.in_air:
            if jump and self.space:
                # only jump if on the ground
                if self.onGround:
                    self.game.jumpsound.play()
                    self.yvel -= JUMP
                    self.jump_state = 'jumped'
                    self.space = False
            
            # jump cut if space key released
            if jump_cut:
                self.yvel += GRAV
                self.space = True

            # double jump           
            if self.jump_state == 'jumped' and not jump and not self.onGround:
                self.jump_state = 'ready_for_double_jump'
            
            if self.jump_state == 'on_ground' and self.yvel > 1.2:
                self.jump_state = 'freefall'
            
            if self.jump_state == 'freefall' and not jump and not self.onGround:
                self.jump_state = 'ready_for_double_jump'
            
            if self.jump_state == 'ready_for_double_jump' and not self.onGround and jump:
                self.game.djumpsound.play()
                self.yvel = 0
                self.yvel -= JUMP
                self.falling = False
                self.jump_state = 'double_jumped'
                self.space = False
            
            if not self.onGround:
                # only accelerate with gravity if in the air
                self.yvel += GRAV
                # max falling speed
                if self.yvel > 8: 
                    self.yvel = 8

        if not self.in_air:
            self.jump_state = 'in_water'

            if jump and self.space:
                self.game.djumpsound.play()
                self.yvel = -WATER_JUMP
                self.space = False
                self.falling = False
        
            if jump_cut:
                self.yvel += GRAV
                self.space = True

            if not self.onGround:
                self.yvel += GRAV

                if self.yvel > 2.8: 
                    self.yvel = 2.8

        # change player status
        if self.yvel < 0 or self.yvel > 1.2:
            self.airborne = True
            
        if self.yvel > 1.2:
            self.falling = True

        # sideway movements
        if left:
            self.xvel = -3
            self.faceright = False
        if right:
            self.xvel = 3
            self.faceright = True
        if not(left or right):
            self.xvel = 0

        # left border    
        if self.rect.x < 0:
            self.rect.x = 0
                
        # right border   
        if self.rect.x > WIN_WIDTH - 32:
            self.rect.x = WIN_WIDTH - 32
        
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False
        # do y-axis collisions
        self.collide(0, self.yvel, platforms)
        # do water collisions
        self.water_collide(water)

        # play animation
        self.animate()

    def collide(self, xvel, yvel, platforms):
        # player collision with platforms
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.airborne = False
                    self.falling = False
                    self.jump_state = 'on_ground'
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
    
    def water_collide(self, water):
        # player collision with water
        if pygame.sprite.spritecollide(self, water, False, pygame.sprite.collide_rect):
            self.in_air = False

        if not pygame.sprite.spritecollide(self, water, False, pygame.sprite.collide_rect):
            self.in_air = True

    def animate(self):
        if self.xvel > 0 or self.xvel < 0:
            self.walkloop()
            if self.airborne:
                self.updatecharacter(jumping)
                if self.falling:
                    self.updatecharacter(falling)
        else:
            self.idleloop()
            if self.airborne:
                self.updatecharacter(jumping)
                if self.falling:
                    self.updatecharacter(falling)
        self.mask = pygame.mask.from_surface(self.image)
    
    def idleloop(self):
        if self.idlecount == 5:
            self.updatecharacter(idle[1])
        if self.idlecount == 10:
            self.updatecharacter(idle[2])
        if self.idlecount == 15:
            self.updatecharacter(idle[3])
        if self.idlecount == 20:
            self.updatecharacter(idle[0])
            self.idlecount = 0
        self.idlecount = self.idlecount + 1

    def walkloop(self):
        if self.walkcount == 2:
            self.updatecharacter(walk[0])
        elif self.walkcount == 4:
            self.updatecharacter(walk[1])
        elif self.walkcount == 6:
            self.updatecharacter(walk[2])
        elif self.walkcount == 8:
            self.updatecharacter(walk[3])
        elif self.walkcount == 10:
            self.updatecharacter(walk[4])
            self.walkcount = 0
        self.walkcount = self.walkcount + 1
    
    def updatecharacter(self, ansurf):
        # flip image if player facing left
        if not self.faceright:
            ansurf = pygame.transform.flip(ansurf, True, False)
        self.image = ansurf

class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = block
        self.image = self.image.convert()
        self.image.set_alpha(150)
        self.rect = pygame.Rect(x, y, 24, 24)

class Water(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = water
        self.rect = pygame.Rect(x, y, 24, 24)

class Spikeup(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = spike[0]
        self.rect = pygame.Rect(x, y, 32, 32)
        self.mask = pygame.mask.from_surface(self.image)

class SpikeupSideways(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 3
        self.moving_right = True
        self.image = spike[0]
        self.rect = pygame.Rect(x, y, 32, 32)
        self.timecount = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, nothing):
        # change direction when hit with invisible block
        if pygame.sprite.spritecollide(self, nothing, False, pygame.sprite.collide_rect):
            self.xvel = -3

        if pygame.sprite.spritecollide(self, nothing, False, pygame.sprite.collide_rect) and self.timecount > 10 :
            self.xvel = 3
            self.timecount = 0
        
        self.rect.left += self.xvel
        self.timecount = self.timecount + 1

class SpikeupUpdown(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.yvel = 1
        self.image = spike[0]
        self.rect = pygame.Rect(x, y, 32, 32)
        self.y = self.rect.top
        self.timecount = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # change direction when rect top moves 40 pixels
        if  self.rect.top > self.y + 40:
            self.yvel = -1

        if self.rect.top < self.y and self.timecount > 10 :
            self.yvel = 1
            self.timecount = 0
        
        self.rect.top += self.yvel
        self.timecount = self.timecount + 1

class Spikedown(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = spike[1]
        self.rect = pygame.Rect(x, y, 32, 32)
        self.mask = pygame.mask.from_surface(self.image)

class Spikeleft(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = spike[2]
        self.rect = pygame.Rect(x, y, 32, 32)
        self.mask = pygame.mask.from_surface(self.image)

class Spikeright(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = spike[3]
        self.rect = pygame.Rect(x, y, 32, 32)
        self.mask = pygame.mask.from_surface(self.image)

class Cherry(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = cherry[0]
        self.rect = pygame.Rect(x, y, 32, 32)
        self.cherrycount = 0
    
    def update(self):
        self.animate()
    
    def animate(self):
        self.timeloop()    
        self.mask = pygame.mask.from_surface(self.image)
    
    def timeloop(self):
        if self.cherrycount == 5:
            self.image = cherry[1]
        elif self.cherrycount == 10:
            self.image = cherry[0]
            self.cherrycount = 0
        self.cherrycount = self.cherrycount + 1

class CherrySideways(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 3
        self.image = cherry[0]
        self.rect = pygame.Rect(x, y, 32, 32)
        self.timecount = 0
        self.cherrycount = 0
    
    def update(self, nothing):
        # change direction when hit with invisible block
        if pygame.sprite.spritecollide(self, nothing, False, pygame.sprite.collide_rect):
            self.xvel = -3

        if pygame.sprite.spritecollide(self, nothing, False, pygame.sprite.collide_rect) and self.timecount > 10 :
            self.xvel = 3
            self.timecount = 0
        
        self.rect.left += self.xvel
        self.timecount = self.timecount + 1
        self.animate()

    def animate(self):
        self.timeloop()    
        self.mask = pygame.mask.from_surface(self.image)
    
    def timeloop(self):
        if self.cherrycount == 5:
            self.image = cherry[1]
        elif self.cherrycount == 10:
            self.image = cherry[0]
            self.cherrycount = 0
        self.cherrycount = self.cherrycount + 1

class CherryUpdown(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.yvel = 3
        self.image = cherry[0]
        self.rect = pygame.Rect(x, y, 32, 32)
        self.timecount = 0
        self.cherrycount = 0
    
    def update(self, nothing):
        # change direction when hit with invisible block
        if pygame.sprite.spritecollide(self, nothing, False, pygame.sprite.collide_rect):
            self.yvel = -3

        if pygame.sprite.spritecollide(self, nothing, False, pygame.sprite.collide_rect) and self.timecount > 10 :
            self.yvel = 3
            self.timecount = 0
        
        self.rect.top += self.yvel
        self.timecount = self.timecount + 1
        self.animate()

    def animate(self):
        self.timeloop()    
        self.mask = pygame.mask.from_surface(self.image)
    
    def timeloop(self):
        if self.cherrycount == 5:
            self.image = cherry[1]
        elif self.cherrycount == 10:
            self.image = cherry[0]
            self.cherrycount = 0
        self.cherrycount = self.cherrycount + 1       

class SaveBlock(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = saveblock
        self.rect = pygame.Rect(x, y, 26, 26)

class EasyPortal(Entity):
     def __init__(self, x, y):
        Entity.__init__(self)
        self.image = easyportal
        self.rect = pygame.Rect(x, y, 32, 32)
        self.mask = pygame.mask.from_surface(self.image)

class NormalPortal(Entity):
     def __init__(self, x, y):
        Entity.__init__(self)
        self.image = normalportal
        self.rect = pygame.Rect(x, y, 32, 32)
        self.mask = pygame.mask.from_surface(self.image)

class HardPortal(Entity):
     def __init__(self, x, y):
        Entity.__init__(self)
        self.image = hardportal
        self.rect = pygame.Rect(x, y, 32, 32)
        self.mask = pygame.mask.from_surface(self.image)

class ExitPortal(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = exitportal
        self.rect = pygame.Rect(x, y, 32, 32)
        self.mask = pygame.mask.from_surface(self.image)
        
class DemoPortal(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = demoportal
        self.rect = pygame.Rect(x, y, 32, 32)
        self.mask = pygame.mask.from_surface(self.image)

class GameOver(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = gameover
        self.rect = pygame.Rect(x, y, 800, 320)

class Nothing(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.transform.scale(nothing, (28, 28))
        self.rect = pygame.Rect(x, y, 28, 28)
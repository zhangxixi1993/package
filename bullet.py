#coding:utf-8       #利用python2.7开发游戏，加入注释前必须加入此行指令！！！！！！！！
import pygame

class Bullet1(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('images/bullet_image.png').convert_alpha()
        self.rect=self.image.get_rect()
        self.rect.left,self.rect.top=position


        self.speed=14
        self.active=True
        self.mask=pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top-=self.speed
        if self.rect.top<0:
            self.active=False

    def reset1(self,positon):
        self.rect.left,self.rect.top=positon
        self.active=True


class Bullet2(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('images/bullet2.png').convert_alpha()
        self.rect=self.image.get_rect()
        self.rect.left,self.rect.top=position
        self.speed=18
        self.active=False
        self.mask=pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top-=self.speed
        if self.rect.top<0:
            self.active=False

    def reset(self,position):
        self.rect.left,self.rect.top=position
        self.active=True











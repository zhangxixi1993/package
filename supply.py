#coding:utf-8       #利用python2.7开发游戏，加入注释前必须加入此行指令！！！！！！！！
import pygame
from random import *
class Supply(pygame.sprite.Sprite):
    def __init__(self,bg_size,image):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(image).convert_alpha()
        self.rect=self.image.get_rect()
        self.width,self.height=bg_size[0],bg_size[1]
        self.rect.left,self.rect.top=randint(0,self.width-self.rect.width),-self.rect.height-10
        self.speed=5
        self.active=False
        self.mask=pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top<self.height:
            self.rect.top+=self.speed
        else:
            self.active=False
    def reset(self):
        self.active=True
        self.rect.left,self.rect.top=randint(0,self.width-self.rect.width),-self.rect.height-10
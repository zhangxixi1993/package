#coding:utf-8       #利用python2.7开发游戏，加入注释前必须加入此行指令！！！！！！！！
import pygame
from random import *


#########################################################################################################定义小型飞机
class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        self.image=pygame.image.load('images/enemy1.png').convert_alpha()
        self.rect=self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed=2
        self.rect.left,self.rect.top=randint(0,self.width-self.rect.width),randint(-5*self.height,-self.rect.height)
        #载入飞机爆炸图片
        self.destory_images=[]
        self.destory_images.extend([pygame.image.load('images/enemy1_down1.png').convert_alpha()])
        self.act=True
        self.mask=pygame.mask.from_surface(self.image)
    def move(self):
        if self.rect.top<self.height:
            self.rect.top+=self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), randint(-6 * self.height, -self.rect.height)
#######################################################################################################定义中型飞机
class MidEnemy(pygame.sprite.Sprite):
    energy=8
    def __init__(self,bg_size):
        self.image=pygame.image.load('images/enemy2.png').convert_alpha()
        self.rect=self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed=1
        self.rect.left,self.rect.top=randint(0,self.width-self.rect.width),randint(-10*self.height,-3*self.height)
        #载入飞机爆炸图片
        self.destory_images=[]
        self.destory_images.extend([pygame.image.load('images/enemy2_down1.png').convert_alpha()])
        self.act=True
        self.energy=MidEnemy.energy


        self.mask = pygame.mask.from_surface(self.image)
    def move(self):
        if self.rect.top<self.height:
            self.rect.top+=self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), randint(-10 * self.height,
                                                                                             -3*self.height)
        self.energy = MidEnemy.energy
#############################################################################################定义大型飞机
class BigEnemy(pygame.sprite.Sprite):
    energy = 20
    def __init__(self,bg_size):
        self.image=pygame.image.load('images/enemy3.png').convert_alpha()
        self.rect=self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed=1
        self.rect.left,self.rect.top=randint(0,self.width-self.rect.width),randint(-15*self.height,-5*self.height)
        #载入飞机爆炸图片
        self.destory_images=[]
        self.destory_images.extend([pygame.image.load('images/enemy3_down1.png').convert_alpha()])
        self.act = True
        self.mask = pygame.mask.from_surface(self.image)
        self.energy = BigEnemy.energy
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width), randint(-15 * self.height,
                                                                                             -5 * self.height)
        self.energy = BigEnemy.energy
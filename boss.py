#coding:utf-8       #利用python2.7开发游戏，加入注释前必须加入此行指令！！！！！！！！
import pygame
from random import *

class Boss(pygame.sprite.Sprite):
    def __init__(self,bg_size,image):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(image).convert_alpha()
        self.rect=self.image.get_rect()
        self.width,self.height=bg_size[0],bg_size[1]
        #定义boss初始化在<0的位置
        self.rect.left,self.rect.top=self.width/2-self.rect.width/2,-3*self.rect.height
        self.speed1=10     #boss初始速度
        self.speed2 =15
        #载入boss战败图片
        self.destory_images=[]
        self.destory_images.extend([pygame.image.load('images/boss_down1.png').convert_alpha()])
        self.destory_images.extend([pygame.image.load('images/boss_down2.png').convert_alpha()])
        self.destory_images.extend([pygame.image.load('images/boss_down3.png').convert_alpha()])
        self.destory_images.extend([pygame.image.load('images/boss_down4.png').convert_alpha()])

        self.destory_rect=[]
        for i in range(4):
            self.destory_rect.extend([self.destory_images[i].get_rect()])

        self.act=True
        self.mask = pygame.mask.from_surface(self.image)

########################################定义boss的上下左右移动
    def move_jinru(self):
        if self.rect.top<self.rect.height//2:
            self.rect.top+=self.speed1
        else:
            if self.rect.left > 0:
                self.rect.left -= self.speed2   #左移
            else:
                self.rect.left = 0

            if self.rect.left < self.width - self.rect.width :
                self.rect.left += self.speed2        #右移
            else:
                self.rect.left = self.width - self.rect.width

            if self.rect.top > 0:
                self.rect.top -= self.speed2    #上移
            else:
                self.rect.top = 0

            if self.rect.bottom < self.height-100 :
                self.rect.top += self.speed2   #下移
            else:
                self.rect.top = self.height  - self.rect.height-100

    def reset(self):
        self.rect.left, self.rect.top =self.width/2-self.rect.width/2,-3*self.rect.height
        self.act=True



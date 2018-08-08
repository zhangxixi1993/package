#coding:utf-8       #利用python2.7开发游戏，加入注释前必须加入此行指令！！！！！！！！
import pygame

class MyPlane(pygame.sprite.Sprite):
    def __init__(self,bg_size,image):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(image).convert_alpha()
        self.rect=self.image.get_rect()
        self.width,self.height=bg_size[0],bg_size[1]
        #定义我方飞机初始化在屏幕下方中央，距离下方底边x像素
        self.x=60
        self.rect.left,self.rect.top=self.width/2-self.rect.width/2,self.height-self.rect.height-self.x
        self.speed=10
        #载入飞机爆炸图片
        self.destory_images=[]
        self.destory_images.extend([pygame.image.load('images/me1_down1.png').convert_alpha()])
        self.act=True
        self.mask = pygame.mask.from_surface(self.image)
        self.wudi=False
########################################定义飞机的上下左右移动
    def moveup(self):                #上移
         if self.rect.top>0:
            self.rect.top-=self.speed
         else:
            self.rect.top=0

    def movedown(self):               #下移
       if self.rect.bottom<self.height-self.x:
           self.rect.top+=self.speed
       else:
           self.rect.top=self.height-self.x-self.rect.height

    def moveleft(self,x):               #左移
        if self.rect.left>x:
            self.rect.left-=self.speed
        else:
            self.rect.left=x

    def moveright(self,y):                 #右移
        if self.rect.left<self.width-self.rect.width-y:
           self.rect.left+=self.speed
        else:
            self.rect.left=self.width-self.rect.width-y

    def reset(self):
        self.rect.left, self.rect.top = self.width / 2 - self.rect.width / 2, self.height - self.rect.height - self.x
        self.act=True
        self.wudi=True



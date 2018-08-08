#coding:utf-8       #利用python2.7开发游戏，加入注释前必须加入此行指令！！！！！！！！
import pygame
import sys
import time
import traceback
import myplane
import enemy
import bullet
import supply
from pygame.locals import *
from random import *

pygame.init()
pygame.mixer.init()
bg_size=width,height=480,700
screen=pygame.display.set_mode(bg_size)
pygame.display.set_caption('飞机大战--zxx@silence')
background=pygame.image.load('images/background.png').convert()
myplane_image='images/me1.png'   #我方飞机图片
bulletimage='images/bullet_image.png'
#################################################################################################载入游戏音乐
pygame.mixer.music.load('sound/game_music.mp3')    #游戏背景音乐
pygame.mixer.music.set_volume(0.2)

bullet_sound=pygame.mixer.Sound('sound/bullet.wav')   #发射子弹音效
bullet_sound.set_volume(0.2)

bomb_sound=pygame.mixer.Sound('sound/use_bomb.wav')   #扔炸弹音效
bomb_sound.set_volume(0.2)

supply_sound=pygame.mixer.Sound('sound/supply.wav')   #获得供给音效
supply_sound.set_volume(0.2)

get_bomb_sound=pygame.mixer.Sound('sound/get_bomb.wav')   #获得炸弹音效
get_bomb_sound.set_volume(0.2)

get_bullet_sound=pygame.mixer.Sound('sound/get_bullet.wav')   #获得炸子弹音效
get_bullet_sound.set_volume(0.2)

upgrade_sound=pygame.mixer.Sound('sound/upgrade.wav')   #更新音效
upgrade_sound.set_volume(0.2)

enemy3_fly_sound=pygame.mixer.Sound('sound/enemy3_flying.wav')   #出现大飞机音效
enemy3_fly_sound.set_volume(0.2)

enemy1_down_sound=pygame.mixer.Sound('sound/enemy1_down.wav')   #小飞机被击落音效
enemy1_down_sound.set_volume(0.1)

enemy2_down_sound=pygame.mixer.Sound('sound/enemy2_down.wav')   #中飞机被击落音效
enemy2_down_sound.set_volume(0.2)

enemy3_down_sound=pygame.mixer.Sound('sound/enemy3_down.wav')   #大飞机被击落音效
enemy3_down_sound.set_volume(0.4)

me_down_sound=pygame.mixer.Sound('sound/me_down.wav')   #我方飞机被击落音效
me_down_sound.set_volume(0.3)
####################################################################################################主程序
delay=100
################################################定义一个检测函数
def main():
    pygame.mixer.music.play()
    clock=pygame.time.Clock()
    running=True
############################################实例化我方飞机
    me=myplane.MyPlane(bg_size,myplane_image)
########################################################################实例化敌方飞机
    smallenemies=[]
    midenemies=[]
    bigenemies=[]
    enemies=[]
    for i in range(15):            #实例化小飞机，15个一组
        smallenemy = enemy.SmallEnemy(bg_size)
        smallenemies.append(smallenemy)
        enemies.append(smallenemy)
    for i in range(7):                 #实例化中飞机，5个一组
        midenemy = enemy.MidEnemy(bg_size)
        midenemies.append(midenemy)
        enemies.append(midenemy)
    for i in range(3):                   #实例化大飞机，2个一组
        bigenemy = enemy.BigEnemy(bg_size)
        bigenemies.append(bigenemy)
        enemies.append(bigenemy)

    ##################################中弹索引
    e1_destory_index=0
    e2_destory_index = 0
    e3_destory_index = 0
    me_destory_index = 0
    #####################################生成子弹
    bullet1=[]
    bullet1_index=0
    BULLET1_NUM=4
    delay=100
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))
    ##############初始化得分
    score=0
    score_font=pygame.font.Font('font/AGENCYR.TTF',36)
    gameover_font=pygame.font.Font('font/LCALLIG.TTF',40)
##################################################################################主循环
    while running:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        screen.blit(background,(0,0))
        ###############################################################敌机登场和碰撞检测
        for each in smallenemies:
            if each.act:
                each.move()
                screen.blit(each.image, each.rect)
            else:
                enemy1_down_sound.play()
                screen.blit(each.destory_images[e1_destory_index],each.rect)
                score+=1000
                each.reset()
                each.act=True            #注意！！！敌机被销毁以后，要讲act为真，否则act一直为假，新生成的飞机不会下落

        for each in midenemies:
            if each.act:
                each.move()
                screen.blit(each.image, each.rect)
            else:
                enemy2_down_sound.play()
                screen.blit(each.destory_images[e2_destory_index],each.rect)
                score+=6000
                each.reset()
                each.act = True

        for each in bigenemies:
            if each.act:
                each.move()
                screen.blit(each.image, each.rect)
                if each.rect.top > -100:
                    enemy3_fly_sound.play()
            else:
                enemy3_down_sound.play()
                screen.blit(each.destory_images[e3_destory_index], each.rect)
                score+=10000
                each.reset()
                each.act = True
        ##########################################################检测敌机是否重叠,如果重叠则重新生成
        for i in enemies:
            enemies.remove(i)
            enemies_chongdie = pygame.sprite.spritecollide(i, enemies, False, pygame.sprite.collide_mask)
            if enemies_chongdie:
                for each in enemies_chongdie:
                    if each.rect.bottom<0:
                        i.reset()
                    else:
                        pass
            else:
                pass
            enemies.append(i)
        ##################################################################我方飞机登场
        if me.act:
            screen.blit(me.image, me.rect)
        else:
            me_down_sound.play()
            screen.blit(me.destory_images[me_destory_index],me.rect)
            print('游戏结束！')
            gameover_text = gameover_font.render('Game Over!' , True, (255, 255, 255))
            screen.blit(gameover_text, (bg_size[0]/2-100, bg_size[1]/2))
            time.sleep(3)

            running=False
######################################检测用户的键盘操作，控制飞机移动
        key_pressed=pygame.key.get_pressed()
        #移动飞机
        if key_pressed[K_w] or key_pressed[K_UP]:
            me.moveup()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            me.movedown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            me.moveleft()
        if key_pressed[K_d] or key_pressed[K_DOWN]:
            me.moveright()
#############################################################################碰撞检测
        enemies_down=pygame.sprite.spritecollide(me,enemies,False,pygame.sprite.collide_mask)
        if enemies_down:
            me.act=False
            for i in enemies_down:
                i.act=False
###############################################################################发射子弹
        delay-=1
        if not delay:
            delay=100
        if not (delay%10):
            bullet1[bullet1_index].reset1(me.rect.midtop)
            bullet1_index=(bullet1_index+1)%BULLET1_NUM

        for b in bullet1:
            if b.active:
                b.move()
                screen.blit(b.image,b.rect)
                enemy_hit=pygame.sprite.spritecollide(b,enemies,False,pygame.sprite.collide_mask)
                if enemy_hit:
                    b.active=False
                    for each in enemy_hit:
                        if each not in smallenemies:
                            ########### #############################################添加血条
                            pygame.draw.line(screen, (0,0,0), (each.rect.left, each.rect.top - 5),
                                             (each.rect.right,
                                              each.rect.top - 5), 2)
                            if each in midenemies:
                                energy_remain = each.energy / enemy.MidEnemy.energy
                            else:
                                energy_remain = each.energy / enemy.BigEnemy.energy

                            if energy_remain > (255,255,0):
                                energy_color = GL_GREEN_SIZE
                            else:
                                energy_color = (255,0,0)
                            pygame.draw.line(screen, energy_color, (each.rect.left, each.rect.top - 5),
                                             (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5), 2)
                            #################################################################每中弹一次，生命值减1
                            each.energy-=1
                            if each.energy==0:
                                each.act = False
                        else:
                            each.act=False
        #########################################绘制得分
        score_text=score_font.render('Score: %s' % str(score),True,(255,255,255))
        screen.blit(score_text,(10,5))

        pygame.display.flip()
        clock.tick(60)
if __name__=='__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()







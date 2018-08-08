#coding:utf-8       #利用python2.7开发游戏，加入注释前必须加入此行指令！！！！！！！！
import pygame
import sys
import time
import traceback
import myplane
import enemy
import bullet
import supply
import boss
from pygame.locals import *
from random import *

pygame.init()
pygame.mixer.init()
bg_size=width,height=480,700
screen=pygame.display.set_mode(bg_size)
pygame.display.set_caption('飞机大战--zxx@silence')
background=pygame.image.load('images/background.png').convert()
myplane_image='images/me1.png'   #我方飞机图片
supper_image='images/supper_plane.png'
son_image='images/son.png'
bulletimage='images/bullet_image.png'

boss_image='images/boss.png'
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

upgrade_sound=pygame.mixer.Sound('sound/upgrade_sound.wav')   #更新音效
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
delay=100  #延迟
################################################定义颜色
BLACK=(0,0,0)
YELLOW=(0,255,0)
WHITE=(255,255,255)
RED=(255,0,0)
BLUE=(0,0,255)
##########################定义加速函数
def acc_speed(target,much):
    target.speed+=much

def main():
    pygame.mixer.music.play()
    clock=pygame.time.Clock()
    running=True
############################################实例化我方飞机
    me=myplane.MyPlane(bg_size,myplane_image)
    supper_me=myplane.MyPlane(bg_size,supper_image)
    my_son1=myplane.MyPlane(bg_size,son_image)
    my_son2 = myplane.MyPlane(bg_size, son_image)

    #########################实例化boss
    BOSS=boss.Boss(bg_size,boss_image)

########################################################################实例化敌方飞机
    smallenemies=[]
    midenemies=[]
    bigenemies=[]
    enemies=[]
    small=0
    mid=0
    big=0
    energy_remain = 1
    for i in range(15):            #实例化小飞机，15个一组
        smallenemy = enemy.SmallEnemy(bg_size)
        small=smallenemy.rect.width   #设小飞机的宽度为small
        smallenemies.append(smallenemy)
        enemies.append(smallenemy)
    for i in range(7):                 #实例化中飞机，7个一组
        midenemy = enemy.MidEnemy(bg_size)
        mid=midenemy.rect.width
        midenemies.append(midenemy)
        enemies.append(midenemy)
    for i in range(3):                   #实例化大飞机，3个一组
        bigenemy = enemy.BigEnemy(bg_size)
        big=bigenemy.rect.width
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
    #####################################生成超级子弹
    bullet2=[]
    bullet2_index=0
    bullet3=[]
    bullet3_index=0
    BULLET2_NUM=8
    for i in range(BULLET2_NUM//2):
        bullet2.append(bullet.Bullet2((me.rect.centerx-me.rect.width/2,me.rect.top)))
        bullet2.append(bullet.Bullet2((me.rect.centerx+me.rect.width/2,me.rect.top)))
    for i in range(BULLET2_NUM//2):
        bullet3.append(bullet.Bullet2((my_son1.rect.left+my_son1.rect.width//2,my_son1.rect.top)))
        bullet3.append(bullet.Bullet2((me.rect.centerx-me.rect.width/2,me.rect.top)))
        bullet3.append(bullet.Bullet2((me.rect.centerx + me.rect.width / 2, me.rect.top)))
        bullet3.append(bullet.Bullet2((my_son2.rect.left+my_son2.rect.width//2, my_son2.rect.top)))
    DOUBLE_BULLET_TIME=USEREVENT+1   #超级子弹计时器
    is_double_bullet=False

    #enemy_hit=[]
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))
    ##############初始化得分
    score=0
    score_font=pygame.font.Font('font/AGENCYR.TTF',36)

    ####################################################################是否暂停游戏
    pause=False
    pause1_image=pygame.image.load('images/pause1.png').convert_alpha()
    pause_image = pygame.image.load('images/pause.png').convert_alpha()
    resume1_image = pygame.image.load('images/resume1.png').convert_alpha()
    resume_image = pygame.image.load('images/resume.png').convert_alpha()
    pause_rect=pause1_image.get_rect()
    pause_rect.left,pause_rect.top=width-pause_rect.width-10,10

    PAUSE_image=pause1_image
    level=1
    ##########################全屏炸弹
    bomb_image=pygame.image.load('images/bomb.png').convert_alpha()
    bomb_rect=bomb_image.get_rect()
    bomb_font = pygame.font.Font('font/AGENCYR.TTF', 32)
    bomb_num=3
    ##############################补给包
    bulletsupply='images/bullet_supply.png'
    bombsupply = 'images/bomb_supply.png'
    bullet_supply=supply.Supply(bg_size,bulletsupply) #实例化子弹补给包
    bomb_supply=supply.Supply(bg_size,bombsupply)  #实例化炸弹补给包
    SUPPLY_TIME=USEREVENT       #定义用户事件，用于计时
    pygame.time.set_timer(SUPPLY_TIME,30*1000)  #每隔30秒发放补给包
    bullets=[]
    ##########################三次生命
    life_image=pygame.image.load('images/life.png').convert_alpha()
    life_image_rect=life_image.get_rect()
    life_num=3
    #################################解除无敌状态
    WUDI_TIME=USEREVENT+2

    ###################################结束画面设置
    recorded=False
    gameover_font = pygame.font.Font('font/LCALLIG.TTF', 40)
    again_image=pygame.image.load('images/again1.png').convert_alpha()
    again_image_rect=again_image.get_rect()
    gameover_image=pygame.image.load('images/gameover1.png').convert_alpha()
    gameover_image_rect = gameover_image.get_rect()
    record_score=0
##################################################################################主循环
    while running:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

            ########################################################暂停或继续
            elif event.type==MOUSEBUTTONDOWN:
                if event.button==1 and pause_rect.collidepoint(event.pos):
                    pause= not pause
            ##############如果游戏处于暂停状态，则停止播放音乐和背景音乐以及补给包
                    if pause:
                        pygame.time.set_timer(SUPPLY_TIME,0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(SUPPLY_TIME,30*1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
            ###############################################控制暂停的按钮
            elif event.type==MOUSEMOTION:
                if pause_rect.collidepoint(event.pos):
                    if pause:
                        PAUSE_image=resume_image
                    else:
                        PAUSE_image=pause_image
                else:
                    if pause:
                        PAUSE_image=resume1_image
                    else:
                        PAUSE_image=pause1_image
            ###################################################
            elif event.type==KEYDOWN:
                if event.key==K_SPACE:    #按下空格使用全屏# 炸弹
                    if bomb_num:
                        bomb_num-=1
                        bomb_sound.play()
                        for i in enemies:
                            if i.rect.bottom>0:
                                i.act=False
            elif event.type==SUPPLY_TIME:
                supply_sound.play()          #随机选择Ture或者False,前者发放炸弹补给，后者发放子弹补给
                if choice([True,False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()
            elif event.type==DOUBLE_BULLET_TIME:
                is_double_bullet=False
                pygame.time.set_timer(DOUBLE_BULLET_TIME,0)
            elif event.type==WUDI_TIME:
                me.wudi=False
                pygame.time.set_timer(WUDI_TIME,0)


        screen.blit(background, (0, 0))
        bomb_text=bomb_font.render('X %d' % bomb_num,True,BLUE)
        text_rect=bomb_text.get_rect()
        screen.blit(bomb_image,(10,height-10-bomb_rect.height))
        screen.blit(bomb_text,(bomb_rect.width+10+5,height-5-text_rect.height))
            ########################################################################

        if not pause and life_num:
            if score>300000 and is_double_bullet:
                me = supper_me
                my_son1.rect.left,my_son1.rect.top=me.rect.left-my_son1.rect.width-5,me.rect.top+40
                my_son2.rect.left, my_son2.rect.top = me.rect.right + 5, me.rect.top+40


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

                    pygame.draw.rect(screen, BLUE,
                                         (each.rect.left, each.rect.top - 10, each.rect.width * (energy_remain), 10), 0)
                    pygame.draw.rect(screen, BLACK,(each.rect.left, each.rect.top - 10, each.rect.width, 10), 1)

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
                    pygame.draw.rect(screen, YELLOW,
                                     (each.rect.left, each.rect.top - 10, each.rect.width * (energy_remain), 10), 0)
                    pygame.draw.rect(screen, BLACK,
                                     (each.rect.left, each.rect.top - 10, each.rect.width, 10), 1)
                    if each.rect.top > -200:
                        enemy3_fly_sound.play()
                else:
                    enemy3_down_sound.play()
                    screen.blit(each.destory_images[e3_destory_index], each.rect)
                    score+=10000
                    each.reset()
                    each.act = True

            ##################################################################我方飞机登场
            if me.act:
                screen.blit(me.image, me.rect)
                if score>300000 and is_double_bullet:
                    screen.blit(my_son1.image,my_son1.rect)
                    screen.blit(my_son2.image, my_son2.rect)
            else:
                if not(delay%3):
                    me_down_sound.play()
                    screen.blit(me.destory_images[me_destory_index],me.rect)
                    life_num-=1
                    me.reset()
                    pygame.time.set_timer(WUDI_TIME,3*1000)

    ######################################检测用户的键盘操作，控制飞机移动
            key_pressed=pygame.key.get_pressed()
            #移动飞机
            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveup()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.movedown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                if score>300000 and is_double_bullet:
                    me.moveleft(my_son1.rect.width)
                else:
                    me.moveleft(0)

            if key_pressed[K_d] or key_pressed[K_DOWN]:
                if score>300000 and is_double_bullet:
                    me.moveright(my_son1.rect.width)
                else:
                    me.moveright(0)
    #############################################################################碰撞检测
            enemies_down=pygame.sprite.spritecollide(me,enemies,False,pygame.sprite.collide_mask)
            if enemies_down and not me.wudi:
                me.act=False
                for i in enemies_down:
                    i.act=False
    ###############################################################################发射子弹
            delay-=1
            if not delay:
                delay=100
            if not (delay%10):
                if score<600000:
                    if is_double_bullet:
                        bullets=bullet2
                        bullets[bullet2_index].reset((me.rect.centerx-me.rect.width/2,me.rect.top))
                        bullets[bullet2_index+1].reset((me.rect.centerx + me.rect.width / 2, me.rect.top))
                        bullet2_index=(bullet2_index+2)%BULLET2_NUM
                    else:
                        bullets=bullet1
                        bullets[bullet1_index].reset1(me.rect.midtop)
                        bullet1_index=(bullet1_index+1)%BULLET1_NUM
                else:              #得分超过600000，则启用无敌子弹
                    if is_double_bullet:
                        bullets=bullet3
                        bullets[bullet3_index].reset((my_son1.rect.left + my_son1.rect.width // 2, my_son1.rect.midtop))
                        bullets[bullet3_index+1].reset((me.rect.centerx - me.rect.width / 2, me.rect.top))
                        bullets[bullet3_index+2].reset((me.rect.centerx + me.rect.width / 2, me.rect.top))
                        bullets[bullet3_index+3].reset((my_son2.rect.left + my_son2.rect.width // 2, my_son2.rect.midtop))
                        bullet3_index=(bullet3_index+4)%(BULLET2_NUM*2)

                    else:
                        bullets = bullet2
                        bullets[bullet2_index].reset((me.rect.centerx - me.rect.width / 2, me.rect.top))
                        bullets[bullet2_index + 1].reset((me.rect.centerx + me.rect.width / 2, me.rect.top))
                        bullet2_index = (bullet2_index + 2) % BULLET2_NUM


            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image,b.rect)
                    enemy_hit=pygame.sprite.spritecollide(b,enemies,False,pygame.sprite.collide_mask)

                    if enemy_hit:
                        b.active=False
                        for each in enemy_hit:
                            if each not in smallenemies:
                                each.energy -= 1
                                    ###############################################################绘制血条
                                if each in midenemies:
                                    energy_remain = float(each.energy) / enemy.MidEnemy.energy

                                else:
                                    energy_remain = float(each.energy) / enemy.BigEnemy.energy

                                if each.energy == 0:
                                    each.act = False
                                    energy_remain=1

                            else:
                                each.act=False
            ################################################################发放补给包
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image,bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply,me):
                    get_bomb_sound.play()
                    if bomb_num<3:
                        bomb_num+=1
                    bomb_supply.active=False

            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image,bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, me):
                    get_bullet_sound.play()
                    bullet_supply.active=False
                    is_double_bullet=True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME,20*1000)

        ##########################################################根据分数增加游戏难度
            if score<50000 and level==1:
                level=2
            elif 50000<score<300000 and level==2:
                upgrade_sound.play()
                level=3
                for i in range(7):  # 添加小飞机
                    smallenemy = enemy.SmallEnemy(bg_size)
                    smallenemies.append(smallenemy)
                    enemies.append(smallenemy)
                for i in range(3):  #  添加中飞机
                    midenemy = enemy.MidEnemy(bg_size)
                    midenemies.append(midenemy)
                    enemies.append(midenemy)
                for i in range(2):  #  添加大飞机
                    bigenemy = enemy.BigEnemy(bg_size)
                    bigenemies.append(bigenemy)
                    enemies.append(bigenemy)
                for each in enemies:
                    if each.rect.width==small:
                        acc_speed(each, 0.7)

            elif 300000<score<600000 and level==3:
                upgrade_sound.play()
                level=4
                for i in range(5):
                    smallenemy = enemy.SmallEnemy(bg_size)
                    smallenemies.append(smallenemy)
                    enemies.append(smallenemy)
                for i in range(3):
                    midenemy = enemy.MidEnemy(bg_size)
                    midenemies.append(midenemy)
                    enemies.append(midenemy)
                for i in range(2):
                    bigenemy = enemy.BigEnemy(bg_size)
                    bigenemies.append(bigenemy)
                    enemies.append(bigenemy)
                for each in enemies:
                    if each.rect.width==small:
                        acc_speed(each, 0.5)
                    elif each.rect.width==mid:
                        acc_speed(each,0.5)
            elif 600000<score<1000000 and level==4:
                upgrade_sound.play()
                level=5
                for i in range(5):
                    smallenemy = enemy.SmallEnemy(bg_size)
                    smallenemies.append(smallenemy)
                    enemies.append(smallenemy)
                for i in range(3):
                    midenemy = enemy.MidEnemy(bg_size)
                    midenemies.append(midenemy)
                    enemies.append(midenemy)
                for i in range(2):
                    bigenemy = enemy.BigEnemy(bg_size)
                    bigenemies.append(bigenemy)
                    enemies.append(bigenemy)
                for each in enemies:
                    if each.rect.width==small:
                        acc_speed(each, 0.6)
                    elif each.rect.width==mid:
                        acc_speed(each,0.4)
                    elif each.rect.width==big:
                        acc_speed(each,0.3)
            elif score>1000000 and level==5:
                upgrade_sound.play()
                level=6
                for i in range(10):
                    smallenemy = enemy.SmallEnemy(bg_size)
                    smallenemies.append(smallenemy)
                    enemies.append(smallenemy)
                for i in range(5):
                    midenemy = enemy.MidEnemy(bg_size)
                    midenemies.append(midenemy)
                    enemies.append(midenemy)
                for i in range(3):
                    bigenemy = enemy.BigEnemy(bg_size)
                    bigenemies.append(bigenemy)
                    enemies.append(bigenemy)
                for each in enemies:
                    if each.rect.width==small:
                        acc_speed(each, 1)
                    elif each.rect.width==mid:
                        acc_speed(each,0.5)
                    elif each.rect.width==big:
                        acc_speed(each,0.5)
            #########################################boss登场
          #  elif score==10000:












        if life_num:
            for i in range(life_num):
                screen.blit(life_image,(width-10-(i+1)*life_image_rect.width,height-10-life_image_rect.height))
        elif life_num==0:
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            pygame.time.set_timer(SUPPLY_TIME,0)
            if not recorded:
                recorded=True
                with open('record.txt','r') as f:
                    record_score=int(f.read())
                if score>record_score:
                    with open('record.txt', 'w') as f:
                        f.write(str(score))
            #################################结束画面
            if score>record_score:
                record_score_text = score_font.render('Best Score:%d' % score, True, BLUE)
            else:
                record_score_text = score_font.render('Best Score:%d' % record_score, True, RED)
            screen.blit(record_score_text,(150,100))
            gameover_text1=gameover_font.render('Your Score',True,BLUE)
            gameover_text1_rect=gameover_text1.get_rect()
            gameover_text1_rect.left,gameover_text1_rect.top=width//2-gameover_text1_rect.width//2,height//3
            screen.blit(gameover_text1,gameover_text1_rect)
            gameover_text2=gameover_font.render(str(score),True,BLUE)
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = width // 2 - gameover_text2_rect.width // 2,\
                                                                 gameover_text1_rect.bottom+10
            screen.blit(gameover_text2, gameover_text2_rect)

            again_image_rect.left,again_image_rect.top=width//2-again_image_rect.width//2,gameover_text2_rect.bottom+50
            screen.blit(again_image,again_image_rect)
            gameover_image_rect.left,gameover_image_rect.top=width//2-gameover_image_rect.width//2,again_image_rect.bottom+10
            screen.blit(gameover_image,gameover_image_rect)
            ##
            if pygame.mouse.get_pressed()[0]:
                pos=pygame.mouse.get_pos()
                if again_image_rect.left<pos[0]<again_image_rect.right and again_image_rect.top<pos[1]<again_image_rect.bottom:
                    main()
                elif gameover_image_rect.left<pos[0]<gameover_image_rect.right and gameover_image_rect.top<pos[1]<gameover_image_rect.bottom:
                    pygame.quit()
                    sys.exit()
            #print('游戏结束！')
            #gameover_text = gameover_font.render('Game Over!' , True, BLUE)
            #screen.blit(gameover_text, (bg_size[0]/2-100, bg_size[1]/2))

            #time.sleep(3)

            #running = False

        #########################################绘制得分
        score_text=score_font.render('Score: %s' % str(score),True,BLUE)
        screen.blit(score_text,(10,5))
        screen.blit(PAUSE_image,pause_rect)

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







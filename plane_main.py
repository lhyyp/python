import pygame
from plame_sprites import *


class PlaneGame(object):
    def __init__(self):
        # 1.创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2.创建时钟对象
        self.clock = pygame.time.Clock()
        #  3.创建精灵组
        self.__create_speites()
        # 4.设置定时器
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

    def __create_speites(self):
        bg1 = Background()
        bg2 = Background(True)
        self.back_group = pygame.sprite.Group(bg1, bg2)

        # 创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()

        # 创建英雄
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group( self.hero )

    def __event_handler(self):
        for event in pygame.event.get():
            # 退出
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            # 判断事件是不是定时器
            elif event.type == CREATE_ENEMY_EVENT:
                enemy = Enemy()
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()

            # elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            #     print('按下向右')
        # 获取按下的键盘被按下的键
        keys_pressd = pygame.key.get_pressed()
        #  判断用户按下的方向
        if keys_pressd[pygame.K_RIGHT]:
            self.hero.speed = 2
        elif keys_pressd[pygame.K_LEFT]:
            self.hero.speed = -2
        else:
            self.hero.speed = 0


    def __check_collide(self):
        # 子弹打飞机
        pygame.sprite.groupcollide(self.hero.bullet_group,self.enemy_group,True,True)

        # 敌机撞英雄
        enemies  = pygame.sprite.spritecollide(self.hero,self.enemy_group,True)

        if len(enemies) > 0:
            self.hero.kill()
            #  清空所有的子弹 精灵组的 子弹
            # self.hero.bullet_group.empty()
            #   停止在事件队列上重复创建子弹事件
            # pygame.time.set_timer(HERO_FIRE_EVENT, 0)
            # Restart = pygame.image.load('./images/restart_sel.png')
            # self.screen.blit(Restart, (0, 0))
            # pygame.display.update()

            PlaneGame.__game_over()



    def __update_sprites(self):
        # 精灵组 更新精灵的位置
        self.back_group.update()
        self.enemy_group.update()
        self.hero_group.update()
        self.hero.bullet_group.update()
        # 绘制所有得精灵
        self.back_group.draw(self.screen)
        self.enemy_group.draw(self.screen)
        self.hero_group.draw(self.screen)
        self.hero.bullet_group.draw(self.screen)


    @staticmethod
    def __game_over():
        pygame.quit()
        exit()


    def start_game(self):
        while True:
            # 1.设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            # 2.事件监听
            self.__event_handler()
            # 3.碰撞检测
            self.__check_collide()
            # 4.更新/绘制精灵组
            self.__update_sprites()
            # 5.更新显示
            pygame.display.update()



if __name__ == '__main__':
    game = PlaneGame()
    game.start_game()

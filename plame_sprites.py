import random
import pygame
# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 刷新的帧率
FRAME_PER_SEC = 60
# 创建敌机定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 创建子弹定时器常量
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GrameSprite(pygame.sprite.Sprite):
    """"飞机大战游戏精灵类"""

    def __init__(self, image_name, speed=1):
        # 调用父类方法
        super().__init__()

        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        self.rect.y += self.speed


class Background(GrameSprite):
    """背景类"""

    def __init__(self, is_flag=False):
        super().__init__('./images/background.png')
        if is_flag:
            self.rect.y = -self.rect.height

    def update(self):
        super().update()
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -SCREEN_RECT.height


class Enemy(GrameSprite):
    """"敌机类"""

    def __init__(self):
        super().__init__('./images/enemy0.png')
        self.speed = random.randint(1, 3)
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)
        self.rect.bottom = 0

    def __del__(self):
        # print('敌机挂了%s' % self.rect)
        pass

    def update(self):
        super().update()
        if self.rect.y >= SCREEN_RECT.height:
            # kill方法可以将精灵从精灵组中移除，精灵就会被销毁
            self.kill()


class Hero(GrameSprite):
    """英雄类"""

    def __init__(self):
        super().__init__('./images/hero1.png', 0)
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120

        # 创建子弹精灵组
        self.bullet_group = pygame.sprite.Group()

    def update(self):
        self.rect.x += self.speed
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        for i in (0,1,2):
            # 1.创建子弹精灵
            bullet = Bullet()
            # 2.设置子弹位置
            bullet.rect.bottom = self.rect.y - i*20
            bullet.rect.centerx = self.rect.centerx
            # 3.子弹精灵添加精灵组
            self.bullet_group.add(bullet)


class Bullet(GrameSprite):
    """子弹类"""

    def __init__(self):
        super().__init__('./images/bullet.png', -2)

    def __del__(self):
        print('子弹销毁')

    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()

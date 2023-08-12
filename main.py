import random
import time

import pygame
from pygame.locals import *

"""player"""


class PlayerPlane(pygame.sprite.Sprite):
    # store all bullets
    bullets = pygame.sprite.Group()

    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)

        self.speed = 12  # player speed
        self.player = pygame.image.load("./resources/image/plane.png")
        self.image = self.player

        # get plane location
        self.rect = self.image.get_rect()
        # player initial coord
        self.rect.topleft = [Manager.bg_size[0] * 0.05, (Manager.bg_size[1] - self.player.get_height()) / 2]
        # plane status
        self.is_up = False
        self.is_down = False

        self.screen = screen

        # ammo
        self.bullets = pygame.sprite.Group()

    @staticmethod
    def clear_bullets():
        PlayerPlane.bullets.empty()

    def move(self):
        # keyboard control
        key_pressed = pygame.key.get_pressed()
        # check if key_pressed = w/up, if so, change plane image
        if key_pressed[K_w] or key_pressed[K_UP]:
            self.is_up = True
            self.is_down = False
            self.player = pygame.image.load("./resources/image/planeUp.png")  # load ascending image
            self.rect.top -= self.speed
        elif key_pressed[K_s] or key_pressed[K_DOWN]:
            self.is_down = True
            self.is_up = False
            self.player = pygame.image.load("./resources/image/planeDown.png")
            self.rect.bottom += self.speed
        else:
            self.is_down = False
            self.is_up = False
        # reset plane image
        if not key_pressed[K_w] or key_pressed[K_UP] or key_pressed[K_s] or key_pressed[K_DOWN]:
            self.player = pygame.image.load("./resources/image/plane.png")
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            self.rect.left -= self.speed
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            self.rect.right += self.speed
        if key_pressed[K_SPACE]:
            bullet = Ammo(self.screen, self.rect.right + self.player.get_width(),
                          self.rect.top + self.player.get_height() / 2)
            self.bullets.add(bullet)
            #
            PlayerPlane.bullets.add(bullet)

    def update(self):
        self.move()
        self.display()

        if self.is_up:
            self.player = pygame.image.load("./resources/image/planeUp.png")
        elif self.is_down:
            self.player = pygame.image.load("./resources/image/planeDown.png")
        else:
            self.player = pygame.image.load("./resources/image/plane.png")

    def display(self):
        self.screen.blit(self.player, self.rect)
        # update bullets coord
        self.bullets.update()
        # add all bullets to screen
        self.bullets.draw(self.screen)


"""player's ammo"""


class Ammo(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        # initialize
        pygame.sprite.Sprite.__init__(self)
        # load bullet image
        self.image = pygame.image.load('./resources/image/bullet.png')
        height = self.image.get_height()
        # bullet location
        self.rect = self.image.get_rect()
        self.rect.topleft = [x - 126, y - height / 2]

        self.screen = screen
        self.speed = 10

    def update(self):
        #
        self.rect.left += self.speed
        # kill bullet if beyond boundary
        if self.rect.left > Manager.bg_size[0]:
            self.kill()


"""enemy plane """


class EnemyPlane(pygame.sprite.Sprite):
    enemy_bullets = pygame.sprite.Group()

    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        # load enemy image
        self.enemy = pygame.image.load("./resources/image/enemy1.png")
        self.image = self.enemy
        # enemy initial coord
        self.rect = self.image.get_rect()

        y = random.randrange(1, Manager.bg_size[1], 50)
        self.rect.topleft = [Manager.bg_size[0], y]
        # enemy speed
        self.speed = random.randint(3, 8)
        # current window obj
        self.screen = screen

        # ammo
        self.bullets = pygame.sprite.Group()

        # enemy plane movement direction
        self.direction = "down"

    def display(self):
        self.screen.blit(self.enemy, self.rect)
        # update bullets coord
        self.bullets.update()
        # add all bullets to screen
        self.bullets.draw(self.screen)

    def automove(self):
        if self.direction == "down":
            self.rect.bottom += self.speed

        elif self.direction == "top":
            self.rect.top -= self.speed

        if self.rect.bottom > Manager.bg_size[1] - self.enemy.get_height():
            self.direction = "top"
        elif self.rect.top < 0:
            self.direction = "down"

        self.rect.left -= self.speed

    def autofire(self):
        """auto fire"""
        firenum = random.randint(1, 15)
        if firenum == 8:
            bullet = EnemyAmmo(self.screen, self.rect.left, self.rect.top)
            self.bullets.add(bullet)
            EnemyPlane.enemy_bullets.add(bullet)

    def update(self):
        self.automove()
        self.autofire()
        self.display()

    @staticmethod
    def clear_bullets():
        EnemyPlane.enemy_bullets.empty()


"""enemy ammo"""


class EnemyAmmo(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        # initialize
        pygame.sprite.Sprite.__init__(self)
        # load bullet3 image
        self.image = pygame.image.load('./resources/image/bullet3.png')
        height = self.image.get_height()
        width = self.image.get_width()
        # bullet coord
        self.rect = self.image.get_rect()
        self.rect.topleft = [x - width, y - height / 2]
        # window
        self.screen = screen
        # bullet speed
        self.speed = random.randint(3, 13)

    def update(self):
        # keep update
        self.rect.left -= self.speed

        if self.rect.right < 0:
            self.kill()


"""background music"""


class GameSound(object):
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load('./resources/sound/bgLoop.wav')
        pygame.mixer.music.set_volume(0.3)  # volume
        # load hit sound
        self.__bomb = pygame.mixer.Sound('./resources/sound/enemyExplode.wav')

    def playBGM(self):
        pygame.mixer.music.play(-1)

    def playHitSound(self):
        pygame.mixer.Sound.play(self.__bomb)


"""hit box"""


class Hit(object):
    def __init__(self, screen, type):
        self.screen = screen
        if type == "enemy":
            self.mImage = [pygame.image.load("./resources/image/explode" + str(y) + ".png") for y in range(1, 4)]
        else:
            self.mImage = [pygame.image.load("./resources/image/planeDie" + str(y) + ".png") for y in range(1, 4)]
        self.mIndex = 0
        self.mPos = [0, 0]
        # visible or not
        self.mVisible = False

    def action(self, rect):
        # trigger explore
        self.mPos[0] = rect.left
        self.mPos[1] = rect.top
        # enable explore  w
        self.mVisible = True

    def draw(self):
        if not self.mVisible:
            return
        self.screen.blit(self.mImage[self.mIndex], (self.mPos[0], self.mPos[1]))
        self.mIndex += 1
        if self.mIndex >= len(self.mImage):
            # end of explosion
            self.mIndex = 0
            self.mVisible = False


class GameBg(object):
    # initialize
    def __init__(self, screen):
        self.mImage1 = pygame.image.load("./resources/image/background.jpg")
        self.mImage2 = pygame.image.load("./resources/image/background.jpg")

        self.screen = screen

        self.x1 = 0
        self.x2 = Manager.bg_size[0]

    def draw(self):
        self.screen.blit(self.mImage1, (self.x1, 0))
        self.screen.blit(self.mImage2, (self.x2, 0))

    def move(self):
        self.x1 -= 2  # first bg
        self.x2 -= 2
        if self.x1 <= -Manager.bg_size[0]:
            self.x1 = 0
        if self.x2 <= 0:
            self.x2 = Manager.bg_size[0]


class Manager(object):
    # bg image size
    bg_size = (1920, 774)
    # create new enemy
    create_enemy_id = 10
    # game over
    game_over_id = 20
    # if game ends
    is_game_over = False
    # timer
    over_time = 3

    def __init__(self):
        pygame.init()
        # initialize window
        self.screen = pygame.display.set_mode(Manager.bg_size, 0, 32)
        # load bg image
        self.background = pygame.image.load("./resources/image/background.jpg")
        # bg movement
        self.map = GameBg(self.screen)
        # initialize a group for player
        self.players = pygame.sprite.Group()
        # initialize a group for enemy
        self.enemys = pygame.sprite.Group()
        # initialize player explosion
        self.player_bomb = Hit(self.screen, "player")
        # initialize enemy explosion
        self.enemy_bomb = Hit(self.screen, "enemy")
        # initialize BGM
        self.sound = GameSound()

    def exit(self):
        print("Exit")
        pygame.quit()
        exit()

    def show_over_text(self):
        self.drawText("Gameover %d" %Manager.over_time, 100, Manager.bg_size[1]/2,
                      textHeight=50, fontColor=[255,0,0])

    def game_over_timer(self):
        self.show_over_text()
        Manager.over_time -= 1
        if Manager.over_time == 0:
            pygame.time.set_timer(Manager.game_over_id, 0)
            # restart
            Manager.over_time = 3
            Manager.is_game_over = False
            self.start_game()

    def start_game(self):
        EnemyPlane.clear_bullets()
        PlayerPlane.clear_bullets()
        manager = Manager()
        manager.main()

    def new_player(self):
        # create player's plane
        player = PlayerPlane(self.screen)
        self.players.add(player)

    def new_enemy(self):
        # create enemy's plane
        enemy = EnemyPlane(self.screen)
        self.enemys.add(enemy)

    def drawText(self, text, x, y, textHeight=30, fontColor=(255, 0, 0),
                 backgroundColor=None):
        # access font file
        font_obj = pygame.font.Font("./resources/font/Cubic_11_1.013_R.ttf", textHeight)
        text_obj = font_obj.render(text, True, fontColor, backgroundColor)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x, y)
        # draw text
        self.screen.blit(text_obj, text_rect)

    def main(self):
        self.sound.playBGM()
        self.new_player()
        # timers for create enemy
        pygame.time.set_timer(Manager.create_enemy_id, 1000)
        self.new_enemy()
        while True:
            # load bg image
            # self.screen.blit(self.background, (0, 0))
            # bg movement
            self.map.move()
            self.map.draw()

            # draw text
            self.drawText("HP: 1000", 0, 0)
            if Manager.is_game_over:
                self.show_over_text()

            for event in pygame.event.get():
                """get quit command"""
                if event.type == QUIT:
                    self.exit()
                elif event.type == Manager.create_enemy_id:
                    # create new enemy
                    self.new_enemy()
                elif event.type == Manager.game_over_id:
                    #
                    self.game_over_timer()

            # explosion
            self.player_bomb.draw()
            self.enemy_bomb.draw()

            # check if hit
            iscollide = pygame.sprite.groupcollide(self.players, self.enemys, True, True)

            if iscollide:
                Manager.is_game_over = True
                pygame.time.set_timer(Manager.game_over_id, 1000)   # start restart timer
                items = list(iscollide.items())[0]
                print(items)
                x = items[0]
                y = items[1][0]
                # player explode
                self.player_bomb.action(x.rect)
                # enemy explode
                self.enemy_bomb.action(y.rect)
                # self.enemy_bomb.action(y.rect)
                self.sound.playHitSound()

            # bullets collide
            is_enemy = pygame.sprite.groupcollide(PlayerPlane.bullets, self.enemys, True, True)
            if is_enemy:
                items = list(is_enemy.items())[0]
                y = items[1][0]
                self.enemy_bomb.action(y.rect)
                self.sound.playHitSound()

            # enemy bullets hit player
            if self.players.sprites():
                isOver = pygame.sprite.spritecollide(self.players.sprites()[0], EnemyPlane.enemy_bullets, True)
                if isOver:
                    Manager.is_game_over = True
                    pygame.time.set_timer(Manager.game_over_id, 1000)

                    self.player_bomb.action(self.players.sprites()[0].rect)
                    # remove player plane
                    self.players.remove(self.players.sprites()[0])
                    # hit sound
                    self.sound.playHitSound()

            # player and ammo display
            self.players.update()
            # enemy and ammo display
            self.enemys.update()

            pygame.display.update()
            time.sleep(0.02)


if __name__ == "__main__":
    manager = Manager()
    manager.main()

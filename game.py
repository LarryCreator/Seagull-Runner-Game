import pygame
from random import randrange
pygame.init()
fps = 60
delta_time = 1/fps
white = (255, 255, 255)
pink = (255, 182, 193)
black = (150, 200, 255)

class player():
    def __init__(self):
        self.image = pygame.transform.flip(pygame.transform.scale(pygame.image.load("PixelArt.png"), (50, 50)), True, False)
        self.position = self.image.get_rect()
        self.lifes = 0
        self.gravity = 0
        self.jump_force = int(800 * delta_time)
        self.imortallity = False
        self.imortal_t_p = False
        self.imortal_t = 0

    def flap(self, keys): #<Give the player gravity and the capability of flapping.
        self.gravity += int(fps * delta_time)
        if self.gravity > 10:
            self.gravity = 10
        if keys[pygame.K_SPACE]:
            if self.gravity >= 0:
                self.gravity = 0
                self.gravity -= self.jump_force
        self.position.y += self.gravity

    def keep_on_screen(self): #It doesn't let the player flap out of the screen.
        if self.position.y < 0:
            self.position.y = 0
        if self.imortallity:
            if self.position.y > 350:
                self.position.y = 350

    def imortal_time(self):          #if the imortallity timer reaches 0, make the player
        if self.imortal_t <= 0:      #capable of dying again.
            self.imortallity = False
            self.imortal_t_p = False

    def imortal_t_blit(self, screen): #if imortallity is activated, put the timer on the screen.
        if self.imortal_t_p:          #and take 1 second from the timer until it reaches zero,
            if self.imortal_t != 0:
                self.imortal_t -= 1 * delta_time
            font = pygame.font.Font('fonte.TTF', 15)
            text = font.render("Imortal Time: {:1f}".format(self.imortal_t), True, black)
            position = (496, 0)
            screen.blit(text, position)

class obstacles():
    def __init__(self, yposition, xposition):
        self.image = pygame.transform.scale(pygame.image.load('clouds.png'), (50, 50))
        self.position = self.image.get_rect()
        self.position.x = xposition
        self.position.y = yposition
        self.pontuation = 0
        self.last_record = 0
        self.last_r = False
        self.list = []
        self.start = True
        self.speed = 300

    def gen_new(self): #It creates a new obstacle.
        x = self.list[len(self.list) - 1].position.x + 200
        self.list.append(obstacles(randrange(0, 400 - 50, 90), x))

    def is_collided_with(self, player):                 #It checks if any of the obstacles collided with
        for i in self.list:                             #the player. If it collided and the player has an
            if i.position.colliderect(player.position): #extra life, then destroy the obstacle and take 1
                if player.lifes <= 0:                   #extra life from the player.
                    return True
                else:
                    if not player.imortallity:
                        player.lifes -= 1
                        self.list.remove(i)
                        self.gen_new()
                    return False

    def move(self): #It moves the obstacles, destroy them if they're out of the screen and creates a new one.
        for i in self.list:
            i.position.x -= int(self.speed * delta_time)
        if self.list[0].position.x <= -50:
            self.list.pop(0)
            self.pontuation += 1 #Every time that an obstacle is destroyed, the player earns 1 point.
            self.gen_new()

    def speed_up(self): #Every time the ponctuation is a multiple of 20, it speeds up the obstacles velocity a little.
        if self.pontuation >= 20 and int(self.pontuation % 20) == 0:
            self.speed += 60 * delta_time

    def first_gen(self): #It creates the first 5 obstacles in the start of the game.
        if self.start:
            self.list.append(obstacles(randrange(0, 400 - 50, 90), 750))
            for i in range(4):
                x = self.list[len(self.list) - 1].position.x + 200
                self.list.append(obstacles(randrange(0, 400 - 50, 90), x))
            self.start = False

    def blit_obstacles(self, screen): # it puts the obstacles on the screen.
        for i in self.list:
            screen.blit(i.image, i.position)

    def blit_pontuation(self, screen): #It puts the pontuation on the screen.
        font = pygame.font.Font('fonte.TTF', 32)
        text = font.render("{}".format(self.pontuation), True, white)
        position = (350, 75)
        screen.blit(text, position)

    def blit_last_record(self, screen): #If it's the second time you're playing, it puts the last record on the screen.
        font = pygame.font.Font('fonte.TTF', 15)
        text = font.render("Record: {}".format(self.last_record), True, white)
        position = (0, 0)
        screen.blit(text, position)

class life_coin():
    def __init__(self, px, py):
        self.image = pygame.transform.scale(pygame.image.load('heart.png'), (50, 50))
        self.position = self.image.get_rect(topleft = (px, py))
        self.permission = False
        self.chosen_number = randrange(63, 70)
        self.list = []

    def creation(self, obstacle):
        if obstacle.pontuation >= self.chosen_number and int(obstacle.pontuation % self.chosen_number) == 0:
            obstacle.pontuation += 1
            self.permission = True

    def spawn(self):
        if self.permission:
            self.list.append(life_coin(780, randrange(0, 350)))
            self.permission = False

    def is_collided_with(self, player):
        return self.list[0].position.colliderect(player)

    def blit(self, screen): #if a coin is spawned, put it on the screen.
        try:
            screen.blit(self.list[0].image, self.list[0].position)
        except:
            pass

    def move(self, player, obstacle): #move the coin and if it collides with the player,
        try:                          #then give him 1 extra life and removes the coin from the screen.
            self.list[0].position.x -= int((obstacle.speed + 100) * delta_time)
            if self.is_collided_with(player.position):
                player.lifes += 1
                self.list.remove(self.list[0])
            elif self.list[0].position.x < -50:
                self.list.remove(self.list[0])
        except:
            pass

    def extra_life_blit(self, screen, player): #blits the extra life gui on the screen
        if player.lifes == 0:
            font = pygame.font.Font('fonte.TTF', 15)
            text = font.render(': {}'.format(player.lifes), True, white)
        else:                                            #if the player has at least 1 extra life,
            font = pygame.font.Font('fonte.TTF', 15)     #show it pink.
            text = font.render(': {}'.format(player.lifes), True, pink)
        position = (152, 0)
        screen.blit(pygame.transform.scale(self.image, (20, 20)), (130, 0))
        screen.blit(text, position)

class imortallity_coin():
    def __init__(self, px, py):
        self.image = pygame.transform.scale(pygame.image.load('imortal_coin.png'), (50, 50))
        self.position = self.image.get_rect(topleft = (px, py))
        self.permission = False
        self.chosen_number = 41
        self.list = []
    def creation(self, obstacle):
        if obstacle.pontuation >= self.chosen_number and int(obstacle.pontuation % self.chosen_number) == 0:
            obstacle.pontuation += 1 #If the pontuation is equal or is a multiple
            self.permission = True   #of the chosen number, the permission
                                     #for spawning the coin is granted.
    def spawn(self):
        if self.permission: #if the permission is granted, then spawn the coin.
            self.list.append(imortallity_coin(780, randrange(0, 350)))
            self.permission = False

    def is_collided_with(self, player): #if the coin collided with the player, return True
        return self.list[0].position.colliderect(player)

    def blit(self, screen): #if a coin is spawned, put it on the screen.
        try:
            screen.blit(self.list[0].image, self.list[0].position)
        except:
            pass

    def move(self, player, obstacle): #move the coin and if it collides with the player,
        try:                          #then give him immortality and take 1 point from him.
            self.list[0].position.x -= int((obstacle.speed + 100) * delta_time)
            if self.is_collided_with(player.position):
                player.imortallity = True
                player.imortal_t_p = True
                player.imortal_t = 10 #<the imortallity will only last 10 seconds.
                obstacle.pontuation -= 1
                self.list.remove(self.list[0])
            elif self.list[0].position.x < -50:
                self.list.remove(self.list[0])
        except:
            pass
class game():
    def __init__(self):
        self.start = True
        self.screen = pygame.display.set_mode((700, 400))
        self.background_image = pygame.transform.scale(pygame.image.load("back.png"), (700, 400))
        self.back_position = self.background_image.get_rect()
        self.back_position2 = self.background_image.get_rect()
        self.clock = pygame.time.Clock()
        self.player = player()
        self.obs = obstacles(750, 750)
        self.life_coin = life_coin(750, 750)
        self.imortallity_coin = imortallity_coin(750, 750)

    def move_background(self): #It moves the background image.
        self.back_position.x -= int(60 * delta_time)
        self.back_position2.x -= int(60 * delta_time)
        if self.back_position2.x == 1:
            self.back_position.x = 700
        elif self.back_position.x == 1:
            self.back_position2.x = 700

    def menu_screen(self): #It creates the menu screen.
        font = pygame.font.Font('fonte.TTF', 40)
        font2 = pygame.font.Font('fonte.TTF', 20)
        text = font.render("Seagull Runner", True, white)
        position = (110, 100)
        text2 = font2.render("Press Space to start...", True, white)
        position2 = (180, 200)
        if self.start: #If it's the first time you're playing, put the background in the position 0 and puts
            self.back_position.x = 0 #another one in front of it, to start the endless background loop.
            self.back_position2.x = self.back_position.x + 700
            self.start = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.main_loop()
            self.move_background()
            self.screen.blit(self.background_image, self.back_position)
            self.screen.blit(self.background_image, self.back_position2)
            self.screen.blit(text, position)
            self.screen.blit(text2, position2)
            pygame.display.update()

    def main_loop(self):
        self.player.position.y = 200
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit(0)
            keys = pygame.key.get_pressed()
            if self.obs.is_collided_with(self.player) or self.player.position.y > 380:
                if not self.player.imortallity:  #if the player collided with an obstacle or fell off the
                    self.obs.start = True        #screen while not being imortal by the imortallity coin,
                    self.obs.speed = 300         #then he dies, everything is reseted and if the pontuation
                    self.player.lifes = 0        #was high enough, store it in the last record variable.
                    self.obs.list.clear()
                    self.imortallity_coin.list.clear()
                    self.life_coin.list.clear()
                    if self.obs.pontuation > self.obs.last_record:
                        self.obs.last_record = self.obs.pontuation
                    self.obs.pontuation = 0
                    self.menu_screen()
            self.clock.tick(fps)                                 #Here is where everything is
            self.imortallity_coin.creation(self.obs)             #put together.
            self.imortallity_coin.spawn()
            self.imortallity_coin.move(self.player, self.obs)
            self.life_coin.creation(self.obs)
            self.life_coin.spawn()
            self.life_coin.move(self.player, self.obs)
            self.move_background()
            self.player.flap(keys)
            self.player.keep_on_screen()
            self.player.imortal_time()
            self.obs.first_gen()
            self.obs.move()
            self.obs.speed_up()
            self.screen.blit(self.background_image, self.back_position)
            self.screen.blit(self.background_image, self.back_position2)
            self.player.imortal_t_blit(self.screen)
            self.imortallity_coin.blit(self.screen)
            self.life_coin.blit(self.screen)
            self.life_coin.extra_life_blit(self.screen, self.player)
            self.obs.blit_obstacles(self.screen)
            self.obs.blit_pontuation(self.screen)
            self.obs.blit_last_record(self.screen)
            self.screen.blit(self.player.image, (30, self.player.position.y))
            pygame.display.update()

game = game()
pygame.display.set_caption("Seagull Runner")
pygame.display.set_icon(game.player.image)
game.menu_screen()

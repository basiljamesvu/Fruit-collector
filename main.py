import random
import time
import pygame
from pygame.locals import *

apple_x = 200
apple_y = 0
basket_x = 375
basket_y = 375
score = 0
life = 3
delay = 0.2

class Bomb:
    def __init__(self, parent_surface):
        self.bomb = pygame.image.load("resources/bomb.jpg").convert()
        self.parent_surface = parent_surface
        self.basket = Basket(self.parent_surface)
        self.apple = Apple(self.parent_surface)

    def bomb_issue(self):
        self.parent_surface.fill((3, 252, 202))
        self.parent_surface.blit(self.bomb, (apple_x, apple_y))
        self.basket.draw_basket()
        self.apple.display()
        pygame.display.flip()


class Apple:
    def __init__(self, parent_surface):
        self.apple = pygame.image.load("resources/apple.jpg").convert()
        self.parent_surface = parent_surface
        self.basket = Basket(self.parent_surface)
        self.create_apple()

    def create_apple(self):
        global delay
        global apple_x
        global apple_y
        delay -= 0.001
        apple_x = random.randint(100, 700)
        apple_y = 0
        self.parent_surface.blit(self.apple, (apple_x, apple_y))

    def move_apple_automatically(self):
        global apple_y
        apple_y += 25
        self.parent_surface.fill((3, 252, 202))
        self.parent_surface.blit(self.apple, (apple_x, apple_y))
        self.display()
        self.basket.draw_basket()

    def display(self):
        font = pygame.font.Font(pygame.font.get_default_font(), 36)
        # now print the text
        text_surface = font.render(f'Score: {score}', True, (0, 0, 0))
        self.parent_surface.blit(text_surface, dest=(840, 20))
        text_surface = font.render(f'Life: {life}', True, (0, 0, 0))
        self.parent_surface.blit(text_surface, dest=(850, 60))


class Basket:
    def __init__(self, parent_surface):

        self.basket = pygame.image.load("resources/basket.jpg").convert()
        self.parent_surface = parent_surface
        self.parent_surface.blit(self.basket, (basket_x, basket_y))

    def move_basket(self, position):
        global basket_x
        self.parent_surface.fill((3, 252, 202))
        if position == "right":
            basket_x += 40
        else:
            basket_x -= 40
        self.parent_surface.blit(self.basket, (basket_x, basket_y))
        pygame.display.flip()

    def draw_basket(self):
        self.parent_surface.blit(self.basket, (basket_x, basket_y))
        pygame.display.flip()


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000, 500))
        pygame.display.set_caption('Fruit Collector')
        self.surface.fill((3, 252, 202))
        self.basket = Basket(self.surface)
        self.apple = Apple(self.surface)
        self.bomb = Bomb(self.surface)
        pygame.mixer.music.load("resources/explosion.wav")

        pygame.display.flip()


    def collision(self):
        if basket_y + 123 >= apple_y >= basket_y:
            if basket_x + 75 >= apple_x >= basket_x:
                return True

    def run(self):
        running = True
        global life
        global score
        while running:
            if apple_y == 500:
                if apple_x % 2 == 0: # bomb condition
                    pass
                else:
                    life -= 1
                print("you missed the fruit")
                if life == 0:
                    print(f'Game Over!! your score is {score}')
                    break
                self.apple.create_apple()
            self.apple.move_apple_automatically()
            if apple_x % 2 == 0 and apple_y >= 300:
                self.bomb.bomb_issue()

            time.sleep(abs(delay))
            if self.collision() and apple_x % 2 == 0:
                pygame.mixer.music.play()
                print(f'Game Over!! your score is {score}')
                break
            elif self.collision():
                print("you collected the fruit")
                apple_sound = pygame.mixer.Sound("resources/laser.wav")
                apple_sound.play()
                score += 1

                self.apple.create_apple()
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RIGHT:
                        self.basket.move_basket("right")

                    if event.key == K_LEFT:
                        self.basket.move_basket("left")

    def display(self):
        self.surface.fill((3, 252, 202))
        font = pygame.font.Font(pygame.font.get_default_font(), 36)

        # now print the text
        text_surface = font.render('Game Over!!', True, (0, 0, 0))
        self.surface.blit(text_surface, dest=(400, 100))
        text_surface = font.render(f'Score: {score}', True, (0, 0, 0))
        self.surface.blit(text_surface, dest=(450, 150))
        pygame.display.flip()
        time.sleep(2)


if __name__ == '__main__':
    game = Game()
    game.run()
    game.display()




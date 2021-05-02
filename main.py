import pygame
from pygame.locals import *
import time

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = 250
        self.y = 250
        self.direction = 'right'

    def draw(self):
        self.parent_screen.fill((252, 157, 3)) # sin esta linea el bloque anterior se queda pintado
        self.parent_screen.blit(self.block, (self.x, self.y))
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_down(self):
        self.direction = 'down'

    def move_up(self):
        self.direction = 'up'

    def walk(self):
        if self.direction == 'right':
            self.x += 10
        if self.direction == 'left':
            self.x -= 10
        if self.direction == 'up':
            self.y -= 10
        if self.direction == 'down':
            self.y += 10
        
        self.draw()



class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((500, 500))
        self.surface.fill((252, 157, 3))
        self.snake = Snake(self.surface)
        self.snake.draw()

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_UP:
                        self.snake.move_up()

                    if event.key == K_DOWN:
                        self.snake.move_down()

                    if event.key == K_RIGHT:
                        self.snake.move_right()

                    if event.key == K_LEFT:
                        self.snake.move_left()

                elif event.type == QUIT:
                    running = False
            self.snake.walk()
            time.sleep(0.1)


if __name__ == "__main__":
    game =Game()
    game.run()
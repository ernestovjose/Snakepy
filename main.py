import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (0, 0, 0)
dificulty = 0.2

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE*2
        self.y = SIZE*2

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()  

    def move(self):
        while True:
            self.x = random.randint(1, 29)*SIZE
            self.y = random.randint(1, 17)*SIZE
            if self.x > 0 and self.x <= 1200 and self.y > 0 and self.y <= 720:
                break;

class Snake:
    def __init__(self, surface, length):
        self.length = length
        self.parent_screen = surface
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'right'

    def increase_tail(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
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
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        
        self.draw()

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.game_over_sound = pygame.mixer.Sound('resources/game_over.mp3')
        self.chewing_sound = pygame.mixer.Sound('resources/chewing.mp3')
        self.play_background_music()
        self.surface = pygame.display.set_mode((1200, 720))
        self.snake = Snake(self.surface, 3)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
    
    def change_dificulty(self):
        global dificulty
        if (self.snake.length) % 5 == 0:
            dificulty -= 0.03

    def render_background(self):
        bg = pygame.image.load("resources/back.png")
        self.surface.blit(bg, (0,0))

    def play_background_music(self):
        pygame.mixer.music.load("resources/background.mp3")
        pygame.mixer.music.play()
    
    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.snake = Snake(self.surface, 3)
        self.apple = Apple(self.surface)

    def game_over(self):
        pygame.mixer.music.pause()
        self.play_sound('game_over')
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 50, bold=True, italic=False)
        font1 = pygame.font.SysFont('arial', 30, bold=True, italic=False)
        end_message = font.render(f"YOU DIED", True, (139, 0, 0))
        self.surface.blit(end_message, (600, 400))
        pygame.display.flip()
        time.sleep(5)
        if self.snake.length*20 == 60:
            score = font1.render(f"Score: 0 press enter to reset", True, (255, 255, 255))
        else:
            score = font1.render(f"Score: {self.snake.length*20} Press enter to reset", True, (255, 255, 255))
        self.surface.blit(score, (600, 450))
        pygame.display.flip()

    def display_score(self):
        font = pygame.font.SysFont('arial', 30, bold=True, italic=False)
        score = font.render(f"Score: {self.snake.length*20}", True, (255, 255, 255))
        if self.snake.length <=3:
            score = font.render(f"Score: 0", True, (255, 255, 255))
            self.surface.blit(score, (1000, 10))    
        else:
            self.surface.blit(score, (1000, 10))    

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def is_collision_wall(self, x1, y1, x2, y2):
        if x1 >= x2 or  y1 >= y2 or x1 < 0 or y1 < 0:
                return True
        return False    

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound('chewing')    
            self.snake.increase_tail()
            self.change_dificulty()
            self.apple.move()

        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Game Over"

        if self.is_collision_wall(self.snake.x[0], self.snake.y[0], 1200, 720):
            raise "Game Over"      

    def run(self):
        global dificulty
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        dificulty = 0.2
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:    

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
            try:
                if not pause:
                    self.play()

            except Exception as e:
                print(e)
                self.game_over()
                pause = True
                self.reset()

            time.sleep(dificulty)


if __name__ == "__main__":
    game =Game()
    game.run()
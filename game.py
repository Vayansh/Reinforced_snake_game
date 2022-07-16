import pygame
from collections import namedtuple
import random
from enum import Enum

pygame.init()

# named tuple named Point
Point = namedtuple('Point','x,y')
font = pygame.font.Font('arial.ttf', 25)

class Direction(Enum):
    right = 1
    left = 2
    up = 3
    down = 4

# color codes 
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)
GREEN = (0,128,0)
YELLOW = (255,255,0)


#some literals 
BLOCKSIZE = 20
SPEED = 20

# main class
class game:
    #init of game
    def __init__(self,w = 640, h = 480):
         self.w = w
         self.h = h
         # init_display
         self.display = pygame.display.set_mode((self.w,self.h))
         pygame.display.set_caption('Snake')
         self.clock= pygame.time.Clock()
         
         # init position of snake
         self.direction = Direction.right
         self.head = Point(self.w/2, self.h/2)
         self.snake = [self.head,
                       Point(self.head.x-BLOCKSIZE,self.head.y),
                       Point(self.head.x-(2*BLOCKSIZE),self.head.y)]
         self.food = None
         self.score = 0
         self._placefood()
         
    # placing of food 
    
    def _placefood(self):
        x = random.randint(0,(self.w - BLOCKSIZE)//BLOCKSIZE) * BLOCKSIZE
        y = random.randint(0,(self.h - BLOCKSIZE)//BLOCKSIZE) * BLOCKSIZE
        self.food = Point(x,y)
        if self.food in self.snake:
            self._placefood()
    
    
    def play_step(self):
    
        # 1. user input    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.left
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.right
                elif event.key == pygame.K_UP:
                    self.direction = Direction.up
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.down

                                        
        # 2. move  
        self.move(self.head.x,self.head.y) #update self.head
        self.snake.insert(0,self.head)
        
       
       #check if there is any collision 
       
        self.game_over= False
        self.collision()
        if self.game_over == True:
            return self.game_over, self.score
        
        #place the food or just move
        self.check_score()
        
        #update ui
        self.update_ui()
        self.clock.tick(SPEED)
        return self.game_over , self.score
        
        
    def update_ui(self):
        self.display.fill(BLACK)
        for pt in self.snake:
            pygame.draw.ellipse(self.display,BLUE1,pygame.Rect(pt.x,pt.y,BLOCKSIZE+6,BLOCKSIZE+6))
            pygame.draw.ellipse(self.display,BLUE2,pygame.Rect(pt.x+8,pt.y+8,8,8))
        
        pygame.draw.ellipse(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCKSIZE, BLOCKSIZE))
        pygame.draw.line(self.display, GREEN ,(self.food.x+(BLOCKSIZE/4),self.food.y+(BLOCKSIZE/4)),(self.food.x-(BLOCKSIZE/4),self.food.y-(BLOCKSIZE/4)),2)
        text = font.render("Score : " + str(self.score),True,WHITE)
        self.display.blit(text,[0,0])
        pygame.display.flip()    
    
    def check_score(self):
        if self.food == self.head:
            self.score += 1
            self._placefood()
        else:
            self.snake.pop()
                
       
    #check_ collision_
    def collision(self):
        if self.head.x > self.w - BLOCKSIZE or self.head.x < 0 or self.head.y > self.h - BLOCKSIZE or self.head.y < 0:
            self.game_over = True
            return
        elif self.head in self.snake[1:]:
            self.game_over = True
            return
       
     
    # update head of snake      
    def move(self,x,y):
        if self.direction == Direction.right:
            x+=BLOCKSIZE
        elif self.direction == Direction.left:
            x-=BLOCKSIZE
        elif self.direction == Direction.down:
            y+=BLOCKSIZE
        elif self.direction == Direction.up:
            y-=BLOCKSIZE
        
        self.head = Point(x,y)
                        
if __name__ == "__main__" :                        
    game = game()
while True:
    game_over,score = game.play_step()
    
    
    if game_over == True:
        break
    
print("Final Score : "+ str(score))
pygame.quit()
    
    
    
                        
import pygame
from collections import namedtuple
import random
from enum import Enum
import numpy as np


pygame.init()

# named tuple named Point
Point = namedtuple('Point','x,y')
font = pygame.font.Font('arial.ttf', 25)

class Direction(Enum):
    right = 1
    down = 2
    left = 3
    up = 4

# color codes 
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)


#some literals 
BLOCKSIZE = 20
SPEED = 40

# play_step(action)

# main class
class Game:
    #init of game
    def __init__(self,w = 640, h = 480):
         self.w = w
         self.h = h
         # init_display
         self.display = pygame.display.set_mode((self.w,self.h))
         pygame.display.set_caption('Snake')
         self.clock= pygame.time.Clock()
         self.reset()    

    # init position of snake     
    def reset(self):
         self.direction = Direction.right
         self.head = Point(self.w/2, self.h/2)
         self.snake = [self.head,
                       Point(self.head.x-BLOCKSIZE,self.head.y),
                       Point(self.head.x-(2*BLOCKSIZE),self.head.y)]
         self.food = None
         self.score = 0
         self._placefood()
         self.frame_iteration = 0

    # placing of food 
    
    def _placefood(self):
        x = random.randint(0,(self.w - BLOCKSIZE)//BLOCKSIZE) * BLOCKSIZE
        y = random.randint(0,(self.h - BLOCKSIZE)//BLOCKSIZE) * BLOCKSIZE
        self.food = Point(x,y)
        if self.food in self.snake:
            self._placefood()
    
    
    def play_step(self,action):
        self.frame_iteration += 1 
        # 1. user input    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT
                quit()
            
                                        
        # 2. move  
        self.move(action) #update self.head
        self.snake.insert(0,self.head)
        
       
       #check if there is any collision 
        reward =0
        self.game_over= False
        if self.collision() or self.frame_iteration > 100*len(self.snake):
            self.game_over = True
            reward = -10
            return reward,self.game_over, self.score
        
        #place the food or just move
        if self.food == self.head:
            self.score += 1
            reward = 10
            self._placefood()
        else:
            self.snake.pop()
                
        #update ui
        self.update_ui()
        self.clock.tick(SPEED)
        return reward,self.game_over , self.score
        
        
    def update_ui(self):
        self.display.fill(BLACK)
        for pt in self.snake:
            pygame.draw.rect(self.display,BLUE1,pygame.Rect(pt.x,pt.y,BLOCKSIZE,BLOCKSIZE))
            pygame.draw.rect(self.display,BLUE2,pygame.Rect(pt.x+4,pt.y+4,12,12))
        
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCKSIZE, BLOCKSIZE),border_radius=8)
        
        text = font.render("Score : " + str(self.score),True,WHITE)
        self.display.blit(text,[0,0])
        pygame.display.flip()    
    
    
       
    #check_ collision_
    def collision(self,pt = None):
        if pt == None:
            pt = self.head
        if (pt.x > self.w - BLOCKSIZE) or (pt.x < 0) or (pt.y > self.h - BLOCKSIZE) or (pt.y < 0):
            return True
        elif pt in self.snake[1:]:
            return True
        return False
     
    # update head of snake      
    def move(self,action):
        x = self.head.x
        y = self.head.y 
        
        #action [1,0,0] or [0,1,0] or [0,0,1]
        
        clock_wise = [Direction.right,Direction.down,Direction.left,Direction.up]
        id = clock_wise.index(self.direction)
        
        
        if np.array_equal( action , [1,0,0]):
            new_dir = clock_wise[id]
        elif np.array_equal( action , [0,1,0]):
            new_dir = clock_wise[(id+1)%4]
        elif np.array_equal (action, [0,0,1]):
            new_dir = clock_wise[(id-1)%4]
        
        #update self direction
            
        self.direction = new_dir    
        
        #update coordinate of head
        
        if self.direction == Direction.right:
            x+=BLOCKSIZE
        elif self.direction == Direction.left:
            x-=BLOCKSIZE
        elif self.direction == Direction.down:
            y+=BLOCKSIZE
        elif self.direction == Direction.up:
            y-=BLOCKSIZE        
         
        # update head    
        self.head = Point(x,y)
                        
    
    
    
                        
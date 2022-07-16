import numpy as np
import torch
from game_AI import Game, Direction, Point,BLOCKSIZE
from collections import deque
import random
from model import Linear_QNet, QTrainer
from helper import plot


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:
    def __init__(self):
        self.n_games = 0   # no of games played 
        self.epsilon = 0   # randomness
        self.gamma = 0.9   #discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(11,256,3)
        self.trainer = QTrainer(self.model,LR,self.gamma)
        
    def get_state(self,game):
        head = game.snake[0]
        point_l = Point(head.x-BLOCKSIZE,head.y)
        point_r = Point((head.x+BLOCKSIZE),head.y)
        point_u = Point(head.x,(head.y-BLOCKSIZE))
        point_d = Point(head.x,(head.y+BLOCKSIZE))
        
        dir_l = game.direction == Direction.left
        dir_r = game.direction == Direction.right
        dir_u = game.direction == Direction.up
        dir_d = game.direction == Direction.down
        
        state = [
            #danger straight
            (dir_r and game.collision(point_r)) or
            (dir_u and game.collision(point_u)) or
            (dir_d and game.collision(point_d)) or
            (dir_l and game.collision(point_l)),
            
            #danger right
            (dir_r and game.collision(point_d)) or
            (dir_d and game.collision(point_l)) or
            (dir_l and game.collision(point_u)) or
            (dir_u and game.collision(point_r)),
            
            #danger left
            (dir_r and game.collision(point_u)) or 
            (dir_u and game.collision(point_l)) or
            (dir_l and game.collision(point_d)) or
            (dir_d and game.collision(point_r)),
            
            #Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            #food location
            game.food.x < head.x,
            game.food.x > head.x,
            game.food.y < head.y,
            game.food.y > head.y,
            
            
        ]
        return np.array(state,dtype=int)
        
    def get_action(self,state):
        #random moves: trade off exploration/ explotation
        self.epsilon = 10 - self.n_games
        final_move = [0,0,0]
        if random.randint(0,200) < self.epsilon:
            move = random.randint(0,2)
            final_move[move] = 1
        else:
            state0 =  torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
                
        return final_move

    def train_short_memory(self,state,action,reward,next_state,g_o):
        self.trainer.train_step(state,action,reward,next_state,g_o)
    
    
    def remember(self,state,action,reward,next_state,g_o):
        self.memory.append((state,action,reward,next_state,g_o))   


    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory,BATCH_SIZE)
        else:
            mini_sample = self.memory
        
        states,actions,rewards,next_states,g_os = zip(*mini_sample)
        self.trainer.train_step(states,actions,rewards,next_states,g_os)        
        
    
    
def train():
    game = Game()
    agent = Agent()
    record = 0
    total_scores = 0
    plot_scores = []
    plot_mean_scores =[]
    
    while True:
        #get current state
        state_old = agent.get_state(game)
        
        # get action or move
        move = agent.get_action(state_old)
        
        # perform move and get new state
        reward,g_o,score = game.play_step(move)
        next_state = agent.get_state(game)
        
        #train short memory
        agent.train_short_memory(state_old,move,reward,next_state,g_o)
        
        #remember
        agent.remember(state_old,move,reward,next_state,g_o)
        
        if g_o:
            game.reset()
            agent.n_games+=1
            agent.train_long_memory()
            
            if score > record:
                record =score
                agent.model.save()
                
            print("Game ", agent.n_games,' Scores ', score , ' Records: ',record)    
            
            plot_scores.append(score)
            total_scores += score
            mean_score = total_scores/agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores,plot_mean_scores)
            
if __name__ == "__main__":
    train()
    
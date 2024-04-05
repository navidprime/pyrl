from games import *
from qlearning import QLearner
from decision_tree import  DecisionTreeLearner
import os,time

total = 4_000
actions = [Move.Left, Move.Right, Move.Down, Move.Up]
ep_length = 2_000
config = {
    "lr":0.1,
    "gamma":0.99,
    
    "batch_size":1024,
    "longtrain_after":128,
    "memory_size":2048
}
learner = DecisionTreeLearner # choose the learner
agent = learner(actions,ep_length, 
                            **config)

game = SimpleGame()

w = 0
t1 = time.time()
for i in range(total):
    os.system("cls")
    print(f"iteration : {i}, wins : {w}, time : {round(time.time()-t1)}s")
    
    action = agent.predict(game.pos)
    prev_pos, cur_pos, status = game.move(action)
    reward = 20 if status == Status.Win else -10 if status == Status.Lose else 0
    if reward > 0:
        w+=1
        
    agent.learn(prev_pos, action, cur_pos, reward)

agent.print_learn_summary()

print("going to test mode...")
time.sleep(10)

game = SimpleGame()

agent2 = agent
agent2.test_mode = True

while True:
    os.system("cls")
    game.show_map()
    time.sleep(0.1)

    move = agent2.predict(game.pos)

    prev_pos, cur_pos, status = game.move(move)
    if (status == Status.Lose):
        print("Game Lose")
        break
    elif (status == Status.Win):
        print("Game Win")
        break
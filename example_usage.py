from game import *
from agent import QLearning
import msvcrt,os,time

def mapping(x:int):
    if (x == 0):
        return Move.Left
    elif (x == 1):
        return Move.Right
    elif (x == 2):
        return Move.Up
    elif (x == 3):
        return Move.Down

total = 100_000
agent = QLearning(4,epsilon_length=int(total/2))
game = Game()

for i in range(total):
    action_i = agent.predict(game.pos)
    action = mapping(action_i)
    prev_pos, cur_pos, status = game.move(action)
    reward = 10 if status == Status.Win else -10 if status == Status.Lose else 0

    agent.learn(prev_pos, action_i, cur_pos, reward)

agent.save_q("saved.pkl")


agent2 = QLearning(4)
agent2.load_q("saved.pkl")
agent2.exit_train_mode()
while True:
    os.system("cls")
    game.show_map()
    time.sleep(1)

    move = mapping(agent2.predict(game.pos))

    prev_pos, cur_pos, status = game.move(move)
    if (status == Status.Lose):
        print("Game Over")
        break
    elif (status == Status.Win):
        print("Game Win")
        break
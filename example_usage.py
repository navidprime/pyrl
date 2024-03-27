from game import *
from agent import QLearning
import msvcrt,os,time

actions = [Move.Left, Move.Right, Move.Up, Move.Down]
total = 100_000
agent = QLearning(actions,epsilon_length=int(total/2))
game = Game()

for i in range(total):
    action = agent.predict(game.pos)
    prev_pos, cur_pos, status = game.move(action)
    reward = 10 if status == Status.Win else -10 if status == Status.Lose else 0

    agent.learn(prev_pos, action, cur_pos, reward)

agent.save_q("saved.pkl")
# print(agent.get_qsize())

agent2 = QLearning([Move.Left, Move.Right, Move.Up, Move.Down])
agent2.load_q("saved.pkl")
agent2.exit_train_mode()
while True:
    os.system("cls")
    game.show_map()
    time.sleep(1)

    move = agent2.predict(game.pos)

    prev_pos, cur_pos, status = game.move(move)
    if (status == Status.Lose):
        print("Game Over")
        break
    elif (status == Status.Win):
        print("Game Win")
        break
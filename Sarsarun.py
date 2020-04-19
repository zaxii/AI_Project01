from Maze import Maze
from RLmain import SarsaTable
from RLmain import SarsaLamdaTable
import matplotlib.pyplot as plt
import numpy as np
import sys

x_plt = np.zeros(100)
y_plt = np.zeros(100)


def update():
    for episode in range(100):
        # initial observation
        observation = env.reset()

        # RL choose action based on observation
        action = RL.choose_action(str(observation))
        print(episode)
        step = 0

        while True:
            if len(sys.argv) == 2 and sys.argv[1] == '-show':
                env.render()

            observation_, reward, done = env.step(action)

            action_ = RL.choose_action(str(observation_))

            RL.learn(str(observation), action, reward, str(observation_), action_)

            observation = observation_
            action = action_
            step += 1

            if done:
                x_plt[episode] = episode + 1
                y_plt[episode] = step
                step = 0
                break

    print('game over')
    plt.plot(x_plt, y_plt)
    for x, y in zip(x_plt, y_plt):
        if y < 50:
            plt.text(x, y, y, ha='center', va='bottom', fontsize=10)
    plt.savefig('./Sarsa.jpg')
    plt.show()
    print(RL.q_table)
    env.destroy()


if __name__ == "__main__":
    env = Maze()
    RL = SarsaTable(actions=list(range(env.n_actions)))

    if sys.argv == 2 and sys.argv[1] == '-show':
        env.after(100, update)
    else:
        env.after(0, update)
    env.mainloop()

import json

import numpy as np
from utils import *
import random
import matplotlib.pyplot as plt
from genMaze import gen_maze


def create_Mtable(cur_maze):
    return np.zeros((len(cur_maze), len(cur_maze[0])))


def iteration_M(cur_maze, value_record):
    new_value_record = np.zeros((len(cur_maze), len(cur_maze[0])))
    x_size, y_size = len(cur_maze), len(cur_maze[0])
    for x in range(x_size):
        for y in range(y_size):
            # 如果在地图上是障碍、陷阱或者终点，那么跳过
            if cur_maze[x][y] == 0:
                new_value_record[x][y] = Bellman(value_record, cur_maze, x, y)

    file = open('Markov_table.txt', 'w')
    file.write(json.dumps(new_value_record))
    return new_value_record


def Bellman(value_record, cur_maze, x, y):
    x_size, y_size = len(cur_maze), len(cur_maze[0])
    cur_value = 0
    # up
    if x == 0:
        cur_value += wall_reward + gamma * value_record[x][y]
    elif y == 0:  # 最小大于2*2
        cur_value += 0.2 * (wall_reward + gamma * value_record[x][y])
        if cur_maze[x-1][y] == wall_flag:
            cur_value += 0.6 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x-1][y] == trap_flag:
            cur_value += 0.6 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.6 * (cur_maze[x-1][y] + gamma * value_record[x-1][y])

        if cur_maze[x - 1][y+1] == wall_flag:
            cur_value += 0.2 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x - 1][y+1] == trap_flag:
            cur_value += 0.2 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.2 * (cur_maze[x - 1][y+1] + gamma * value_record[x - 1][y+1])

    elif y == y_size - 1:
        if cur_maze[x - 1][y - 1] == wall_flag:
            cur_value += 0.2 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x - 1][y - 1] == trap_flag:
            cur_value += 0.2 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.2 * (cur_maze[x - 1][y - 1] + gamma * value_record[x - 1][y - 1])

        if cur_maze[x - 1][y] == wall_flag:
            cur_value += 0.6 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x - 1][y] == trap_flag:
            cur_value += 0.6 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.6 * (cur_maze[x - 1][y] + gamma * value_record[x - 1][y])

        cur_value += 0.2 * (wall_reward + gamma * value_record[x][y])

    else:
        if cur_maze[x - 1][y - 1] == wall_flag:
            cur_value += 0.2 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x - 1][y - 1] == trap_flag:
            cur_value += 0.2 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.2 * (cur_maze[x - 1][y - 1] + gamma * value_record[x - 1][y - 1])

        if cur_maze[x - 1][y] == wall_flag:
            cur_value += 0.6 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x - 1][y] == trap_flag:
            cur_value += 0.6 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.6 * (cur_maze[x - 1][y] + gamma * value_record[x - 1][y])

        if cur_maze[x - 1][y+1] == wall_flag:
            cur_value += 0.2 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x - 1][y+1] == trap_flag:
            cur_value += 0.2 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.2 * (cur_maze[x - 1][y+1] + gamma * value_record[x - 1][y+1])

    value = cur_value
    cur_value = 0

    # down
    if x == x_size - 1:
        cur_value += wall_reward + gamma * value_record[x][y]
    elif y == 0:  # 最小大于2*2
        cur_value += 0.2 * (wall_reward + gamma * value_record[x][y])
        if cur_maze[x + 1][y] == wall_flag:
            cur_value += 0.6 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x + 1][y] == trap_flag:
            cur_value += 0.6 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.6 * (cur_maze[x + 1][y] + gamma * value_record[x + 1][y])

        if cur_maze[x + 1][y + 1] == wall_flag:
            cur_value += 0.2 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x + 1][y + 1] == trap_flag:
            cur_value += 0.2 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.2 * (cur_maze[x + 1][y + 1] + gamma * value_record[x + 1][y + 1])

    elif y == y_size - 1:
        if cur_maze[x + 1][y - 1] == wall_flag:
            cur_value += 0.2 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x + 1][y - 1] == trap_flag:
            cur_value += 0.2 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.2 * (cur_maze[x + 1][y - 1] + gamma * value_record[x + 1][y - 1])

        if cur_maze[x + 1][y] == wall_flag:
            cur_value += 0.6 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x + 1][y] == trap_flag:
            cur_value += 0.6 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.6 * (cur_maze[x + 1][y] + gamma * value_record[x + 1][y])

        cur_value += 0.2 * (wall_reward + gamma * value_record[x][y])

    else:
        if cur_maze[x + 1][y - 1] == wall_flag:
            cur_value += 0.2 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x + 1][y - 1] == trap_flag:
            cur_value += 0.2 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.2 * (cur_maze[x + 1][y - 1] + gamma * value_record[x + 1][y - 1])

        if cur_maze[x + 1][y] == wall_flag:
            cur_value += 0.6 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x + 1][y] == trap_flag:
            cur_value += 0.6 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.6 * (cur_maze[x + 1][y] + gamma * value_record[x + 1][y])

        if cur_maze[x + 1][y + 1] == wall_flag:
            cur_value += 0.2 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x + 1][y + 1] == trap_flag:
            cur_value += 0.2 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.2 * (cur_maze[x + 1][y + 1] + gamma * value_record[x + 1][y + 1])

    value = max(value, cur_value)
    cur_value = 0

    # left
    if y == 0:
        cur_value += 0.2 * (wall_reward + gamma * value_record[x][y])
    elif x == 0:  # 最小大于2*2
        cur_value += 0.2 * (wall_reward + gamma * value_record[x][y])

        if cur_maze[x][y-1] == wall_flag:
            cur_value += 0.6 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x][y-1] == trap_flag:
            cur_value += 0.6 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.6 * (cur_maze[x][y-1] + gamma * value_record[x][y-1])

        if cur_maze[x + 1][y - 1] == wall_flag:
            cur_value += 0.2 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x + 1][y - 1] == trap_flag:
            cur_value += 0.2 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.2 * (cur_maze[x + 1][y - 1] + gamma * value_record[x + 1][y - 1])

    elif x == x_size - 1:
        if cur_maze[x - 1][y - 1] == wall_flag:
            cur_value += 0.2 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x - 1][y - 1] == trap_flag:
            cur_value += 0.2 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.2 * (cur_maze[x - 1][y - 1] + gamma * value_record[x - 1][y - 1])

        if cur_maze[x][y - 1] == wall_flag:
            cur_value += 0.6 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x][y - 1] == trap_flag:
            cur_value += 0.6 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.6 * (cur_maze[x][y - 1] + gamma * value_record[x][y - 1])

        cur_value += 0.2 * (wall_reward + gamma * value_record[x][y])

    else:
        if cur_maze[x - 1][y - 1] == wall_flag:
            cur_value += 0.2 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x - 1][y - 1] == trap_flag:
            cur_value += 0.2 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.2 * (cur_maze[x - 1][y - 1] + gamma * value_record[x - 1][y - 1])

        if cur_maze[x][y - 1] == wall_flag:
            cur_value += 0.6 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x][y - 1] == trap_flag:
            cur_value += 0.6 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.6 * (cur_maze[x][y - 1] + gamma * value_record[x][y - 1])

        if cur_maze[x + 1][y - 1] == wall_flag:
            cur_value += 0.2 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x + 1][y - 1] == trap_flag:
            cur_value += 0.2 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.2 * (cur_maze[x + 1][y - 1] + gamma * value_record[x + 1][y - 1])

    value = max(value, cur_value)
    cur_value = 0

    # right
    if y == y_size - 1:
        cur_value += 0.2 * (wall_reward + gamma * value_record[x][y])
    elif x == 0:  # 最小大于2*2
        cur_value += 0.2 * (wall_reward + gamma * value_record[x][y])

        if cur_maze[x][y + 1] == wall_flag:
            cur_value += 0.6 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x][y + 1] == trap_flag:
            cur_value += 0.6 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.6 * (cur_maze[x][y + 1] + gamma * value_record[x][y + 1])

        if cur_maze[x + 1][y + 1] == wall_flag:
            cur_value += 0.2 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x + 1][y + 1] == trap_flag:
            cur_value += 0.2 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.2 * (cur_maze[x + 1][y + 1] + gamma * value_record[x + 1][y + 1])

    elif x == x_size - 1:
        if cur_maze[x - 1][y + 1] == wall_flag:
            cur_value += 0.2 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x - 1][y + 1] == trap_flag:
            cur_value += 0.2 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.2 * (cur_maze[x - 1][y + 1] + gamma * value_record[x - 1][y + 1])

        if cur_maze[x][y + 1] == wall_flag:
            cur_value += 0.6 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x][y + 1] == trap_flag:
            cur_value += 0.6 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.6 * (cur_maze[x][y + 1] + gamma * value_record[x][y + 1])

        cur_value += 0.2 * (wall_reward + gamma * value_record[x][y])

    else:
        if cur_maze[x - 1][y + 1] == wall_flag:
            cur_value += 0.2 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x - 1][y + 1] == trap_flag:
            cur_value += 0.2 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.2 * (cur_maze[x - 1][y + 1] + gamma * value_record[x - 1][y + 1])

        if cur_maze[x][y + 1] == wall_flag:
            cur_value += 0.6 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x][y + 1] == trap_flag:
            cur_value += 0.6 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.6 * (cur_maze[x][y + 1] + gamma * value_record[x][y + 1])

        if cur_maze[x + 1][y + 1] == wall_flag:
            cur_value += 0.2 * (wall_reward + gamma * value_record[x][y])
        elif cur_maze[x + 1][y + 1] == trap_flag:
            cur_value += 0.2 * (trap_reward + gamma * value_record[0][0])
        else:
            cur_value += 0.2 * (cur_maze[x + 1][y + 1] + gamma * value_record[x + 1][y + 1])
    return max(value, cur_value)


def find_way_M(cur_maze, value_record):
    cur_x, cur_y = 0, 0
    total_record = cur_maze + value_record
    step = 0
    max_step = 50000
    while True:
        choice = choose_direction_M(total_record, cur_x, cur_y)
        cur_x, cur_y, flag = move(cur_maze, cur_x, cur_y, choice)
        if flag:
            return step
        step += 1
        if step >= max_step:
            return 1000


def move(cur_maze, x, y, direction):
    x_back, y_back = x, y

    tmp = random.random()
    if tmp < 0.6:
        offset = 0
    elif tmp < 0.8:
        offset = -1
    else:
        offset = 1

    if direction == 0:
        x -= 1
        y += offset
    elif direction == 1:
        x += 1
        y += offset
    elif direction == 2:
        x += offset
        y -= 1
    else:
        x += offset
        y += 1
    x_size, y_size = len(cur_maze), len(cur_maze[0])
    if (x < 0 or x >= x_size) or (y < 0 or y >= y_size) or cur_maze[x][y] == wall_flag:
        return x_back, y_back, False
    if cur_maze[x][y] == trap_flag:
        return 0, 0, False
    if cur_maze[x][y] == final_flag:
        return x, y, True
    return x, y, False


def choose_direction_M(total_record, x, y):
    x_size = len(total_record)
    y_size = len(total_record[0])
    v = [-1, -1, -1, -1, -1, -1, -1, -1]
    if x > 0:
        v[1] = get_reward(total_record[x-1][y])
        if y > 0:
            v[0] = get_reward(total_record[x-1][y-1])
        if y < y_size-1:
            v[2] = get_reward(total_record[x-1][y+1])
    if x < x_size - 1:
        v[6] = get_reward(total_record[x+1][y])
        if y > 0:
            v[5] = get_reward(total_record[x+1][y-1])
        if y < y_size-1:
            v[7] = get_reward(total_record[x+1][y+1])
    if y > 0:
        v[3] = get_reward(total_record[x][y-1])
    if y < y_size - 1:
        v[4] = get_reward(total_record[x][y+1])

    d = get_direction_value(v)
    return direction_policy(d)


def direction_policy(d):
    max_queue = [0]
    max_value = d[0]
    k = 1
    while k < 4:
        if max_value < d[k]:
            max_value = d[k]
            max_queue.clear()
            max_queue.append(k)
        elif max_value == d[k]:
            max_queue.append(k)
        k += 1
    ran = random.randint(0, len(max_queue) - 1)
    policy = max_queue[ran]  # 贪心策略
    is_greedy = random.random() < epsilon
    if not is_greedy:
        tmp = [0, 1, 2, 3]
        tmp.pop(policy)
        policy = tmp[random.randint(0, 2)]
    return policy


def get_direction_value(v):
    d = [0.2*v[0] + 0.6*v[1] + 0.2*v[2],
         0.2*v[5] + 0.6*v[6] + 0.2*v[7],
         0.2*v[0] + 0.6*v[3] + 0.2*v[5],
         0.2*v[2] + 0.6*v[4] + 0.2*v[7]]
    return d


def get_reward(flag):
    if flag == wall_flag:
        return wall_reward
    if flag == trap_reward:
        return trap_reward
    return flag


def a_test():
    gen_maze()
    with open('input.txt', 'r') as f:
        text = f.read()
        my_maze = json.loads(text)

    array = create_Mtable(my_maze)
    x_axis = range(100)
    y_axis = []
    for i in range(100):
        n = 0
        for j in range(10):
            n += find_way_M(my_maze, array)
        y_axis.append(n / 10)
        array = iteration_M(my_maze, array)

    plt.plot(x_axis, y_axis)
    for xp, yp in zip(x_axis, y_axis):
        if yp < 25:
            plt.text(xp, yp, yp, ha='center', va='bottom', fontsize=10)
    plt.show()


if __name__ == "__main__":
    a_test()

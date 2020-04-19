import numpy as np
import pandas as pd


class RL(object):
    def __init__(self, action_space, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9):
        self.actions = action_space
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy

        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            self.q_table = self.q_table.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )

    def choose_action(self, observation):
        self.check_state_exist(observation)
        if np.random.uniform() < self.epsilon:
            state_action = self.q_table.loc[observation, :]
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        else:
            action = np.random.choice(self.actions)
        return action

    def learn(self, *args):
        pass


class SarsaTable(RL):

    def __init__(self, actions, learning_rate=0.1 , reward_decay=1, e_greedy=0.99):
        super(SarsaTable, self).__init__(actions, learning_rate, reward_decay, e_greedy)

    def learn(self, s, a, r, s_, a_):
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        if s_ != 'terminal':
            q_target = r + self.gamma * self.q_table.loc[s_, a_]
        else:
            q_target = r
        self.q_table.loc[s, a] += self.lr * (q_target - q_predict)


class SarsaLamdaTable(RL):

    def __init__(self, actions, learning_rate=0.1, reward_decay=1, e_greedy=0.99, lambda_=0.9):
        super(SarsaLamdaTable, self).__init__(actions, learning_rate, reward_decay, e_greedy)

        self.lambda_ = lambda_
        self.eligibility_trace = self.q_table.copy()

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            appender = pd.Series(
                    [0]*len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            self.q_table = self.q_table.append(appender)

            self.eligibility_trace = self.eligibility_trace.append(appender)

    def learn(self, s, a, r, s_, a_):
        self.check_state_exist(s_)

        qpredict = self.q_table.loc[s, a]
        if s_ != 'terminal':
            qtarget = r + self.gamma * self.q_table.loc[s_, a_]
        else:
            qtarget = r
        error = qtarget - qpredict

        self.eligibility_trace.loc[s, :] *= 0
        self.eligibility_trace.loc[s, a] = 1

        self.q_table += self.lr * error * self.eligibility_trace

        self.eligibility_trace *= self.gamma * self.lambda_


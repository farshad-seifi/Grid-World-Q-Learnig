import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Initializing the board with the height, width, win location, lose location, and block location.
Row = 3
Column = 4
Win_Status = (2, 3)
Lose_Status = (1, 3)
Block_Status = (1, 1)
Start_Status = (0, 0)


class State:

    def __init__(self, state=Start_Status):

        self.board = np.zeros([Row, Column])
        self.isEnd = False
        self.state = state


    def GiveReward(self):
        """
        Calculating the reward of status
        :return: +1 for reaching win location and -1 for reaching lose location
        """
        if self.state == Win_Status:
            return 1
        elif self.state == Lose_Status:
            return -1
        else:
            return 0

    def IsEndChecker(self):
        """
        Check for possible end of the game
        :return: True when the agent reach any of win or lose positions
        """

        if (self.state == Win_Status or self.state == Lose_Status):
            self.isEnd = True

    def NextPosition(self, action):
        """
        Determine the next position of the agent based on the current position and the selected action
        :param action: Selected action by the agent
        :return: Next position
        """

        # nextStatus = self.state

        if action == "up":
            nextStatus = (self.state[0] + 1, self.state[1])
        elif action == "down":
            nextStatus = (self.state[0] - 1, self.state[1])
        elif action == "right":
            nextStatus = (self.state[0], self.state[1] + 1)
        else:
            nextStatus = (self.state[0], self.state[1] - 1)


        # Check the validity of the next position based on the boarder and block location

        if (nextStatus[0] >=0 and nextStatus[0] <=Row-1):
            if(nextStatus[1] >=0 and nextStatus[1] <= Column-1):
                if (nextStatus != Block_Status):

                    return nextStatus

        return self.state


class Agent:

    def __init__(self):
        """
        Set of initial parameter like epsilon(for epsilon greedy parameter) and learning rate(for updating Q values)
        """
        self.states = []
        self.actions = ["up", "down", "right", "left"]
        self.State = State()
        self.epsilon = 0.3
        self.lr = 0.2
        self.state_values = np.zeros((Row, Column))


    def ChooseAction(self):
        """
        Function for selecting next action based on current state
        :return: Next action
        """

        max_reward = 0
        action = ""

        # This part is in charge of selecting an action randomly or based on greedy policy
        if np.random.random() < self.epsilon:
            action = np.random.choice(self.actions)
        else:
            # Shuffling helps us to avoid doing repeated actions in first steps where all the states have zero value
            np.random.shuffle(self.actions)
            for a in self.actions:
                next_reward = self.state_values[self.State.NextPosition(a)[0]][self.State.NextPosition(a)[1]]

                if next_reward >= max_reward:
                    max_reward = next_reward
                    action = a

        return action

    def TakeAction(self, action):
        """
        :param action: Selected action in the ChooseAction function
        :return: Updated state
        """
        position = self.State.NextPosition(action)
        return State(state = position)

    def Reset(self):
        """
        Restarting the game states
        :return: Restarted states
        """
        self.states = []
        self.State = State()


    def Play(self, round = 10):

        for i in range(0, round):
            # Calculating the final reward for the final states
            if self.State.isEnd:
                reward = self.State.GiveReward()
                self.state_values[self.State.state[0]][self.State.state[1]] = reward
                print("Game End Reward", reward)
                print("Iteration:" , i)

                # Updating State Values for non-final states
                for s in reversed(self.states):
                    reward = self.state_values[s[0]][s[1]] + self.lr * (reward - self.state_values[s[0]][s[1]])
                    self.state_values[s[0]][s[1]] = reward

                self.Reset()

            else:
                action = self.ChooseAction()
                self.states.append(self.State.NextPosition(action))
                print("current position {} action {}".format(self.State.state, action))
                self.State = self.TakeAction(action)
                self.State.IsEndChecker()
                print("nxt state", self.State.state)
                print("Iteration:" , i)
                print("---------------------")



if __name__ == "__main__":
    ag = Agent()
    ag.Play(5000)


# Drawing Q Values
ax = sns.heatmap(ag.state_values, linewidths=0.5, annot=True, cmap = "viridis" , fmt = '0.3f')
plt.rcParams['font.family'] = 'DeJavu Serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.title("Q value table")
plt.show()

from learner import Learner
import numpy as np

class QLearner(Learner):
    """q learning algorithm"""
    def __init__(self, actions: list, epsilon_length: int, test_mode=False, **kwargs) -> None:
        super().__init__(actions, epsilon_length, test_mode, **kwargs)
        
        self.lr = float(kwargs["lr"])
        self.gamma = float(kwargs["gamma"])
        
        self.qvalues = dict()
        
        self.qvalues_updatedtimes = dict()
    
    def predict(self, state, **kwargs):
        if (self.get_epsilon() and not self.test_mode): # random action
            return self.actions[np.random.randint(0, self.n_actions)]
        else:
            state = tuple(state)
            
            if state in self.qvalues.keys():
                return self.actions[np.argmax(self.qvalues[state])]
            else:
                self.qvalues[state] = self.__get_random_array()

                return self.actions[np.random.randint(0, self.n_actions)]
        
    def learn(self, state, action_index, next_state, reward, **kwargs):
        state = tuple(state)
        new_state = tuple(next_state)
        action_index = self.actions.index(action_index)

        if not state in self.qvalues.keys():
            self.qvalues[state] = self.__get_random_array()
            
        if not new_state in self.qvalues.keys():
            self.qvalues[new_state] = self.__get_random_array()
        
        self.qvalues[state][action_index] = self.qvalues[state][action_index] \
            + (self.lr * (reward + (self.gamma * np.max(self.qvalues[new_state])) - self.qvalues[state][action_index]))
        
        self.qvalues_updatedtimes[state] = self.qvalues_updatedtimes.get(state, 0) + 1
    
    def __get_random_array(self):
        return np.random.normal(loc=0, scale=.1, size=(self.n_actions,)).astype('float32')

    def print_learn_summary(self):
        print("all seen Q values length: ", len(self.qvalues))
        print("q values updated stddev: ", np.std(list(self.qvalues_updatedtimes.values()), axis=0))
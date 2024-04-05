import numpy as np 
from sklearn.tree import DecisionTreeRegressor
from sklearn.exceptions import NotFittedError 
from collections import deque
from learner import Learner
import random

class DecisionTreeLearner(Learner):
    """this is q learning algorithm that uses Decision Tree instead of saving evert q values for each state"""
    def __init__(self, actions: list, epsilon_length: int, test_mode=False, **kwargs) -> None:
        super().__init__(actions, epsilon_length, test_mode, **kwargs)
        
        self.forest = DecisionTreeRegressor(
                                            criterion="squared_error",
                                            min_samples_split=2,
                                            min_samples_leaf=1,
                                            splitter="best"
                                            )
        self.gamma = kwargs["gamma"]
        self.batch_size = kwargs["batch_size"]
        self.memory = deque(maxlen=kwargs["memory_size"])
        self.longtrain_after = kwargs["longtrain_after"]
        
        self.epochs = 0
        self.trains = 0
        self.random_preds = 0
        self.true_preds = 0
        
    def predict(self, state, **kwargs):
        if (self.get_epsilon()) and (not self.test_mode):
            self.random_preds += 1
            return self.actions[np.random.randint(0, self.n_actions)]
        else:
            self.true_preds += 1
            state = list(state)
            return self.__get_best_action(state)
    
    def learn(self, state, action, next_state, reward, **kwargs):
        self.epochs += 1
        action_index = self.actions.index(action)
        
        state = tuple(state)
        next_state = tuple(next_state)
        
        self.memory.append((state, action_index, next_state, reward))
        
        if (self.epochs%self.longtrain_after == 0):
            self.trains += 1
            self.epochs = 0
            
            if (len(self.memory) > self.batch_size):
                states, actions, next_states, rewards = zip(*random.sample(list(self.memory), self.batch_size))
            else:
                states, actions, next_states, rewards = zip(*list(self.memory))
            
            s = []
            r = []
            for i in range(len(states)):
                s.append(states[i]+(actions[i],))
                next_action_index = self.actions.index(self.__get_best_action(list(next_states[i])))
                next_q_value = self.__get_qvalues(list(next_states[i]))[next_action_index]
                
                r.append(rewards[i] + self.gamma * next_q_value)
            self.forest.fit(s, r)
            
    def print_learn_summary(self):
        print("trains: ",self.trains)
        print("rands: ",self.random_preds)
        print("true: ",self.true_preds)
    
    def __get_best_action(self, state:list):
        q_values = self.__get_qvalues(state)
        action = self.actions[np.argmax(q_values)]
        return action
    
    def __get_qvalues(self, state:list):
        q_values = []
        s = []
        for i in range(self.n_actions):
            g = state.copy()
            g.append(i)
            s.append(g)
        try:
            q_values = self.forest.predict(s).tolist()
        except NotFittedError:
            q_values = [0 for i in range(len(self.actions))]
        
        return q_values
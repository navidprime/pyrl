import numpy as np
import pickle

class QLearning:
    def __init__(self, n_actions:int, lr:float=0.1, gamma:float=.99, epsilon_length:int=200) -> None:
        self.n_actions = n_actions
        self.lr = lr
        self.gamma = gamma
        self.epsilon_length = epsilon_length
        
        self.__epsilon = 0
        self.__test_mode = False
        
        self.__q_values = dict()
    
    def __get_random_array(self):
        return np.random.normal(loc=0, scale=.1, size=(self.n_actions,)).astype('float32')
    
    def predict(self, state):
        random_choice_proba = np.random.randint(0, self.epsilon_length)
        if (self.__epsilon < random_choice_proba) and (not self.__test_mode):
            self.__epsilon += 1
            return np.random.randint(0, self.n_actions)
        else:
            state = tuple(state)
            
            if state in self.__q_values.keys():
                return np.argmax(self.__q_values[state])
            else:
                self.__q_values[state] = self.__get_random_array()

                return np.random.randint(0, self.n_actions)
    
    def learn(self, state, action, new_state, reward):
        state = tuple(state)
        new_state = tuple(new_state)
        
        if not state in self.__q_values.keys():
            self.__q_values[state] = self.__get_random_array()
            
        if not new_state in self.__q_values.keys():
            self.__q_values[new_state] = self.__get_random_array()
        self.__q_values[state][action] = self.__q_values[state][action] \
            + (self.lr * (reward + (self.gamma * np.max(self.__q_values[new_state])) - self.__q_values[state][action]))
    
    def exit_train_mode(self):
        self.__test_mode = True
    
    def enter_train_mode(self):
        self.__test_mode = False

    def save_q(self, filename):
        """file name should end in .pkl"""
        with open(filename, 'wb') as f:
            if not all(isinstance(key, tuple) and isinstance(value, np.ndarray) for key, value in self.__q_values.items()):
                raise ValueError("Dictionary must have tuple keys and numpy.ndarray values.")
            pickle.dump(self.__q_values, f)
    
    def load_q(self, filename):
        """file name should end in .pkl"""
        try:
            with open(filename, 'rb') as f:
                self.__q_values = pickle.load(f)
        except (IOError, pickle.UnpicklingError) as e:
            print(f"Error loading data from '{filename}': {e}")

import random

class Learner:
    """this is the base class for every rl algorithm"""
    def __init__(self,
                 actions:list,
                 epsilon_length:int,
                 test_mode=False,
                 **kwargs) -> None:
        self.actions = actions
        self.epsilon_length = epsilon_length
        self.test_mode = test_mode
        
        self.n_actions = len(actions)
        
        self.epsilon = 0
    
    def predict(self, state, **kwargs):
        """choose the action from self.actions and return it. returned action is member of the self.actions"""
        pass
    
    def learn(self, state, action, next_state, reward, **kwargs):
        """update the internal policy """
        pass
    
    def print_learn_summary(self):
        """anything that should be shown after learning process"""
        pass
    
    def get_epsilon(self) -> bool:
        """exploration and exploitation"""
        rand = random.randint(0, self.epsilon_length-1)
        if (rand > self.epsilon):
            self.epsilon += 1
            return True
        return False

if __name__ == "__main__":
    l = Learner([],100)
    
    for i in range(200):
        print(l.get_epsilon()) # works fine
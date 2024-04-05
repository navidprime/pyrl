import math

class Status(enumerate):
    Win = 0,
    Lose = 1,
    Nothing = 2

class Move(enumerate):
    Left = 0,
    Right = 1,
    Up = 2,
    Down = 3

class SimpleGame:
    """this is a simple game to test the rl algorithms.
        objective of the game is that the player should avoid obstacles(lose_positions) and should reach one of the $ (win_positions)"""
    def __init__(self) -> None:
        self.pos = (0,0)
        self.lose_positions = [(1,1),(1,0),(0,1),(1,2),(2,1),(-1,-1),(-2,0), (-2,-2), (0,-3), (-2,2), (-1, 3), (2, -2), (1, -2)]
        self.win_positions = [(2,2), (4,3), (-2, -1), (-2,3), (2, -3), (-4,-3)]
        self.awake_for = 0
    
    def move(self, move: Move) -> tuple[tuple[int,int],tuple[int,int],Status]: # prev,current
        prev_pos = self.pos
        status = Status.Nothing

        if (move == Move.Left):
            self.pos = (self.pos[0],self.pos[1]-1)
        elif (move == Move.Right):
            self.pos = (self.pos[0],self.pos[1]+1)
        elif (move == Move.Up):
            self.pos = (self.pos[0]-1,self.pos[1])
        elif (move == Move.Down):
            self.pos = (self.pos[0]+1,self.pos[1])

        if (self.pos[0]**2+self.pos[1]**2 > 30 or self.awake_for > 20):
            status = Status.Lose
        elif(self.pos in self.win_positions):
            status = Status.Win
        elif (self.pos in self.lose_positions):
            status = Status.Lose
        
        if (status == Status.Lose or status == Status.Win):
            self.pos = (0,0)
            self.awake_for = 0
        else:
            self.awake_for += 1
        
        return (prev_pos, self.pos, status)
    
    def show_map(self) -> None:
        for i in range(-5,5):
            for j in range(-5,5):
                c = "*"
                if ( (i,j) in self.win_positions):
                    c = "$"
                elif ( (i,j) in self.lose_positions):
                    c = "&"
                elif ( (i,j) == self.pos):
                    c = "O"
                print(c+" ",end="")
            print()
class State:
    def __init__(self, grid : list[[str]]):
        self.grid : list[[str]] = grid    #[5x5] of strings (ex: aP9)
        self.children : list[State] = []  #potential states or plays
        self.heuristic : int = 0          #heuristic value extracted from a heuristic function



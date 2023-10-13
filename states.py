from unit import Player

class States:
    def __init__(self, current_state : list[[str]], belongs_to : Player):
        self.current_state : list[[str]] = current_state    #[5x5] of strings that is technically a grid (ex: aP9)
        self.belongs_to = belongs_to                        #Player.Attacker or Player.Defender
        self.children : list[States] = []                   #potential states or plays
        self.heuristic : int = 0                            #heuristic value extracted from a heuristic function

    #implement function that creates all possible states by the rules:
    def populate_potential_states(self):
        pass



from state import State


class AI:
    def __init__(self, game):
        self.game = game
        self.belongs_to = None              #attacker or defender
        self.algorithm = None               #alpha beta or minimax (could be a string : "a_b")
        self.heuristic_choice = None        #heurisitc function choice (could also be a string : "e0")
        self.current_state : State = None   #starting state


    #implement heuristics functions here: e0, e1, e2

    #implement ai algorithms here : minimax and alphabeta

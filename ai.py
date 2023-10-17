from state import State
from unit import Player


class AI:
    def __init__(self, game, belongs_to : Player, algorithm : bool, heuristic_choice : str):
        self.game = game
        self.belongs_to = belongs_to                    #Player.Attacker or Player.Defender
        self.algorithm = algorithm                      #if false , alpha_beta else, minimax
        self.heuristic_choice = heuristic_choice        #heurisitc function choice (could also be a string : "e0")
        self.current_state : State = None
        #starting state (can be set later)

    #implement heuristics functions here: e0, e1, e2
        #every function should go through every state in the "tree" and give it a heuristic value

    #implement ai algorithms here : minimax and alphabeta
        # given the tree of states with heuristic values calculated, choose the best move to do


    #def e0(self, ):

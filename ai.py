from state import State
from unit import Player


class AI:
    def __init__(self, game, belongs_to: Player, algorithm: bool, heuristic_choice: str):
        self.game = game
        self.belongs_to = belongs_to  # Player.Attacker or Player.Defender
        self.algorithm = algorithm  # if false , alpha_beta else, minimax
        self.heuristic_choice = heuristic_choice  # heurisitc function choice (could also be a string : "e0")
        self.current_state: State = None
        # starting state (can be set later)

    # implement heuristics functions here: e0, e1, e2
    # every function should go through every state in the "tree" and give it a heuristic value

    # implement ai algorithms here : minimax and alphabeta
    # given the tree of states with heuristic values calculated, choose the best move to do

    def e0_minimax(self, game_state, depth, max_player, starting_depth):

        if depth == 0 or self.is_game_over_from_state(game_state): #checking if the game is over or reached max depth
            return self.calculate_e0(game_state)

        if max_player:
            max_eval = (float('-inf'), None)
            best_move = None

           # for child in game_state.get_children():





    def calculate_e0(self, game_state):

        heuristic_value = 0
        d_a = d_p = d_t = d_f = d_v = 0
        a_a = a_p = a_t = a_f = a_v = 0

        for row in game_state.current_state:
            for pos in row:  # pos = position
                if pos[0] == "d":

                    # adding the stats to the defensive unit variables
                    match pos[1]:
                        case "A":
                            d_a += 9999

                        case "P":
                            d_p += 3

                        case "T":
                            d_t += 3

                        case "F":
                            d_f += 3

                        case "V":
                            d_v += 3

                elif pos[0] == "a":

                    # adding the stats to the unit variables
                    match pos[1]:
                        case "A":
                            a_a += 9999

                        case "P":
                            a_p += 3

                        case "V":
                            a_v += 3

                        case "F":
                            a_f += 3

                        case "T":
                            a_t += 3

        if self.belongs_to == Player.ATTACKER:
            heuristic_value = (a_a + a_p + a_v + a_f + a_t) - (d_a + d_p + d_v + d_f + d_t)

        else:
            heuristic_value = (d_a + d_p + d_v + d_f + d_t) - (a_a + a_p + a_v + a_f + a_t)

            return heuristic_value

    def is_game_over_from_state(self, game_state):

        for row in game_state.current_state:
            for pos in row:  # pos = position
                if pos[0] == "d" or pos[0] == "a":
                    if pos[1] == "A":
                        return False

        return True

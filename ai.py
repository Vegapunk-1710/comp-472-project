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

    def minimax(self, game_state, depth, max_player, starting_depth, rounds_left):

        if depth == 0 or self.is_game_over_from_state(game_state,
                                                      rounds_left):  # checking if the game is over or reached max depth

            return self.calculate_heuristic(game_state), game_state

        if max_player:
            max_eval = (float('-inf'), None)

            for child in game_state.children:
                current_eval, state = self.minimax(child, depth - 1, False, starting_depth, rounds_left - 1)

                if current_eval > max_eval[0]:
                    max_eval = (current_eval, child if depth == starting_depth else None)

            return max_eval

        else:
            min_eval = (float("inf"), None)

            for child in game_state.children:
                current_eval, state = self.minimax(child, depth - 1, True, starting_depth, rounds_left - 1)

                if current_eval < min_eval[0]:
                    # Starting depth - 1 because we want to get the state
                    # Right below the current state
                    min_eval = (current_eval, child if depth == starting_depth else None)

            return min_eval

    def alpha_beta(self, game_state, depth, alpha, beta, max_player, starting_depth, rounds_left):

        if depth == 0 or self.is_game_over_from_state(game_state,
                                                      rounds_left):  # checking if the game is over or reached max depth
            return self.calculate_heuristic(game_state), game_state

        if max_player:
            max_eval = (float('-inf'), None)

            for child in game_state.children:
                current_eval, state = self.alpha_beta(child, depth - 1, alpha, beta, False, starting_depth, rounds_left)

                if current_eval > max_eval[0]:
                    max_eval = (current_eval, child if depth == starting_depth else None)

                alpha = max(alpha, current_eval)
                if beta <= alpha:
                    break

            return max_eval

        else:
            min_eval = (float("inf"), None)

            for child in game_state.children:
                current_eval, state = self.alpha_beta(child, depth - 1, alpha, beta, True, starting_depth, rounds_left)

                if current_eval < min_eval[0]:
                    # Starting depth - 1 because we want to get the state
                    # Right below the current state
                    min_eval = (current_eval, child if depth == starting_depth else None)
                beta = min(beta, current_eval)
                if beta <= alpha:
                    break
            return min_eval

    def calculate_heuristic(self, game_state):

        match self.heuristic_choice:
            case "e0":
                return self.calculate_e0(game_state)
            case "e1":
                return self.calculate_e1(game_state)

            case "e2":
                return self.calculate_e2(game_state)

    def calculate_e0(self, game_state):

        heuristic_value = 0
        d_a = d_p = d_t = d_f = d_v = 0
        a_a = a_p = a_t = a_f = a_v = 0

        for row in game_state.current_state:
            for pos in row:  # pos = position
                if len(pos) != 0:
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

        if self.belongs_to == Player.ATTACKER:
            heuristic_value = (a_a + a_p + a_v + a_f + a_t) - (d_a + d_p + d_v + d_f + d_t)

        else:
            heuristic_value = (d_a + d_p + d_v + d_f + d_t) - (a_a + a_p + a_v + a_f + a_t)

        return heuristic_value

    # Strategy that is more attack oriented
    def calculate_e1(self, game_state):
        heuristic_value = 0
        d_a = d_p = d_t = d_f = d_v = 0
        a_a = a_p = a_t = a_f = a_v = 0

        for row in game_state.current_state:
            for pos in row:  # pos = position
                if pos != "" and pos[0] == "d":
                    # adding the stats to the defensive unit variables
                    match pos[1]:
                        case "A":
                            d_a += 100

                        case "P":
                            d_p += 20

                        case "T":
                            d_t += 15

                        case "F":
                            d_f += 10

                elif pos != "" and pos[0] == "a":
                    # adding the stats to the unit variables
                    match pos[1]:
                        case "A":
                            a_a += 100

                        case "P":
                            a_p += 20

                        case "V":
                            a_v += 30

                        case "F":
                            a_f += 10

        if self.belongs_to == Player.ATTACKER:
            heuristic_value = (a_a + a_p + a_v + a_f + a_t) - (d_a + d_p + d_v + d_f + d_t)

        else:
            heuristic_value = (d_a + d_p + d_v + d_f + d_t) - (a_a + a_p + a_v + a_f + a_t)

        return heuristic_value

    # Strategy that is more defense oriented
    def calculate_e2(self, game_state):

        heuristic_value = 0
        d_a = d_p = d_t = d_f = d_v = 0
        a_a = a_p = a_t = a_f = a_v = 0

        for row in game_state.current_state:
            for pos in row:  # pos = position
                if len(pos) != 0:
                    if pos[0] == "d":

                        # adding the stats to the defensive unit variables
                        match pos[1]:
                            case "A":
                                d_a += 100

                            case "P":
                                d_p += 15

                            case "T":
                                d_t += 30

                            case "F":
                                d_f += 20

                    elif pos[0] == "a":

                        # adding the stats to the unit variables
                        match pos[1]:
                            case "A":
                                a_a += 100

                            case "P":
                                a_p += 20

                            case "V":
                                a_v += 10

                            case "F":
                                a_f += 30

        if self.belongs_to == Player.ATTACKER:
            heuristic_value = (a_a + a_p + a_v + a_f + a_t) - (d_a + d_p + d_v + d_f + d_t)

        else:
            heuristic_value = (d_a + d_p + d_v + d_f + d_t) - (a_a + a_p + a_v + a_f + a_t)

        return heuristic_value

    # function checks_if_ai is dead
    # should probably also check if the number of rounds is done as well
    def is_game_over_from_state(self, game_state, rounds_left):
        ai_counter = 0
        if rounds_left <= 0:
            return True
        for row in game_state.current_state:
            for pos in row:  # pos = position
                if pos != "":
                    if pos[0] == "d" or pos[0] == "a":
                        if pos[1] == "A":
                            ai_counter += 1
        if ai_counter < 2:
            return True

        return False

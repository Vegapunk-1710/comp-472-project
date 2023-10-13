import copy

from unit import Player

class States:
    def __init__(self, current_state : list[[str]], belongs_to : Player):
        self.current_state : list[[str]] = current_state    #[5x5] of strings that is technically a grid (ex: aP9)
        self.belongs_to = belongs_to                        #Player.Attacker or Player.Defender
        self.children : list[States] = []                   #potential states or plays
        self.heuristic : int = 0                            #heuristic value extracted from a heuristic function

    #implement function that creates all possible states by the rules:
    def populate_potential_states(self, depth=3):
        belongs_to_char = self.belongs_to.value[0].lower()
        children = self.get_potential_states(self.current_state, belongs_to_char)

    def get_potential_states(self, current_state, belongs_to_char):
        states = []
        move_states = self.get_potential_moves(current_state, belongs_to_char)
        attack_states = self.get_potential_attacks(current_state, belongs_to_char)
        repair_states = self.get_potential_repairs(current_state, belongs_to_char)
        destruct_states = self.get_potential_destructs(current_state, belongs_to_char)
        states.extend(move_states)
        # states.extend(attack_states)
        # states.extend(repair_states)
        # states.extend(destruct_states)
        for state in states:
            self.print_state(state)
        return states

    def get_potential_moves(self, current_state, belongs_to_char):
        move_states = []
        for row in range(len(current_state)):
            for column in range(len(current_state[row])):
                if current_state[row][column] != "" and belongs_to_char in current_state[row][column]:
                    potential_moves = self.check_potential_moves(current_state, row, column)
                    applied_moves = self.apply_potential_moves(current_state, row, column, potential_moves)
                    move_states.extend(applied_moves)
        return move_states

    def check_potential_moves(self, current_state, row, column):
        belongs_to_char, type_char, health = current_state[row][column][0], current_state[row][column][1], int(current_state[row][column][2])
        up, left, down, right = None, None, None, None
        if row - 1 >= 0:
            up = [row - 1, column]
        if column - 1 >= 0:
            left = [row, column - 1]
        if row + 1 <= 4:
            down = [row + 1, column]
        if column + 1 <= 4:
            right = [row, column + 1]
        if (type_char == "A" or type_char == "F" or type_char == "P") and self.check_potential_combat(current_state, belongs_to_char, [up, left, down, right]):
            return []
        elif (type_char == "A" or type_char == "F" or type_char == "P") and belongs_to_char == "a":
            return [up, left]
        elif (type_char == "A" or type_char == "F" or type_char == "P") and belongs_to_char == "d":
            return [down, right]
        else:
            return [up, left, down, right]

    def apply_potential_moves(self, current_state, row, column, potential_moves):
        new_states = []
        for coord in potential_moves:
            if coord != None:
                new_state = copy.deepcopy(current_state)
                to_row, to_column = coord[0],coord[1]
                if new_state[to_row][to_column] == "":
                    unit = new_state[row][column]
                    new_state[to_row][to_column] = unit
                    new_state[row][column] = ""
                    new_states.append(new_state)
        return new_states


    def get_potential_attacks(self, current_state, belongs_to_char):
        pass

    def check_potential_combat(self, current_state, belongs_to_char, potential_locations):
        for coord in potential_locations:
            if coord != None:
                row, column = coord[0], coord[1]
                if  current_state[row][column] != "" and current_state[row][column][0] != belongs_to_char:
                    return True
        return False

    def get_potential_repairs(self, current_state, belongs_to_char):
        pass

    def get_potential_destructs(self, current_state, belongs_to_char):
        pass

    def print_state(self, state):
        print("=========================================")
        for row in range(len(state)):
            for column in range(len(state[row])):
                if state[row][column] == "":
                    print("_", end ="  ")
                else:
                    print(state[row][column], end="  ")
            print()
        print("=========================================")


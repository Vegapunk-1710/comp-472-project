import copy
import itertools

from unit import Player

DAMAGE_CHART = {
    "A": {
        "A": 3,
        "V": 3,
        "T": 3,
        "F": 1,
        "P": 3,
    },
    "V": {
        "A": 9,
        "V": 1,
        "T": 6,
        "F": 1,
        "P": 6,
    },
    "T": {
        "A": 1,
        "V": 6,
        "T": 1,
        "F": 1,
        "P": 1,
    },
    "F": {
        "A": 1,
        "V": 1,
        "T": 1,
        "F": 1,
        "P": 1,
    },
    "P": {
        "A": 3,
        "V": 3,
        "T": 3,
        "F": 1,
        "P": 3,
    },
}
REPAIR_CHART = {
    "A": {
        "A": 0,
        "V": 1,
        "T": 1,
        "F": 0,
        "P": 0,
    },
    "V": {
        "A": 0,
        "V": 0,
        "T": 0,
        "F": 0,
        "P": 0,
    },
    "T": {
        "A": 3,
        "V": 0,
        "T": 0,
        "F": 3,
        "P": 3,
    },
    "F": {
        "A": 0,
        "V": 0,
        "T": 0,
        "F": 0,
        "P": 0,
    },
    "P": {
        "A": 0,
        "V": 0,
        "T": 0,
        "F": 0,
        "P": 0,
    },
}
class State:
    id_iter = itertools.count()
    def __init__(self, current_state: list[[str]], belongs_to: Player, parent_id : int, to_string=""):
        self.id : int = next(State.id_iter)              # State's ID
        self.parent_id : int = parent_id                 # State's Parent's ID
        self.current_state: list[[str]] = current_state  # [5x5] of strings that is technically a grid (ex: aP9)
        self.belongs_to : Player = belongs_to            # Player.Attacker or Player.Defender (who's turn to play aka generate states to)
        self.children: list[State] = []                  # Potential states or plays
        self.heuristic: int = 0                          # Heuristic value determined with a heuristic function
        self.to_string : str = to_string                 # Description of what happened in order to create this state
        self.branches : list[int] = []

    def get_branching_factors(self, size):
        self.get_branches(self.children, len(self.children), [0]*size, 0)

    def get_branches(self, children, branching_factor, branches, depth):
        branches[depth] = branching_factor
        if children[0].children != []:
            self.get_branches(children[0].children, len(children[0].children)*branching_factor,branches, depth+1)
        else:
            self.branches = branches
            return

    def populate_potential_states(self, depth=3):
        belongs_to_char = self.belongs_to.value[0].lower()
        self.children = self.get_potential_states(self.current_state, belongs_to_char)
        self.populate_potential_children_states(self.children, depth - 1)
        self.get_branching_factors(depth)


    def populate_potential_children_states(self, children, depth):
        if depth == 0:
            return
        for child in children:
            belongs_to_char = child.belongs_to.value[0].lower()
            child.children = child.get_potential_states(child.current_state, belongs_to_char)
            child.populate_potential_children_states(child.children, depth - 1)


    def get_potential_states(self, current_state, belongs_to_char):
        states = []
        move_states = self.get_potential_moves(current_state, belongs_to_char)
        attack_states = self.get_potential_attacks(current_state, belongs_to_char)
        repair_states = self.get_potential_repairs(current_state, belongs_to_char)
        destruct_states = self.get_potential_destructs(current_state, belongs_to_char)
        states.extend(move_states)
        states.extend(attack_states)
        states.extend(repair_states)
        states.extend(destruct_states)
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
        belongs_to_char, type_char, health = current_state[row][column][0], current_state[row][column][1], int(
            current_state[row][column][2])
        up, left, down, right = None, None, None, None
        if row - 1 >= 0:
            up = [row - 1, column]
        if column - 1 >= 0:
            left = [row, column - 1]
        if row + 1 <= 4:
            down = [row + 1, column]
        if column + 1 <= 4:
            right = [row, column + 1]
        if (type_char == "A" or type_char == "F" or type_char == "P") and self.check_potential_combat(current_state,
                                                                                                      belongs_to_char,
                                                                                                      [up, left, down,
                                                                                                       right]):
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
                to_row, to_column = coord[0], coord[1]
                if new_state[to_row][to_column] == "":
                    unit = new_state[row][column]
                    new_state[to_row][to_column] = unit
                    new_state[row][column] = ""
                    new_state = State(new_state, self.switch_state_belonging(), self.id,
                                      self.get_to_string_from_move(unit, [row, column], [to_row, to_column]))
                    new_states.append(new_state)
        return new_states

    def get_potential_attacks(self, current_state, belongs_to_char):
        attack_states = []
        for row in range(len(current_state)):
            for column in range(len(current_state[row])):
                if current_state[row][column] != "" and belongs_to_char in current_state[row][column]:
                    potential_attacks = self.check_potential_attacks(current_state, row, column)
                    applied_attacks = self.apply_potential_attacks(current_state, row, column, potential_attacks)
                    attack_states.extend(applied_attacks)
        return attack_states

    def check_potential_attacks(self, current_state, row, column):
        potential_attacks = []
        belongs_to_char, type_char, health = current_state[row][column][0], current_state[row][column][1], int(
            current_state[row][column][2])
        up, left, down, right = None, None, None, None
        if row - 1 >= 0:
            up = [row - 1, column]
            if self.check_potential_combat(current_state, belongs_to_char, [up]):
                potential_attacks.append(up)
        if column - 1 >= 0:
            left = [row, column - 1]
            if self.check_potential_combat(current_state, belongs_to_char, [left]):
                potential_attacks.append(left)
        if row + 1 <= 4:
            down = [row + 1, column]
            if self.check_potential_combat(current_state, belongs_to_char, [down]):
                potential_attacks.append(down)
        if column + 1 <= 4:
            right = [row, column + 1]
            if self.check_potential_combat(current_state, belongs_to_char, [right]):
                potential_attacks.append(right)
        return potential_attacks

    def apply_potential_attacks(self, current_state, row, column, potential_attacks):
        new_states = []
        for coord in potential_attacks:
            if coord != None:
                new_state = copy.deepcopy(current_state)
                to_row, to_column = coord[0], coord[1]
                unit = new_state[row][column]
                other_unit = new_state[to_row][to_column]
                out_damage = DAMAGE_CHART[unit[1]][other_unit[1]]
                in_damage = DAMAGE_CHART[other_unit[1]][unit[1]]
                if int(other_unit[2]) - out_damage > 0 and int(unit[2]) - in_damage > 0:
                    unit = unit.replace(unit[2],str(int(unit[2]) - in_damage))
                    other_unit = other_unit.replace(other_unit[2], str(int(other_unit[2]) - out_damage))
                if int(unit[2]) - in_damage <= 0:
                    unit = unit.replace(unit[2],"0")
                if int(other_unit[2]) - out_damage <= 0:
                    other_unit = other_unit.replace(other_unit[2],"0")
                desc = self.get_to_string_from_attack(unit, other_unit, [row, column], [to_row, to_column])
                if "0" in unit:
                    unit = ""
                if "0" in other_unit:
                    other_unit = ""
                new_state[row][column] = unit
                new_state[to_row][to_column] = other_unit
                state = State(new_state, self.switch_state_belonging(), self.id, desc)
                new_states.append(state)
        return new_states

    def check_potential_combat(self, current_state, belongs_to_char, potential_locations):
        for coord in potential_locations:
            if coord != None:
                row, column = coord[0], coord[1]
                if current_state[row][column] != "" and current_state[row][column][0] != belongs_to_char:
                    return True
        return False

    def get_potential_repairs(self, current_state, belongs_to_char):
        repair_states = []
        for row in range(len(current_state)):
            for column in range(len(current_state[row])):
                if current_state[row][column] != "" and belongs_to_char in current_state[row][column]:
                    potential_repairs = self.check_potential_repairs(current_state, row, column)
                    applied_repairs = self.apply_potential_repairs(current_state, row, column, potential_repairs)
                    repair_states.extend(applied_repairs)
        return repair_states

    def check_potential_repairs(self, current_state, row, column):
        potential_repairs = []
        belongs_to_char, type_char, health = current_state[row][column][0], current_state[row][column][1], int(
            current_state[row][column][2])
        up, left, down, right = None, None, None, None
        if row - 1 >= 0:
            up = [row - 1, column]
            if current_state[row-1][column] != "" and belongs_to_char == current_state[row-1][column][0]:
                potential_repairs.append(up)
        if column - 1 >= 0:
            left = [row, column - 1]
            if current_state[row][column-1] != "" and belongs_to_char == current_state[row][column-1][0]:
                potential_repairs.append(left)
        if row + 1 <= 4:
            down = [row + 1, column]
            if current_state[row+1][column] != "" and belongs_to_char == current_state[row+1][column][0]:
                potential_repairs.append(down)
        if column + 1 <= 4:
            right = [row, column + 1]
            if current_state[row][column+1] != "" and belongs_to_char == current_state[row][column+1][0]:
                potential_repairs.append(right)
        return potential_repairs

    def apply_potential_repairs(self, current_state, row, column, potential_repairs):
        new_states = []
        for coord in potential_repairs:
            if coord != None:
                new_state = copy.deepcopy(current_state)
                to_row, to_column = coord[0], coord[1]
                unit = new_state[row][column]
                other_unit = new_state[to_row][to_column]
                out_heal = REPAIR_CHART[unit[1]][other_unit[1]]
                if int(other_unit[2]) < 9 and out_heal > 0:
                    if int(other_unit[2]) + out_heal > 9:
                        other_unit = other_unit.replace(other_unit[2],"9")
                    else:
                        other_unit = other_unit.replace(other_unit[2],str(int(other_unit[2]) + out_heal))
                    desc = self.get_to_string_from_repair(unit, other_unit, [row, column], [to_row, to_column])
                    new_state[row][column] = unit
                    new_state[to_row][to_column] = other_unit
                    state = State(new_state, self.switch_state_belonging(), self.id, desc)
                    new_states.append(state)
        return new_states

    def get_potential_destructs(self, current_state, belongs_to_char):
        destruct_states = []
        for row in range(len(current_state)):
            for column in range(len(current_state[row])):
                if current_state[row][column] != "" and belongs_to_char in current_state[row][column]:
                    potential_destructs = self.check_potential_destructs(current_state, row, column)
                    applied_destructs = self.apply_potential_destructs(current_state, row, column, potential_destructs)
                    destruct_states.extend(applied_destructs)
        return destruct_states

    def check_potential_destructs(self, current_state, row, column):
        potential_destructs = []
        belongs_to_char, type_char, health = current_state[row][column][0], current_state[row][column][1], int(
            current_state[row][column][2])
        up, left, down, right, left_up, right_up, left_down, right_down = None, None, None, None, None, None, None, None
        if row - 1 >= 0 and current_state[row - 1][column] != "":
            up = [row - 1, column]
            potential_destructs.append(up)
        if column - 1 >= 0 and current_state[row][column - 1] != "":
            left = [row, column - 1]
            potential_destructs.append(left)
        if row + 1 <= 4 and current_state[row + 1][column] != "":
            down = [row + 1, column]
            potential_destructs.append(down)
        if column + 1 <= 4 and current_state[row][column + 1] != "":
            right = [row, column + 1]
            potential_destructs.append(right)
        if (row - 1 >= 0 and column - 1 >= 0) and current_state[row - 1][column - 1] != "":
            left_up = [row - 1, column - 1]
            potential_destructs.append(left_up)
        if (row - 1 >= 0 and column + 1 <= 4) and current_state[row - 1][column + 1] != "":
            right_up = [row - 1, column + 1]
            potential_destructs.append(right_up)
        if (row + 1 <= 4 and column - 1 >= 0)  and current_state[row + 1][column - 1] != "":
            left_down = [row + 1, column - 1]
            potential_destructs.append(left_down)
        if (row + 1 <= 4 and column + 1 <= 4) and current_state[row + 1][column + 1] != "":
            right_down = [row + 1, column + 1]
            potential_destructs.append(right_down)
        return potential_destructs

    def apply_potential_destructs(self, current_state, row, column, potential_destructs):
        new_state = copy.deepcopy(current_state)
        unit = new_state[row][column]
        if unit[1] == "A":
            return []
        for coord in potential_destructs:
            if coord != None:
                to_row, to_column = coord[0], coord[1]
                other_unit = new_state[to_row][to_column]
                if int(other_unit[2]) - 2 <= 0:
                    other_unit = other_unit.replace(other_unit[2], "0")
                else:
                    other_unit = other_unit.replace(other_unit[2], str(int(other_unit[2]) - 2))
                new_state[to_row][to_column] = other_unit
        desc = self.get_to_string_from_destruction(unit, new_state, potential_destructs, [row, column])
        for coord in potential_destructs:
            if coord != None:
                to_row, to_column = coord[0], coord[1]
                other_unit = new_state[to_row][to_column]
                if int(other_unit[2]) <= 0:
                    other_unit = ""
                    new_state[to_row][to_column] = other_unit
        unit = ""
        new_state[row][column] = unit
        state = State(new_state, self.switch_state_belonging(), self.id, desc)
        return [state]

    def switch_state_belonging(self):
        if self.belongs_to == Player.ATTACKER:
            return Player.DEFENDER
        else:
            return Player.ATTACKER

    def print_state(self, state):
        for row in range(len(state.current_state)):
            for column in range(len(state.current_state[row])):
                if state.current_state[row][column] == "":
                    print("_", end="  ")
                else:
                    print(state.current_state[row][column], end="  ")
            print()
        print("=========================================")
        print("ID : " + str(state.id))
        print("Parent ID : " + str(state.parent_id))
        print("Desc : " + state.to_string)
        print("Countering : " + state.belongs_to.value)
        print("=========================================")

    def get_to_string_from_move(self, unit_str, old_loc, new_loc):
        belongs_to_char, type_char, health = unit_str[0], unit_str[1], int(unit_str[2])
        belongs_to = self.get_belongs_to_value(belongs_to_char)
        type = self.get_type_value(type_char)
        old_loc = self.get_loc_value(old_loc)
        new_loc = self.get_loc_value(new_loc)
        return belongs_to + "'s " + type + " move from " + old_loc + " to " + new_loc + "."

    def get_to_string_from_attack(self, unit, other_unit, old_loc, new_loc):
        s = ""
        belongs_to_char, type_char, health = unit[0], unit[1], int(unit[2])
        other_belongs_to_char, other_type_char, other_health = other_unit[0], other_unit[1], int(other_unit[2])
        belongs_to = self.get_belongs_to_value(belongs_to_char)
        type = self.get_type_value(type_char)
        other_belongs_to = self.get_belongs_to_value(other_belongs_to_char)
        other_type = self.get_type_value(other_type_char)
        old_loc = self.get_loc_value(old_loc)
        new_loc = self.get_loc_value(new_loc)
        if health > 0 and other_health > 0:
            s = belongs_to + "'s " + type + " attacked " + other_belongs_to + "'s " + other_type + " ↓ " + str(other_health) + " (" + old_loc + " → " + new_loc + "). "
        else:
            if other_health <= 0:
                s += other_belongs_to + "'s " + other_type + " got killed. " + new_loc + " is now an empty space. "
            if health <= 0 :
                s += belongs_to + "'s " + type + " killed themselves by attacking. " + old_loc + " is now an empty space. "
        return s

    def get_to_string_from_repair(self, unit, other_unit, old_loc, new_loc):
        belongs_to_char, type_char, health = unit[0], unit[1], int(unit[2])
        other_belongs_to_char, other_type_char, other_health = other_unit[0], other_unit[1], int(other_unit[2])
        belongs_to = self.get_belongs_to_value(belongs_to_char)
        type = self.get_type_value(type_char)
        other_type = self.get_type_value(other_type_char)
        old_loc = self.get_loc_value(old_loc)
        new_loc = self.get_loc_value(new_loc)
        return belongs_to + "'s " + type + " repaired its " + other_type + " ↑ " + str(other_health) + " (" + old_loc + " → " + new_loc + ")."

    def get_to_string_from_destruction(self, unit, potential_state, potential_destructs, old_loc):
        belongs_to_char, type_char, health = unit[0], unit[1], int(unit[2])
        belongs_to = self.get_belongs_to_value(belongs_to_char)
        type = self.get_type_value(type_char)
        old_loc = self.get_loc_value(old_loc)
        s = belongs_to + "'s " + type + " self-destructed and hurt :"
        for destructed_loc in potential_destructs:
            to_row, to_column = destructed_loc[0], destructed_loc[1]
            other_unit = potential_state[to_row][to_column]
            other_belongs_to_char, other_type_char, other_health = other_unit[0], other_unit[1], int(other_unit[2])
            other_belongs_to = self.get_belongs_to_value(other_belongs_to_char)
            other_type = self.get_type_value(other_type_char)
            new_loc = self.get_loc_value(destructed_loc)
            s+= " " + other_belongs_to + "'s " + other_type + " ↓ " + str(other_health) + " (" + old_loc + " → " + new_loc + ")."
        return s

    def get_belongs_to_value(self, belongs_to_char):
        if belongs_to_char == "a":
            return "Attacker"
        else:
            return "Defender"

    def get_type_value(self, type_char):
        if type_char == "A":
            return "AI"
        if type_char == "P":
            return "Program"
        if type_char == "F":
            return "Firewall"
        if type_char == "T":
            return "Tech"
        if type_char == "V":
            return "Virus"

    def get_loc_value(self, loc):
        start = ord('A')
        letter = chr(start + loc[0])
        return str(str(letter) + str(loc[1]))

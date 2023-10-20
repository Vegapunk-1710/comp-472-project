from enum import Enum

from output import write_move, write_attack, write_attack_kill, write_attack_suicide, write_repair, write_self_destruct


class Type(Enum):
    AI = "AI"
    VIRUS = "Virus"
    TECH = "Tech"
    PROGRAM = "Program"
    FIREWALL = "Firewall"


class Player(Enum):
    ATTACKER = "Attacker"
    DEFENDER = "Defender"


class Unit:
    def __init__(self, health: int, type: Type, belongs_to: Player, location: [int], game):
        self.health = health
        self.type = type  # AI, Virus, Tech, Program, Firewall
        self.belongs_to = belongs_to  # Attacker or Defender
        self.location = location  # position on the grid limited to [4,4]
        self.game = game # the game's engine
        self.in_combat = False
        self.DAMAGE_CHART = {
            Type.AI.value : {
                Type.AI.value : 3,
                Type.VIRUS.value: 3,
                Type.TECH.value: 3,
                Type.FIREWALL.value: 1,
                Type.PROGRAM.value: 3,
            },
            Type.VIRUS.value: {
                Type.AI.value: 9,
                Type.VIRUS.value: 1,
                Type.TECH.value: 6,
                Type.FIREWALL.value: 1,
                Type.PROGRAM.value: 6,
            },
            Type.TECH.value: {
                Type.AI.value: 1,
                Type.VIRUS.value: 6,
                Type.TECH.value: 1,
                Type.FIREWALL.value: 1,
                Type.PROGRAM.value: 1,
            },
            Type.FIREWALL.value: {
                Type.AI.value: 1,
                Type.VIRUS.value: 1,
                Type.TECH.value: 1,
                Type.FIREWALL.value: 1,
                Type.PROGRAM.value: 1,
            },
            Type.PROGRAM.value: {
                Type.AI.value: 3,
                Type.VIRUS.value: 3,
                Type.TECH.value: 3,
                Type.FIREWALL.value: 1,
                Type.PROGRAM.value: 3,
            },
        }
        self.REPAIR_CHART = {
            Type.AI.value: {
                Type.AI.value: 0,
                Type.VIRUS.value: 1,
                Type.TECH.value: 1,
                Type.FIREWALL.value: 0,
                Type.PROGRAM.value: 0,
            },
            Type.VIRUS.value: {
                Type.AI.value: 0,
                Type.VIRUS.value: 0,
                Type.TECH.value: 0,
                Type.FIREWALL.value: 0,
                Type.PROGRAM.value: 0,
            },
            Type.TECH.value: {
                Type.AI.value: 3,
                Type.VIRUS.value: 0,
                Type.TECH.value: 0,
                Type.FIREWALL.value: 3,
                Type.PROGRAM.value: 3,
            },
            Type.FIREWALL.value: {
                Type.AI.value: 0,
                Type.VIRUS.value: 0,
                Type.TECH.value: 0,
                Type.FIREWALL.value: 0,
                Type.PROGRAM.value: 0,
            },
            Type.PROGRAM.value: {
                Type.AI.value: 0,
                Type.VIRUS.value: 0,
                Type.TECH.value: 0,
                Type.FIREWALL.value: 0,
                Type.PROGRAM.value: 0,
            },
        }

    def get_empty_locations(self, adjacents):
        self.in_combat = self.check_combat(adjacents)
        if (self.type == Type.AI or self.type == Type.FIREWALL or self.type == Type.PROGRAM) and self.in_combat:
            return []
        elif (self.type == Type.AI or self.type == Type.FIREWALL or self.type == Type.PROGRAM) and self.belongs_to == Player.ATTACKER:
            return self.get_empty_locations_by_rules(adjacents, up=True, left=True)
        elif (self.type == Type.AI or self.type == Type.FIREWALL or self.type == Type.PROGRAM) and self.belongs_to == Player.DEFENDER:
            return self.get_empty_locations_by_rules(adjacents, down=True, right=True)
        else:
            return self.get_empty_locations_by_rules(adjacents, left=True, up=True, right=True, down=True)

    def get_empty_locations_by_rules(self, adjacents, left=False, up=False, right=False, down=False):
        moves = []
        if left and isinstance(adjacents["left"], list):
            moves.append(adjacents["left"])
        if up and isinstance(adjacents["up"], list):
            moves.append(adjacents["up"])
        if right and isinstance(adjacents["right"], list):
            moves.append(adjacents["right"])
        if down and isinstance(adjacents["down"], list):
            moves.append(adjacents["down"])
        return moves

    def move(self, row_to_be_moved_to, column_to_be_moved_to):
        for highlight in self.game.controller.highlighted_moves:
            if row_to_be_moved_to == highlight[0] and column_to_be_moved_to == highlight[1]:
                old_row, old_column = self.location
                self.game.map.grid[row_to_be_moved_to][column_to_be_moved_to] = self
                self.location = [row_to_be_moved_to, column_to_be_moved_to]
                self.game.map.grid[old_row][old_column] = None
                write_move(self.game.counter, self.belongs_to.value, self.type.value, self.encode_loc([old_row, old_column]) , self.encode_loc([row_to_be_moved_to,column_to_be_moved_to]) )
                return True


    def get_attackable_units_location(self, adjacents):
        attacks = []
        self.in_combat = self.check_combat(adjacents)
        if self.in_combat:
            for key, value  in adjacents.items():
                if isinstance(value, Unit) and value.belongs_to != self.belongs_to:
                    attacks.append(value.location)
        return attacks

    def attack(self, row_to_be_attacked, column_to_be_attacked):
        for highlight in self.game.controller.highlighted_attacks:
            if row_to_be_attacked == highlight[0] and column_to_be_attacked == highlight[1]:
                other = self.game.map.grid[row_to_be_attacked][column_to_be_attacked]
                other.health -= self.DAMAGE_CHART[self.type.value][other.type.value]
                self.health -= self.DAMAGE_CHART[other.type.value][self.type.value]
                write_attack(self.game.counter, self.belongs_to.value, self.type.value, other.belongs_to.value, other.type.value, other.health, self.encode_loc(self.location), self.encode_loc(other.location))
                if other.health <= 0:
                    write_attack_kill(self.game.counter, other.belongs_to.value, other.type.value, self.encode_loc(other.location))
                    self.game.map.grid[row_to_be_attacked][column_to_be_attacked] = None
                    del other
                if self.health <= 0:
                    write_attack_suicide(self.game.counter, self.belongs_to.value, self.type.value, self.encode_loc(self.location))
                    self.game.map.grid[self.location[0]][self.location[1]] = None
                    del self
                return True

    def get_repairable_units_location(self, adjacents):
        repairs = []
        for key, value in adjacents.items():
            if isinstance(value, Unit) and value.belongs_to == self.belongs_to and self.REPAIR_CHART[self.type.value][value.type.value] != 0 and value.health < 9:
                repairs.append(value.location)
        return repairs

    def repair(self, row_to_be_repaired, column_to_be_repaired):
        for highlight in self.game.controller.highlighted_repairs:
            if row_to_be_repaired == highlight[0] and column_to_be_repaired == highlight[1]:
                other = self.game.map.grid[row_to_be_repaired][column_to_be_repaired]
                other.health += self.REPAIR_CHART[self.type.value][other.type.value]
                if other.health > 9:
                    other.health = 9
                write_repair(self.game.counter, self.belongs_to.value, self.type.value, other.type.value, other.health, self.encode_loc(self.location), self.encode_loc(other.location))
                return True

    def get_impacted_units_location_by_destruction(self, adjacents, diagonals):
        surroundings = []
        for key, value in adjacents.items():
            if isinstance(value, Unit):
                surroundings.append(value.location)
        for key, value in diagonals.items():
            if isinstance(value, Unit):
                surroundings.append(value.location)
        return surroundings

    def self_destruct(self):
        for highlight in self.game.controller.highlighted_destructions:
            other = self.game.map.grid[highlight[0]][highlight[1]]
            other.health -= 2
            self.game.map.grid[self.location[0]][self.location[1]] = None
            write_self_destruct(self.game.counter, self.belongs_to.value, self.type.value, other.belongs_to.value, other.type.value, other.health,self.encode_loc(self.location),self.encode_loc(other.location))
            if other.health <= 0:
                self.game.map.grid[highlight[0]][highlight[1]] = None
                del other
        del self
        return True

    def check_combat(self, adjacents):
        for key, value in adjacents.items():
            if isinstance(value, Unit):
                if value.belongs_to != self.belongs_to:
                    return True
        return False

    def encode_loc(self, loc):
        start = ord('A')
        letter = chr(start + loc[0])
        return str(str(letter) + str(loc[1]))

    def __str__(self):
        return str(self.belongs_to.value) + "'s " + str(self.type.value) + " @ " + self.encode_loc(self.location) + ", In Combat ? : " +str(self.in_combat)




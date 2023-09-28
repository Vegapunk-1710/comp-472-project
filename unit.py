from enum import Enum

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

    def movement(self, adjacents):
        self.in_combat = self.check_combat(adjacents)
        if (self.type == Type.AI or self.type == Type.FIREWALL or self.type == Type.PROGRAM) and self.in_combat:
            return []
        elif (self.type == Type.AI or self.type == Type.FIREWALL or self.type == Type.PROGRAM) and self.belongs_to == Player.ATTACKER:
            return self.moves(adjacents, up=True, left=True)
        elif (self.type == Type.AI or self.type == Type.FIREWALL or self.type == Type.PROGRAM) and self.belongs_to == Player.DEFENDER:
            return self.moves(adjacents, down=True, right=True)
        else:
            return self.moves(adjacents, left=True, up=True, right=True, down=True)

    def moves(self, adjacents, left=False, up=False, right=False, down=False):
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

    def move(self, row, column):
        for highlight in self.game.highlighted_moves:
            if row == highlight[0] and column == highlight[1]:
                old_row, old_column = self.location
                self.game.map.grid[row][column] = self
                self.location = [row, column]
                self.game.map.grid[old_row][old_column] = None


    def attacking(self, adjacents):
        attacks = []
        self.in_combat = self.check_combat(adjacents)
        if self.in_combat:
            for key, value  in adjacents.items():
                if isinstance(value, Unit) and value.belongs_to != self.belongs_to:
                    attacks.append(value.location)
        return attacks

    def attack(self, row, column):
        for highlight in self.game.highlighted_attacks:
            if row == highlight[0] and column == highlight[1]:
                other = self.game.map.grid[row][column]
                other.health -= self.DAMAGE_CHART[self.type.value][other.type.value]
                self.health -= self.DAMAGE_CHART[other.type.value][self.type.value]
                if other.health <= 0:
                    self.game.map.grid[row][column] = None
                    del other
                if self.health <= 0:
                    self.game.map.grid[self.location[0]][self.location[1]] = None
                    del self



    def repair(self, other):
        if self.type == Type.AI:
            pass
        elif self.type == Type.VIRUS:
            pass
        elif self.type == Type.TECH:
            pass
        elif self.type == Type.PROGRAM:
            pass
        elif self.type == Type.FIREWALL:
            pass

    def self_destruct(self):
        pass

    def check_combat(self, adjacents):
        for key, value in adjacents.items():
            if isinstance(value, Unit):
                if value.belongs_to != self.belongs_to:
                    return True
        return False

    def __str__(self):
        start = ord('A')
        letter = chr(start + self.location[0])
        location =  str(letter) + str(self.location[1] + 1)
        return str(self.belongs_to.value) + "'s " +  str(self.type.value) + " @ " + str(location) + ", In combat ? : " +str(self.in_combat)




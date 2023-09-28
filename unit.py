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

    def attack(self, other):
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




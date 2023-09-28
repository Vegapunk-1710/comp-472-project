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
    def __init__(self, health: int, type: Type, belongs_to: Player, location: [int], map):
        self.health = health
        self.type = type  # AI, Virus, Tech, Program, Firewall
        self.belongs_to = belongs_to  # Attacker or Defender
        self.location = location  # position on the grid limited to [4,4]
        self.map = map # the game's map
        self.in_combat = False

    def movement(self, adjacents):
        self.in_combat = self.check_combat(adjacents)
        if (self.type == Type.AI or self.type == Type.FIREWALL or self.type == Type.PROGRAM) and self.in_combat:
            return []
        elif (self.type == Type.AI or self.type == Type.FIREWALL or self.type == Type.PROGRAM) and self.belongs_to == Player.ATTACKER:
            return self.move(adjacents, up=True, left=True)
        elif (self.type == Type.AI or self.type == Type.FIREWALL or self.type == Type.PROGRAM) and self.belongs_to == Player.DEFENDER:
            return self.move(adjacents, down=True, right=True)
        else:
            return self.move(adjacents, left=True, up=True, right=True, down=True)

    def move(self, adjacents, left=False, up=False, right=False, down=False):
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

    def update(self):
        pass

    def __str__(self):
        return "Unit : " + str(self.type) + ", " + str(self.belongs_to) + ", " + str(self.location)




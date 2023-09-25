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
    def __init__(self, health: int, type: Type, belongs_to: Player, place: [int], grid):
        self.health = health
        self.type = type  # AI, Virus, Tech, Program, Firewall
        self.belongs_to = belongs_to  # Attacker or Defender
        self.place = place  # position on the grid limited to [4,4]
        self.grid = grid # the game's map
        self.in_combat = False

    def movement(self):
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

    def update(self):
        pass




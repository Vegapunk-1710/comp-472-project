import pygame

from settings import Settings
from unit import Player, Type, Unit


class Grid:
    def __init__(self):
        self.grid = [
            ["dA9","dT9","dF9","",""],
            ["dT9","dP9","","",""],
            ["dF9","","","","aP9"],
            ["","","","aF9","aV9"],
            ["","","aP9","aV9","aA9"],
        ]
        for row in range(len(self.grid)):
            for column in range(len(self.grid[row])):
                if self.grid[row][column] != "":
                    place = [row, column]
                    belongs_to, type, health = self.decode(self.grid[row][column])
                    self.grid[row][column] = Unit(health, type, belongs_to, place, self)
                else:
                    self.grid[row][column] = None

        for row in range(len(self.grid)):
            for column in range(len(self.grid[row])):
                if self.grid[row][column]:
                    print(self.grid[row][column].type.name, self.grid[row][column].place)

        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 12)
        text_surface = self.font.render('Some Text', True, (0, 0, 0))



    def decode(self, str):
        belongs_to = str[0]
        type = str[1]
        health = int(str[2])

        if belongs_to == "d":
            belongs_to = Player.DEFENDER
        else:
            belongs_to = Player.ATTACKER

        if type == "A":
            type = Type.AI
        elif type == "V":
            type = Type.VIRUS
        elif type == "T":
            type = Type.TECH
        elif type == "P":
            type = Type.PROGRAM
        elif type == "F":
            type = Type.FIREWALL

        return belongs_to, type, health


    def update(self, pos):
        column = pos[0] // (Settings.SQUARE_WIDTH + Settings.SQUARE_MARGIN)
        row = pos[1] // (Settings.SQUARE_HEIGHT + Settings.SQUARE_MARGIN)
        try:
            print("Click position :  ", pos, "Grid coordinates: ", row, column)
        except:
            print("Click position :  ", pos)


    def render(self, display):

        for row in range(5):
            for column in range(5):
                x =  (Settings.SQUARE_MARGIN + Settings.SQUARE_WIDTH) * column + Settings.SQUARE_MARGIN
                y = (Settings.SQUARE_MARGIN + Settings.SQUARE_HEIGHT) * row + Settings.SQUARE_MARGIN
                color = Settings.WHITE
                if self.grid[row][column] and self.grid[row][column].belongs_to == Player.ATTACKER:
                    color = Settings.RED
                elif self.grid[row][column] and self.grid[row][column].belongs_to == Player.DEFENDER:
                    color = Settings.GREEN
                pygame.draw.rect(display, color,[x,y, Settings.SQUARE_WIDTH, Settings.SQUARE_HEIGHT])
                if self.grid[row][column]:
                    name = self.font.render(self.grid[row][column].type.value, True, (0, 0, 0))
                    display.blit(name, (x+30,y+30))
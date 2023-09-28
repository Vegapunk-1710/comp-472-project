import pygame

from settings import Settings
from unit import Player, Type, Unit


class Grid:
    def __init__(self, game):
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

        self.game= game
        self.font = pygame.font.SysFont('Comic Sans MS', 16)

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

    def encode_location(self):
        pass

    def check_adjacents(self, row, column):
        adj = {}
        adj["up"], adj["left"], adj["down"], adj["right"] = None, None, None, None
        if self.grid[row][column]:
            unit = self.grid[row][column]
            if row - 1 >= 0:
                adj["up"] = self.grid[row - 1][column] if self.grid[row - 1][column] != None else [row - 1,column]
            if column - 1 >= 0:
                adj["left"] = self.grid[row][column - 1] if self.grid[row][column - 1] != None else [row,column - 1]
            if row + 1 <= len(self.grid[row]) - 1:
                adj["down"] = self.grid[row + 1][column] if self.grid[row + 1][column] != None else [row + 1,column]
            if column + 1 <= len(self.grid[row]) - 1:
                adj["right"] = self.grid[row][column + 1] if self.grid[row][column + 1] != None else [row, column + 1]
        return unit, adj


    def update(self):
        pass

    def render(self, display):
        for row in range(5):
            for column in range(5):
                x = (Settings.SQUARE_MARGIN + Settings.SQUARE_WIDTH) * column + Settings.SQUARE_MARGIN
                y = (Settings.SQUARE_MARGIN + Settings.SQUARE_HEIGHT) * row + Settings.SQUARE_MARGIN
                color = Settings.WHITE

                if self.grid[row][column] and self.grid[row][column].belongs_to == Player.ATTACKER:
                    color = Settings.RED
                elif self.grid[row][column] and self.grid[row][column].belongs_to == Player.DEFENDER:
                    color = Settings.BLUE

                for highlight in self.game.highlighted_moves:
                    if row == highlight[0] and column == highlight[1]:
                        color = Settings.GREEN

                pygame.draw.rect(display, color,[x,y, Settings.SQUARE_WIDTH, Settings.SQUARE_HEIGHT])

                if self.grid[row][column]:
                    name = self.font.render(self.grid[row][column].type.value, True, (0, 0, 0))
                    display.blit(name, (x+30,y+30))
                    health = self.font.render(str(self.grid[row][column].health), True, (0, 0, 0))
                    display.blit(health, (x + 45, y + 15))

        if self.game.is_selected:
            selection = self.font.render("Selected : " + str(self.game.selected_unit), True, (255, 255, 255))
            display.blit(selection, (500,700))
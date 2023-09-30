import pygame

from helper import decode_string_from_init_map_coordinate
from settings import Settings
from unit import Player, Type, Unit


class Grid:
    def __init__(self, game):
        self.game = game

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
                    belongs_to, type, health = decode_string_from_init_map_coordinate(self.grid[row][column])
                    self.grid[row][column] = Unit(health, type, belongs_to, place, self.game)
                else:
                    self.grid[row][column] = None

        self.font = pygame.font.SysFont('Comic Sans MS', 16)

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

    def check_diagonals(self, row, column):
        diag = {}
        diag["left_up"], diag["right_up"], diag["left_down"], diag["right_down"] = None, None, None, None
        if self.grid[row][column]:
            if row - 1 >= 0 and column - 1 >= 0:
                diag["left_up"] = self.grid[row - 1][column - 1] if self.grid[row - 1][column - 1] != None else [row - 1, column - 1]
            if row - 1 >= 0 and column + 1 <= len(self.grid[row]) - 1:
                diag["right_up"] = self.grid[row - 1][column + 1] if self.grid[row - 1][column + 1] != None else [row - 1, column + 1]
            if row + 1 <= len(self.grid[row]) - 1 and column - 1 >= 0:
                diag["left_down"] = self.grid[row + 1][column - 1] if self.grid[row + 1][column - 1] != None else [row + 1, column - 1]
            if row + 1 <= len(self.grid[row]) - 1 and column + 1 <= len(self.grid[row]) - 1:
                diag["right_down"] = self.grid[row + 1][column + 1] if self.grid[row + 1][column + 1] != None else [row + 1, column + 1]
        return diag


    def render(self, display):
        for row in range(5):
            for column in range(5):

                x = (Settings.SQUARE_MARGIN + Settings.SQUARE_WIDTH) * column + Settings.SQUARE_MARGIN
                y = (Settings.SQUARE_MARGIN + Settings.SQUARE_HEIGHT) * row + Settings.SQUARE_MARGIN

                color = self.pick_correct_square_color(row, column)

                pygame.draw.rect(display, color,[x,y, Settings.SQUARE_WIDTH, Settings.SQUARE_HEIGHT])

                if self.grid[row][column]:
                    name = self.font.render(self.grid[row][column].type.value, True, (0, 0, 0))
                    display.blit(name, (x+30,y+30))
                    if color == Settings.YELLOW:
                        self.render_units_destructed_health(row, column, x, y, display)
                    if color == Settings.PURPLE:
                        self.render_units_healed_health(row, column, x, y, display)
                    if color == Settings.ORANGE:
                        self.render_units_attacked_health(row, column, x, y, display)
                    else:
                        health = self.font.render(str(self.grid[row][column].health), True, (0, 0, 0))
                        display.blit(health, (x + 45, y + 15))

        self.render_game_related_text(display)

    def render_units_attacked_health(self, row, column, x, y, display):
        health_minus_damage = self.get_health_impact(row, column, self.game.selected_unit.DAMAGE_CHART, " - ")
        health_minus_damage = self.font.render(health_minus_damage, True, (0, 0, 0))
        display.blit(health_minus_damage, (x + 45, y + 15))

    def render_units_healed_health(self, row, column, x, y, display):
        health_plus_repair = self.get_health_impact(row, column, self.game.selected_unit.REPAIR_CHART, " + ")
        health_plus_repair = self.font.render(health_plus_repair, True, (0, 0, 0))
        display.blit(health_plus_repair, (x + 45, y + 15))

    def render_units_destructed_health(self, row, column, x, y, display):
        health_minus_damage = str(self.grid[row][column].health) + " - " + str(2)
        health_minus_damage = self.font.render(health_minus_damage, True, (0, 0, 0))
        display.blit(health_minus_damage, (x + 45, y + 15))

    def get_health_impact(self, row_impacted, column_impacted, chart, sign):
        from_type = self.game.selected_unit.type.value
        to_type = self.grid[row_impacted][column_impacted].type.value
        impact = str(chart[from_type][to_type])
        return str(self.grid[row_impacted][column_impacted].health) + sign + impact

    def render_game_related_text(self, display):
        if self.game.is_selected:
            selected_unit_text = self.font.render("Selected Unit : " + str(self.game.selected_unit), True, (255, 255, 255))
            display.blit(selected_unit_text, (500,690))
        self_destruct_text = self.font.render("Self-Destruct Next Unit : " + str(self.game.destruct_unit), True, (255, 255, 255))
        display.blit(self_destruct_text, (500,670))

    def pick_correct_square_color(self, row, column):
        color = Settings.WHITE

        if self.grid[row][column] and self.grid[row][column].belongs_to == Player.ATTACKER:
            color = Settings.RED
        elif self.grid[row][column] and self.grid[row][column].belongs_to == Player.DEFENDER:
            color = Settings.BLUE

        for highlight in self.game.highlighted_moves:
            if row == highlight[0] and column == highlight[1]:
                color = Settings.GREEN
        for highlight in self.game.highlighted_attacks:
            if row == highlight[0] and column == highlight[1]:
                color = Settings.ORANGE
        for highlight in self.game.highlighted_repairs:
            if row == highlight[0] and column == highlight[1]:
                color = Settings.PURPLE
        for highlight in self.game.highlighted_destructions:
            if row == highlight[0] and column == highlight[1]:
                color = Settings.YELLOW

        return color
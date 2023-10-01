import pygame

from helper import decode_string_from_init_map_coordinate
from output import write_init
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

        write_init(self.grid, a_b=self.game.a_b, timeout=self.game.timeout, max_turns=self.game.MAX_TURNS)

        for row in range(len(self.grid)):
            for column in range(len(self.grid[row])):
                if self.grid[row][column] != "":
                    place = [row, column]
                    belongs_to, type, health = decode_string_from_init_map_coordinate(self.grid[row][column])
                    self.grid[row][column] = Unit(health, type, belongs_to, place, self.game)
                else:
                    self.grid[row][column] = None

        self.font = pygame.font.SysFont('Comic Sans MS', 16)
        self.end_font = pygame.font.SysFont('Comic Sans MS', 32)

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

    def check_game_over(self):
        is_attacker_ai_alive = False
        is_defender_ai_alive = False
        for row in range(len(self.grid)):
            for column in range(len(self.grid[row])):
                if isinstance(self.grid[row][column], Unit):
                    if self.grid[row][column].belongs_to.value == "Attacker" and self.grid[row][column].type.value == "AI":
                        is_attacker_ai_alive = True
                    if self.grid[row][column].belongs_to.value == "Defender" and self.grid[row][column].type.value == "AI":
                        is_defender_ai_alive = True
        if not is_attacker_ai_alive:
            return True, "Defender Won!"
        elif not is_defender_ai_alive:
            return True, "Attacker Won!"
        elif self.game.counter == self.game.MAX_TURNS:
            return True, "Game Over! Defender Won By Default!"
        else :
            return False, ""


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
        end = self.end_font.render(self.game.end_message, True, (255, 255, 255))
        display.blit(end, (690, 360))
        counter = self.font.render("Round : " + str(self.game.counter+1), True, (255, 255, 255))
        display.blit(counter, (680, 10))
        turn = self.font.render("Turn : ", True, (255, 255, 255))
        display.blit(turn, (680, 30))
        if self.game.turn == 0:
            turn = self.font.render("Attacker", True, (255, 0, 0))
            display.blit(turn, (730, 30))
        else:
            turn = self.font.render("Defender", True, (0, 0, 255))
            display.blit(turn, (730, 30))

        if self.game.is_selected:
            selected_unit_text = self.font.render("Selected Unit : " + str(self.game.selected_unit), True, (255, 255, 255))
            display.blit(selected_unit_text, (500,690))
        self_destruct_text = self.font.render("Self-Destruct Next Unit ? : " + str(self.game.destruct_unit), True, (255, 255, 255))
        display.blit(self_destruct_text, (1020,690))
        d_text = self.font.render("D + 2 x Clicks : To Destruct a Unit", True, (255, 255, 255))
        display.blit(d_text, (1000, 10))
        c_text = self.font.render("C : To Cancel a Move", True,(255, 255, 255))
        display.blit(c_text, (1000, 30))
        r_text = self.font.render("R : To Restart the Game", True, (255, 255, 255))
        display.blit(r_text, (1000, 50))

        a_text = self.font.render("A", True, (255, 255, 255))
        display.blit(a_text, (660, 40))
        b_text = self.font.render("B", True, (255, 255, 255))
        display.blit(b_text, (660, 170))
        c_text = self.font.render("C", True, (255, 255, 255))
        display.blit(c_text, (660, 300))
        d_text = self.font.render("D", True, (255, 255, 255))
        display.blit(d_text, (660, 430))
        e_text = self.font.render("E", True, (255, 255, 255))
        display.blit(e_text, (660, 560))

        zero_text = self.font.render("0", True, (255, 255, 255))
        display.blit(zero_text, (60, 660))
        one_text = self.font.render("1", True, (255, 255, 255))
        display.blit(one_text, (190, 660))
        two_text = self.font.render("2", True, (255, 255, 255))
        display.blit(two_text, (320, 660))
        three_text = self.font.render("3", True, (255, 255, 255))
        display.blit(three_text, (450, 660))
        four_text = self.font.render("4", True, (255, 255, 255))
        display.blit(four_text, (580, 660))


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

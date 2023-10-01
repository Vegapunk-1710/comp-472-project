import sys
import pygame

from output import write_end
from settings import Settings
from grid import Grid

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.display = pygame.display.set_mode(Settings.WINDOW_SIZE)
        pygame.display.set_caption("Wargame 💣")
        self.clock = pygame.time.Clock()
        self.is_done = False

        self.map = Grid(self)
        self.is_selected = False
        self.selected_unit = None
        self.highlighted_moves = []
        self.highlighted_attacks = []
        self.highlighted_repairs = []
        self.highlighted_destructions = []
        self.destruct_unit = False

        self.counter = 0
        self.MAX_COUNTER = 100
        self.turn = 0
        self.end = False
        self.end_message = ""



    def run(self):
        while not self.is_done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_done = True
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.end:
                        self.handle_click()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.destruct_unit = not self.destruct_unit
                    if event.key == pygame.K_r:
                        self.restart()
                    if event.key == pygame.K_c:
                        self.cancel()

            self.display.fill(Settings.BLACK)
            self.map.render(self.display)
            self.over()

            self.clock.tick(60)
            pygame.display.flip()

        pygame.quit()

    def handle_click(self):
        pos = pygame.mouse.get_pos()
        column = pos[0] // (Settings.SQUARE_WIDTH + Settings.SQUARE_MARGIN)
        row = pos[1] // (Settings.SQUARE_HEIGHT + Settings.SQUARE_MARGIN)
        if not self.is_selected:
            self.get_unit(row, column)
        else:
            self.set_unit(row, column)

    def get_unit(self, from_row, from_column):
        try:
            if from_row <= 4 and from_column <= 4 and self.map.grid[from_row][from_column] != None:
                if (self.turn == 0 and self.map.grid[from_row][from_column].belongs_to.value == "Attacker") or (self.turn == 1 and self.map.grid[from_row][from_column].belongs_to.value == "Defender"):
                    self.selected_unit, adjacents = self.map.check_adjacents(from_row, from_column)
                    if self.destruct_unit:
                        diagonals = self.map.check_diagonals(from_row, from_column)
                        self.highlighted_destructions = self.selected_unit.get_impacted_units_location_by_destruction(adjacents, diagonals)
                    else:
                        self.highlighted_moves = self.selected_unit.get_empty_locations(adjacents)
                        self.highlighted_attacks = self.selected_unit.get_attackable_units_location(adjacents)
                        self.highlighted_repairs = self.selected_unit.get_repairable_units_location(adjacents)
                    self.is_selected = True
        except Exception as e:
            print(e)

    def set_unit(self, to_row, to_column):
        try:
            if self.destruct_unit and (self.highlighted_moves == [] and self.highlighted_attacks == [] and self.highlighted_repairs == []):
                self.selected_unit.self_destruct()
            else:
                self.selected_unit.move(to_row, to_column)
                self.selected_unit.attack(to_row, to_column)
                self.selected_unit.repair(to_row, to_column)
        except Exception as e:
            print(e)
        finally:
            self.cancel()
            self.counter += 1
            self.turn = self.counter % 2

    def restart(self):
        self.map = Grid(self)
        self.cancel()
        self.counter = 0
        self.MAX_COUNTER = 100
        self.turn = 0
        self.end = False
        self.end_message = ""

    def cancel(self):
        self.is_selected = False
        self.selected_unit = None
        self.highlighted_moves = []
        self.highlighted_attacks = []
        self.highlighted_repairs = []
        self.highlighted_destructions = []
        self.destruct_unit = False

    def over(self):
        if not self.end:
            self.end,  self.end_message = self.map.check_game_over()
            if self.end:
                write_end(self.counter, self.end_message)


Game().run()
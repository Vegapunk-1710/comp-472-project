import sys
import pygame
from settings import Settings
from grid import Grid

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.map = Grid(self)
        self.display = pygame.display.set_mode(Settings.WINDOW_SIZE)
        pygame.display.set_caption("Wargame 💣")
        self.clock = pygame.time.Clock()
        self.is_done = False

        self.is_selected = False
        self.selected_unit = None
        self.highlighted_moves = []
        self.highlighted_attacks = []
        self.highlighted_repairs = []

    def run(self):
        while not self.is_done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_done = True
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click()

            self.display.fill(Settings.BLACK)
            self.map.render(self.display)

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
                self.selected_unit, adjacents = self.map.check_adjacents(from_row, from_column)
                self.highlighted_moves = self.selected_unit.movement(adjacents)
                # self.highlighted_attacks = self.selected_unit.attack(adjacents)
                # self.highlighted_repairs = self.selected_unit.repair(adjacents)
                self.is_selected = True
        except Exception as e:
            print(e)

    def set_unit(self, to_row, to_column):
        try:
            self.selected_unit.move(to_row, to_column)
            # self.selected_unit.attack(to_row, to_column)
            # self.selected_unit.repair(to_row, to_column)
        except Exception as e:
            print(e)
        finally:
            self.is_selected = False
            self.selected_unit = None
            self.highlighted_moves = []
            self.highlighted_attacks = []
            self.highlighted_repairs = []

Game().run()
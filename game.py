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

    def update(self):
        pos = pygame.mouse.get_pos()
        column = pos[0] // (Settings.SQUARE_WIDTH + Settings.SQUARE_MARGIN)
        row = pos[1] // (Settings.SQUARE_HEIGHT + Settings.SQUARE_MARGIN)
        if not self.is_selected:
            self.get_unit(row, column)
        else:
            self.set_unit(row, column)

    def get_unit(self, row, column):
        try:
            self.selected_unit, adjacents = self.map.check_adjacents(row, column)
            self.highlighted_moves = self.selected_unit.movement(adjacents)
            self.is_selected = True
        except Exception as e:
            print(e)

    def set_unit(self, row, column):
        try:
            for highlight in self.highlighted_moves:
                if row == highlight[0] and column == highlight[1]:
                    old_row, old_column = self.selected_unit.location
                    self.map.grid[row][column] = self.selected_unit
                    self.selected_unit.location = [row, column]
                    self.map.grid[old_row][old_column] = None
        except Exception as e:
            print(e)
        finally:
            self.is_selected = False
            self.selected_unit = None
            self.highlighted_moves = []

    def run(self):
        while not self.is_done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_done = True
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.update()

            self.display.fill(Settings.BLACK)
            self.map.render(self.display)

            self.clock.tick(60)
            pygame.display.flip()

        pygame.quit()

Game().run()
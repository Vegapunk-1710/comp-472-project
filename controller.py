import pygame

from ai import AI
from settings import Settings
from states import States
from unit import Player


class Controller:
    def __init__(self, game, is_attacker_ai=False, is_defender_ai=False):
        self.game = game
        self.is_selected = False
        self.selected_unit = None
        self.highlighted_moves = []
        self.highlighted_attacks = []
        self.highlighted_repairs = []
        self.highlighted_destructions = []
        self.destruct_unit = False
        self.is_attacker_ai = is_attacker_ai
        self.is_defender_ai = is_defender_ai
        if is_attacker_ai:
            #example of an AI for the attacker
            self.attacker_ai = AI(self.game, Player.ATTACKER, self.game.a_b, "e0")
        if is_defender_ai:
            #example of an AI for the defender
            self.defender_ai = AI(self.game, Player.DEFENDER, self.game.a_b, "e1")

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
            if from_row <= 4 and from_column <= 4 and self.game.map.grid[from_row][from_column] != None:
                if (self.game.turn == 0 and self.game.map.grid[from_row][from_column].belongs_to.value == "Attacker") or (
                        self.game.turn == 1 and self.game.map.grid[from_row][from_column].belongs_to.value == "Defender"):
                    self.selected_unit, adjacents = self.game.map.check_adjacents(from_row, from_column)
                    if self.destruct_unit:
                        diagonals = self.game.map.check_diagonals(from_row, from_column)
                        self.highlighted_destructions = self.selected_unit.get_impacted_units_location_by_destruction(
                            adjacents, diagonals)
                    else:
                        self.highlighted_moves = self.selected_unit.get_empty_locations(adjacents)
                        self.highlighted_attacks = self.selected_unit.get_attackable_units_location(adjacents)
                        self.highlighted_repairs = self.selected_unit.get_repairable_units_location(adjacents)
                    self.is_selected = True
        except Exception as e:
            print(e)


    def set_unit(self, to_row, to_column):
        try:
            if self.destruct_unit and (
                    self.highlighted_moves == [] and self.highlighted_attacks == [] and self.highlighted_repairs == []):
                self.selected_unit.self_destruct()
            else:
                self.selected_unit.move(to_row, to_column)
                self.selected_unit.attack(to_row, to_column)
                self.selected_unit.repair(to_row, to_column)
        except Exception as e:
            print(e)
        finally:
            self.cancel()
            self.game.counter += 1
            self.game.turn = self.game.counter % 2

    def cancel(self):
        self.is_selected = False
        self.selected_unit = None
        self.highlighted_moves = []
        self.highlighted_attacks = []
        self.highlighted_repairs = []
        self.highlighted_destructions = []
        self.destruct_unit = False

    def handle_ai(self):
        if self.game.turn == 0 and self.is_attacker_ai:
            self.attacker_ai_play()
        else:
            self.defender_ai_play()

    def attacker_ai_play(self):
        #Get the current and potential states
        #Calculate the heuristic value for every state
        #Choose an AI algorithm and use it
        #Make the unit do the action
        try:
            current_state = self.game.map.get_state()
            state = States(current_state, Player.ATTACKER)
            state.populate_potential_states()
        except:
            pass
        finally:
            self.cancel()
            self.game.counter += 1
            self.game.turn = self.game.counter % 2
        pass

    def defender_ai_play(self):
        #Get the current and potential states
        #Calculate the heuristic value for every state
        #Choose an AI algorithm and use it
        #Make the unit do the action
        try:
            current_state = self.game.map.get_state()
            state = States(current_state, Player.DEFENDER)
            state.populate_potential_states()
        except:
            pass
        finally:
            self.cancel()
            self.game.counter += 1
            self.game.turn = self.game.counter % 2
import pygame

from ai import AI
from output import write_illegal_move
from settings import Settings
from state import State
from unit import Player


class Controller:
    def __init__(self, game, mode):
        self.game = game
        self.is_selected = False
        self.selected_unit = None
        self.highlighted_moves = []
        self.highlighted_attacks = []
        self.highlighted_repairs = []
        self.highlighted_destructions = []
        self.destruct_unit = False
        self.mode = mode
        if mode[0] != "H":
            # example of an AI for the attacker
            self.attacker_ai = AI(self.game, Player.ATTACKER, self.game.a_b, "e0")
        if mode[2] != "H":
            # example of an AI for the defender
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
                if (self.game.turn == 0 and self.game.map.grid[from_row][
                    from_column].belongs_to.value == "Attacker") or (
                        self.game.turn == 1 and self.game.map.grid[from_row][
                    from_column].belongs_to.value == "Defender"):
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
                self.cancel()
                self.game.counter += 1
                self.game.turn = self.game.counter % 2
            else:
                did_move = self.selected_unit.move(to_row, to_column)
                did_attack = self.selected_unit.attack(to_row, to_column)
                did_repair = self.selected_unit.repair(to_row, to_column)
                if did_move or did_attack or did_repair:
                    self.cancel()
                    self.game.counter += 1
                    self.game.turn = self.game.counter % 2
                else:
                    write_illegal_move(self.game.counter, self.selected_unit.belongs_to.value,
                                       self.selected_unit.type.value,
                                       self.selected_unit.encode_loc(self.selected_unit.location),
                                       self.selected_unit.encode_loc([to_row, to_column]))
                    self.game.warning = True
        except Exception as e:
            print(e)

    def cancel(self):
        self.is_selected = False
        self.selected_unit = None
        self.highlighted_moves = []
        self.highlighted_attacks = []
        self.highlighted_repairs = []
        self.highlighted_destructions = []
        self.destruct_unit = False
        self.game.warning = False

    def handle_ai(self):
        if self.game.turn == 0 and self.mode[0] == "A":
            self.attacker_ai_play()
        else:
            self.defender_ai_play()

    def attacker_ai_play(self):
        # Get the current and potential states : DONE
        # Calculate the heuristic value for every state
        # Choose an AI algorithm and use it
        # Make the unit do the action
        try:
            current_state = self.game.map.get_state()
            state = State(current_state, Player.ATTACKER, 0)
            state.populate_potential_states(depth=3)
            rounds_left = self.game.MAX_TURNS - self.game.counter + 1
            if self.game.a_b:
                value, chosen_state = self.attacker_ai.alpha_beta(state, 3, float("-inf"), float("inf"), True, 3,
                                                                  rounds_left)
            else:
                value, chosen_state = self.attacker_ai.minimax(state, 3, True, 3, rounds_left)
            print(chosen_state)
        except Exception as e:
            print(e)
        finally:
            self.cancel()
            self.game.counter += 1
            self.game.turn = self.game.counter % 2
        pass

    def defender_ai_play(self):
        # Get the current and potential states : DONE
        # Calculate the heuristic value for every state
        # Choose an AI algorithm and use it
        # Make the unit do the action
        # try:
        current_state = self.game.map.get_state()
        state = State(current_state, Player.DEFENDER, 0)
        state.populate_potential_states(depth=3)
        rounds_left = self.game.MAX_TURNS - self.game.counter + 1
        if self.game.a_b:
            value, chosen_state = self.defender_ai.alpha_beta(state, 1, float("-inf"), float("inf"), True, 1,
                                                              rounds_left)
        else:
            value, chosen_state = self.defender_ai.minimax(state, 1, True, 1, rounds_left)
        print(chosen_state)
        # except Exception as e:
        #     print(e)
        # finally:
        self.cancel()
        self.game.counter += 1
        self.game.turn = self.game.counter % 2

import sys
import pygame

from controller import Controller
from output import write_end, change_filename
from settings import Settings
from grid import Grid

class Game:
    def __init__(self, filename, a_b, timeout, max_turns):
        pygame.init()
        pygame.font.init()
        self.display = pygame.display.set_mode(Settings.WINDOW_SIZE)
        pygame.display.set_caption("Wargame 💣")
        self.clock = pygame.time.Clock()
        self.is_done = False
        change_filename(filename)

        self.mode = "H-A"
        self.a_b = a_b
        self.timeout = timeout
        self.MAX_TURNS = max_turns

        self.controller = Controller(self, self.mode)

        self.map = Grid(self)

        self.counter = 0
        self.turn = 0
        self.end = False
        self.end_message = ""
        self.warning = False

    def run(self):
        while not self.is_done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_done = True
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.end and ((self.turn == 0 and self.mode[0] == "H") or (self.turn == 1 and self.mode[2] == "H")):
                        self.controller.handle_click()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.controller.destruct_unit = not self.controller.destruct_unit
                    if event.key == pygame.K_r:
                        self.restart()
                    if event.key == pygame.K_c:
                        self.controller.cancel()

            if (self.turn == 0 and self.mode[0] != "H") or (self.turn == 1 and self.mode[2] != "H"):
                    self.controller.handle_ai()

            self.display.fill(Settings.BLACK)
            self.map.render(self.display)
            self.over()

            self.clock.tick(60)
            pygame.display.flip()

        pygame.quit()


    def restart(self):
        self.map = Grid(self)
        self.controller.cancel()
        self.counter = 0
        self.MAX_TURNS = 100
        self.turn = 0
        self.end = False
        self.end_message = ""

    def over(self):
        if not self.end:
            self.end,  self.end_message = self.map.check_game_over()
            if self.end:
                write_end(self.counter, self.end_message)


if __name__ == "__main__":
    filename, a_b, timeout, max_turns = "gameTrace", False, 0, 100
    if len(sys.argv) > 0 :
        try:
            args = str(sys.argv[1])
            args = args.replace(".txt", "")
            splits = args.split("-")
            filename = splits[0]
            a_b = eval(splits[1].capitalize())
            timeout = int(splits[2])
            max_turns = int(splits[3])
            print(filename, a_b, timeout, max_turns)
        except Exception as e:
            print(e)
    game = Game(filename, a_b, timeout, max_turns)
    game.run()
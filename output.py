FIlENAME = ""

def change_filename(filename):
    global FIlENAME
    FIlENAME = filename

def write_init(grid, timeout=0, max_turns=100, ai="None", a_b=False, play_mode="H-H", e="None"):
    write('===========================================================================================')
    write("*PARAMETERS*")
    write("Timeout in seconds : " + str(timeout))
    write("Max number of turns : " + str(max_turns))
    write("AI Player  : " + str(ai) + ", Alpha-Beta  : " + str(a_b))
    write("Play Mode  : " + str(play_mode))
    write("Name of Heuristic : " + str(e))
    write('===========================================================================================')
    write("*BOARD*")
    write_grid(grid)
    write('===========================================================================================')
    write("*GAMEPLAY*")

def write_grid(grid):
    for row in grid:
            write(str(row))

def write_move(turn, player, type, old_loc, new_loc):
    s = "Turn #" + str(turn+1) + " : " + player + "'s " + type + " move from " + old_loc + " to " + new_loc + "."
    write(s)

def write_attack(turn, player1, type1, player2, type2, player2_health, player1_loc, player2_loc):
    s = "Turn #" + str(turn + 1) + " : " + player1 + "'s " + type1 + " attacked " + player2 + "'s " + type2 + " ↓ " + str(player2_health) + " (" + player1_loc + " → " + player2_loc + ")."
    write(s)

def write_attack_kill(turn, player_killed, type_killed, killed_loc):
    s = "Turn #" + str(turn + 1) + " : " + player_killed + "'s " + type_killed + " got killed. " + killed_loc + " is now an empty space."
    write(s)

def write_attack_suicide(turn, player_killed, type_killed, killed_loc):
    s = "Turn #" + str(turn + 1) + " : " + player_killed + "'s " + type_killed + " killed themselves by attacking. " + killed_loc + " is now an empty space."
    write(s)

def write_repair(turn, player1, type1, type2, player2_health, player1_loc, player2_loc):
    s = "Turn #" + str(turn + 1) + " : " + player1 + "'s " + type1 + " repaired its " + type2 + " ↑ " + str(player2_health) + " (" + player1_loc + " → " + player2_loc + ")."
    write(s)

def write_self_destruct(turn, player1, type1, player2, type2, player2_health, player1_loc, player2_loc):
    s = "Turn #" + str(turn + 1) + " : " + player1 + "'s " + type1 + " self-destructed and hurt " + player2 + "'s " + type2 + " ↓ " + str(player2_health) + " (" + player1_loc + " → " + player2_loc + ")."
    write(s)

def write_end(turns, message):
    write('===========================================================================================')
    s = message + " The game took " + str(turns + 1) + " turns."
    write(s)
    write('===========================================================================================')

def write(s):
    with open(FIlENAME+'.txt', 'a', encoding="utf-8") as f:
        f.write(s + '\n')
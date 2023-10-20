from unit import Player, Type

def decode_string_from_init_map_coordinate(str):
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

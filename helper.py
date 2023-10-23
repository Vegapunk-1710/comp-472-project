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

def cumulative_to_strings(cumu_list):
    s1 = ""
    s2 = ""
    counter = 1
    total = 0
    for c in cumu_list:
        s1+=" " + str(counter) + "=" + str(c)
        total += c
        counter+=1

    counter = 1
    for c in cumu_list:
        s2+=" " + str(counter) + "=" + str(round((c/total)*100,2)) + "%"
        counter += 1
    return (s1,s2,get_average_branching_factor(cumu_list),str(total))

def get_average_branching_factor(cumu_list):
    total = 0
    counter = 0
    for i in range(len(cumu_list)):
        for j in range(len(cumu_list)):
            if i == j - 1:
                total += (cumu_list[j]/cumu_list[i])
                counter += 1

    return str(round( (total/counter) , 1) )

def get_ai_player_to_string(string):
    p1 = string[0]
    p2 = string[2]
    if p1 == "A" and p2 == "A":
        return "Attacker & Defender"
    if p1 == "A":
        return "Attacker"
    if p2 == "A":
        return "Defender"




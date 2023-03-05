import itertools
import math
from characters import CharacterState
from actions import AttackAbility
from menu import partmenu, abilitymenu, askforinput

def displaycharacterhealth(character1, character2, initiative):
    print("{:<39}{:^10}{:>38}".format(character1.name + ":", "initiative: " + str(initiative), ":" + character2.name))

    for (part1, part2) in itertools.zip_longest(character1.parts, character2.parts):
        if part1 is not None:
            leftline = part1[0] + ": " + str(part1[1].currenthp) + "/" + str(part1[1].maxhp)
        else:
            leftline = ""
        if part2 is not None:
            rightline = str(part2[1].currenthp) + "/" + str(part2[1].maxhp) + " :" + part2[0]
        else:
            rightline = ""
        print("{:<45}{}{:>45}".format(leftline, "", rightline))

    print("")

def defeated(character):
    match character.state:
        case CharacterState.Helpless | CharacterState.Unconscious | CharacterState.Dead:
            return True
        case CharacterState.Alive:
            return False

def playerturn(player, enemy, initiative):
    displaycharacterhealth(player, enemy, initiative)

    while True:
        print("Pick an action")
        abilitytouse = player.actions[askforinput(abilitymenu(player))]
        if isinstance(abilitytouse, AttackAbility):
            print("pick a part to use with the action")
            partindex = askforinput(partmenu(player, abilitytouse, "use"))
            if partindex < len(player.parts):
                parttouse = player.parts[partindex]
            else:
                continue

            print("pick a target for the action")
            partindex = askforinput(partmenu(enemy, abilitytouse, "target"))
            if partindex < len(enemy.parts):
                parttodmg = enemy.parts[partindex][1]
            else:
                continue

            returnvalue = ((initiative + math.ceil(abilitytouse.startup / player.speed)),
                           abilitytouse, parttouse, enemy, parttodmg)
            return returnvalue
        else:
            returnvalue = ((initiative + abilitytouse.startup), abilitytouse)
            return returnvalue

def enemyturn(enemy, player):
    print("Enemy Turn NYI")

def combatinstance(player, enemy):
    initiative = 0
    player.nextturn = math.ceil(50 / player.speed)
    enemy.nextturn = math.ceil(50 / enemy.speed)
    pendingactions = []

    while not defeated(player) and not defeated(enemy):
        if player.nextturn == initiative:
            pendingactions.append(playerturn(player, enemy, initiative))
            player.nextturn = math.ceil(initiative + (pendingactions[-1][1].recovery / player.speed))
        if enemy.nextturn == initiative:
            enemyturn(enemy, player)

        for action in list(pendingactions):
            if action[0] == initiative and isinstance(action[1], AttackAbility):
                action[1].finishattack(action[2], action[3], action[4])
                print("{:^90}".format("Initiative: " + str(action[0])))
                tempmessage = "{} executed targeting {}".format(action[1].name, action[3].name)
                print("{:^90}".format(tempmessage))
                pendingactions.remove(action)

        player.updatestate()
        enemy.updatestate()
        if defeated(player):
            print("{:^90}".format("Game Over: player defeated"))
        elif defeated(enemy):
            print("{:^90}".format("Game Over: enemy defeated"))
        initiative += 1

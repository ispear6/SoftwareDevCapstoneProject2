from actions import AttackAbility

def askforinput(options):
    while True:
        print("Type the name or number to select an option:")
        count = 1

        for option in options:
            line = "{}: {}".format(option[0], option[1])
            print("{:^15}".format(line), end="")
            count += 1

            if count > 3 or option == options[-1]:
                print("")
                count = 1

        command = str(input("")).lower()

        for option in options:
            if command in option:
                return int(option[0])
        print("\nInvalid option")


def getplayername():
    while True:
        name = input("What is your name? ")
        if name.isalpha():
            return name
        else:
            print("improper format")

def partmenu(character, ability=None, menutype=""):
    partlist = []
    if isinstance(ability, AttackAbility) and menutype == "target":
        for i, part in enumerate(character.parts):
            if part[1].parttype in ability.targets:
                partlist.append((str(i), part[0]))
    elif isinstance(ability, AttackAbility) and menutype == "use":
        for i, part in enumerate(character.parts):
            if part[1].parttype == ability.part:
                partlist.append((str(i), part[0]))
    else:
        for i, part in enumerate(character.parts):
            partlist.append((str(i), part[0]))
    partlist.append((str(len(character.parts)), "back"))
    return partlist

def abilitymenu(character):
    abilitylist = []
    for i, action in enumerate(character.actions):
        abilitylist.append((str(i), action.name))
    return abilitylist

from bodyparts import BodyPartType, BodyPart
from actions import ActionID, getaction
from enum import Enum
import math

from menu import getplayername

class CharacterState(Enum):
    Alive = 1
    Helpless = 2
    Unconscious = 3
    Dead = 4

class CreatureType(Enum):
    Human = 1

class EnemyType(Enum):
    bandit = 1
    wolf = 2

class Character:
    def __init__(self, name, creaturetype, parts, actions, level, speed):
        self.name = name
        self.creaturetype = creaturetype
        self.parts = parts
        self.actions = actions
        self.level = level
        self.speed = speed

    nextturn = 0
    state = CharacterState.Alive

    def takedamage(self, target, dmg):
        overflow = target.takedamage(dmg)
        if overflow > 0:
            healthyparts = 0

            for part in self.parts:
                if part[1].currenthp > 0:
                    healthyparts += 1
            overflowdmg = math.ceil(overflow / healthyparts)
            for part in self.parts:
                if part[1].currenthp > 0:
                    self.takedamage(part[1], overflowdmg)


    def updatestate(self):
        healthyheads = 0
        healthytorsos = 0
        healthyarms = 0
        healthylegs = 0
        for part in self.parts:
            if not part[1].isbroken:
                match part[1].parttype:
                    case BodyPartType.Head:
                        healthyheads += 1
                    case BodyPartType.Torso:
                        healthytorsos += 1
                    case BodyPartType.Arm:
                        healthyarms += 1
                    case BodyPartType.Leg:
                        healthylegs += 1

        if healthyheads == 0:
            self.state = CharacterState.Dead
        elif healthytorsos == 0:
            self.state = CharacterState.Unconscious
        else:
            match self.creaturetype:
                case CreatureType.Human:
                    if healthyarms == 0 and healthylegs == 0:
                        self.state = CharacterState.Helpless
                    elif self.state != CharacterState.Alive:
                        self.state = CharacterState.Alive

    def __addpart(self, location, parttoadd):
        if location not in self.parts:
            self.parts.append((location, parttoadd))
            self.parts.sort(key=lambda x: [x[1].parttype.value, x[0]])

    def removepart(self, location):
        for i, part in enumerate(self.parts):
            if part[0] == location:
                del self.parts[i]

    def changepart(self, location, parttoadd):
        self.removepart(location)
        self.__addpart(location, parttoadd)

def getpartvalues(creaturetype, parttype):
    match creaturetype:
        case CreatureType.Human:
            match parttype:
                case BodyPartType.Head:
                    return BodyPart("human head", BodyPartType.Head, 60, 100, 100)
                case BodyPartType.Torso:
                    return BodyPart("human torso", BodyPartType.Torso, 160, 100, 100)
                case BodyPartType.Arm:
                    return BodyPart("human arm", BodyPartType.Arm, 100, 100, 100)
                case BodyPartType.Leg:
                    return BodyPart("human leg", BodyPartType.Leg, 100, 100, 100)

def getbaselineparts(creature):
    match creature:
        case CreatureType.Human:
            return [("head", getpartvalues(CreatureType.Human, BodyPartType.Head)),
                    ("torso", getpartvalues(CreatureType.Human, BodyPartType.Torso)),
                    ("left arm", getpartvalues(CreatureType.Human, BodyPartType.Arm)),
                    ("right arm", getpartvalues(CreatureType.Human, BodyPartType.Arm)),
                    ("left leg", getpartvalues(CreatureType.Human, BodyPartType.Leg)),
                    ("right leg", getpartvalues(CreatureType.Human, BodyPartType.Leg))]


# player is persistent and should hold values long term, so it is global and referenced directly
player = Character(getplayername(),
                   CreatureType.Human,
                   getbaselineparts(CreatureType.Human),
                   [getaction(ActionID.punch),
                    getaction(ActionID.kick),
                    getaction(ActionID.wait)],
                   1,
                   10)


def banditfinal(level):
    abilities = [getaction(ActionID.punch),
                 getaction(ActionID.kick),
                 getaction(ActionID.wait)]
    name = "Elite Bandit" if level > 3 else "Bandit"

    enemy = Character(name, CreatureType.Human, getbaselineparts(CreatureType.Human), abilities, level, (10 + level))
    for part in enemy.parts:
        part[1].maxhp -= 20
        part[1].currenthp = part[1].maxhp
    return enemy

# enemies are created when needed and do not need to hold values long term, so they are created at runtime
def spawnenemy(enemytospawn, level=1):
    match enemytospawn:
        case EnemyType.bandit:
            return banditfinal(level)

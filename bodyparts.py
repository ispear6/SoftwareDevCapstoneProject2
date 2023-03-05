from enum import Enum
import math

class BodyPartType(Enum):
    Head = 1
    Torso = 2
    Arm = 3
    Leg = 4


class BodyPart:
    def __init__(self, name, parttype, maxhp, strength, toughness):
        self.name = name
        self.parttype = parttype
        self.maxhp = maxhp
        self.currenthp = maxhp
        self.strength = strength
        self.toughness = toughness
    isbroken = False
    toughnessup = 1.0
    toughnessdown = 1.0
    strengthup = 1.0
    strengthdown = 1.0

    def getfinaltoughness(self):
        return math.ceil((self.toughness * self.toughnessup) / self.toughnessdown)

    def getfinalstrength(self):
        return math.ceil((self.strength * self.strengthup) / self.strengthdown)

    def takedamage(self, dmg):
        toughnessmod = self.getfinaltoughness() / 100
        dmgapplied = math.ceil(dmg / toughnessmod)
        returnvalue = dmgapplied - self.currenthp
        self.currenthp = max(0, self.currenthp - dmgapplied)
        if self.currenthp == 0:
            self.isbroken = True
            return returnvalue
        else:
            return -1

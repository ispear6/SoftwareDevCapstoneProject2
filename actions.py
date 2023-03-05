from enum import Enum
import math
from bodyparts import BodyPartType


class ActionID(Enum):
    wait = 1
    punch = 2
    kick = 3

class Ability:
    def __init__(self, name, startup, recovery, cooldownstat):
        self.name = name
        self.startup = startup
        self.recovery = recovery
        self.cooldownstat = cooldownstat
    cooldowntime = 0
    offcooldown = True

    def incrementcooldown(self):
        self.cooldowntime = max((0, self.cooldowntime - 1))
        if self.cooldowntime == 0:
            self.offcooldown = True

    def startcooldown(self):
        self.cooldowntime = self.cooldownstat
        self.offcooldown = False


class AttackAbility(Ability):
    def __init__(self, name, startup, recovery, cooldownstat,
                 dmg, part, targets, stamcost=0):
        super().__init__(name, startup, recovery, cooldownstat)
        self.dmg = dmg
        self.stamcost = stamcost
        self.part = part
        self.targets = targets

    def finishattack(self, parttouse, targetcharacter, targetpart):
        dmg = math.ceil(self.dmg * (parttouse[1].getfinalstrength() / 100))
        targetcharacter.takedamage(targetpart, dmg)

def getaction(actionid):
    match actionid:
        case ActionID.wait:
            return Ability("wait", 0, 50, 0)
        case ActionID.punch:
            targets = [BodyPartType.Head,
                       BodyPartType.Torso,
                       BodyPartType.Arm]
            return AttackAbility("punch", 50, 80, 0, 15, BodyPartType.Arm, targets, 30)
        case ActionID.kick:
            targets = [BodyPartType.Torso,
                       BodyPartType.Leg]
            return AttackAbility("kick",  80, 140, 0, 35, BodyPartType.Leg, targets, 54)

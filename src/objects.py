"""
Weapon:     name => String,
            wprolls => WeaponRoll
WeaponRoll: type => String,
            mws => String
            barrels => String
            note => None
            rolls => List
"""


class Weapon:
    def __init__(self, name):
        self.name = name
        self.wprolls = []

    def get_name(self):
        return self.name

    def get_wprolls(self):
        return self.wprolls

    def append(self, wpr):
        self.wprolls.append(wpr)


class WeaponRoll:
    def __init__(self):
        self.type = None  # pve/pvp/...
        self.mws = None  # masterworks
        self.barrels = []  # barrels
        self.note = None  # custom note
        self.rolls = []  # list with all rolls

    # Getters

    def get_type(self):
        return self.type

    def get_mws(self):
        return self.mws

    def get_barrels(self):
        return self.barrels

    def get_note(self):
        return self.note

    def get_rolls(self):
        return self.rolls

    # Setters

    def set_type(self, new):
        self.type = new

    def set_mws(self, new):
        self.mws = new

    def set_barrels(self, new):
        self.barrels = new

    def set_note(self, new):
        self.note = new

    def app_roll(self, new):
        self.rolls.append(new)

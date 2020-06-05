import random

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk-10
        self.atkh = atk+10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]
        self.name = name

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def get_hp(self):
        return self.hp

    def get_maxhp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_maxmp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self):
        i = 1
        print("\n" + "    " + bcolors.BOLD + self.name + bcolors.ENDC)
        print(bcolors.OKBLUE + bcolors.BOLD + "    ACTIONS: " + bcolors.ENDC)
        for item in self.actions:
            print("        " + str(i) + ":", item)
            i += 1

    def choose_magic(self):
        i = 1
        print("\n" + bcolors.OKGREEN + bcolors.BOLD + "    MAGIC: " + bcolors.ENDC)
        for spell in self.magic:
            print("        " + str(i) + ":", spell.name, "(cost:" + str(spell.cost) + ")")
            i += 1

    def choose_item(self):
        i = 1
        print("\n" + bcolors.OKGREEN + bcolors.BOLD + "    ITEMS: " + bcolors.ENDC)
        for item in self.items:
            print("        " + str(i) + ".", item["item"].name + ":", item["item"].description + " (x" + str(item["quantity"]) + ")")
            i += 1

    def choose_target(self, enemies):
        i = 1
        print("\n" + bcolors.FAIL + bcolors.BOLD + "    TARGET: " + bcolors.ENDC)
        for enemy in enemies:
            if enemy.get_hp() != 0:
                print("        " + str(i) + ".", enemy.name)
                i += 1
        choice = int(input("    Choose target: "))-1
        return choice

    def get_enemy_stats(self):
        en_bar = ""
        en_tick = (self.hp/self.maxhp) * 100 / 2
        while en_tick > 0:
            en_bar += "█"
            en_tick -= 1
        while len(en_bar) < 50:
            en_bar += " "

        en_string = str(self.hp) + "/" + str(self.maxhp)
        current_en = ""

        if len(en_string) < 11:
            decen = 11 - len(en_string)

            while decen > 0:
                current_en += " "
                decen -= 1

            current_en += en_string
        else:
            current_en = en_string

        print("                             __________________________________________________")
        print(bcolors.BOLD + self.name + "        " +
              current_en + " |" + bcolors.FAIL + en_bar + bcolors.ENDC + bcolors.BOLD + "|")

    def get_stats(self):
        hp_bar = ""
        bar_tick = (self.hp/self.maxhp) * 100 / 4

        mp_bar = ""
        mp_tick = (self.mp / self.maxmp) * 100 / 10

        while bar_tick > 0:
            hp_bar += "█"
            bar_tick -= 1

        while len(hp_bar) < 25:
            hp_bar += " "

        while mp_tick > 0:
            mp_bar += "█"
            mp_tick -= 1

        while len(mp_bar) < 10:
            mp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""
        mp_string = str(self.mp) + "/" + str(self.maxmp)
        current_mp = ""

        if len(mp_string) < 7:
            decmp = 7 - len(mp_string)

            while decmp>0:
                current_mp += " "
                decmp -= 1

            current_mp += mp_string
        else:
            current_mp = mp_string

        if len(hp_string) < 9:
            dec = 9 - len(hp_string)

            while dec>0:
                current_hp += " "
                dec -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        print("                             _________________________                    __________")
        print(bcolors.BOLD + self.name + "          " +
              current_hp + " |" + bcolors.OKGREEN + hp_bar + bcolors.ENDC + bcolors.BOLD + "|          " +
              current_mp + " |" + bcolors.OKBLUE + mp_bar + bcolors.ENDC + "|")

    # enemy_spells = [fire, blizzard, curata]
    # enemy_spells = [{"spell":fire, "quantity": 9999}, {"spell":blizzard, "quantity": 9999}, {"spell":curata, "quantity": 2}]

    def choose_enemy_spell(self):
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]#["spell"]
        #quantity = self.magic[magic_choice]["quantity"]
        magic_dmg = spell.generate_damage()

        pct = self.hp/self.maxhp

        if self.mp < spell.cost or spell.type == 'white' and pct > 50:# and quantity < 1:
            #print("quantity white: ", quantity)
            self.choose_enemy_spell()
        else:
            #quantity -= 1
            #print("remaining quantity: ", quantity)
            return spell, magic_dmg

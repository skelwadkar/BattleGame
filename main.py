from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

# Black magic
fire = Spell("Fire", 20, 500, "black")
thunder = Spell("Thunder", 22, 600, "black")
blizzard = Spell("Blizzard", 25, 700, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 130, "black")

# White magic
cure = Spell("Cure", 25, 650, "white")
cura = Spell("Cura", 35, 1400, "white")
curata = Spell("Curata", 50, 3000, "white")

player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spells = [fire, blizzard, curata]

# Create Items
potion = Item("Potion", "potion", "50 health points", 50)
hipotion = Item("Hi-Potion", "potion", "100 health points", 100)
superpotion = Item("Super Potion", "potion", "500 health points", 500)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one team member", 9999)
hielixir = Item("Hielixir", "elixir", "Fully restores HP/MP of all team members", 9999)
grenade = Item("Grenade", "attack", "deals 500 damage", 500)

player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 10},
                {"item": superpotion, "quantity": 5},
                {"item": elixir, "quantity": 3}, {"item": hielixir, "quantity": 1}, {"item": grenade, "quantity": 10}]

# Player Instantiation
player1 = Person("Valerie ", 3800, 145, 300, 34, player_spells, player_items)
player2 = Person("Sonal   ", 4200, 180, 315, 35, player_spells, player_items)
player3 = Person("Bot     ", 3200, 120, 200, 35, player_spells, player_items)

enemy1 = Person("Procus  ", 1400, 140, 572, 325, enemy_spells, [])
enemy2 = Person("Xerxes  ", 19200, 695, 512, 25, enemy_spells, [])
enemy3 = Person("Trevor  ", 1400, 140, 572, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

run = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "BATTLE GAME" + bcolors.ENDC)

while run:
    print("=============================")
    print("\n\n")
    print("NAME                         HP                                          MP")
    for player in players:
        player.get_stats()

    print("\n")
    for enemy in enemies:
        enemy.get_enemy_stats()
    print("\n")

    for player in players:
        player.choose_action()
        ind = int(input("    Choose Action: ")) - 1

        if ind == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("\n" + player.name.replace(" ", "") + " attacks " + enemies[enemy].name.replace(" ", "") +
                  " for " + str(dmg) + " points.")

            if enemies[enemy].get_hp() == 0:
                print(bcolors.FAIL + enemies[enemy].name.replace(" ", "") + " has died." + bcolors.ENDC)
                del enemies[enemy]

        elif ind == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough magic points\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == 'white':
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals " + player.name.replace(" ", "") + " with " + str(
                    magic_dmg) + " health points. " + bcolors.ENDC)
            elif spell.type == 'black':
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + player.name.replace(" ", "") + " casts " + spell.name + ", deals " +
                      str(magic_dmg) + " points of damage to " + enemies[enemy].name.replace(" ", "") + "." + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(bcolors.FAIL + enemies[enemy].name.replace(" ", "") + " has died." + bcolors.ENDC)
                    del enemies[enemy]

        elif ind == 2:
            player.choose_item()
            item_choice = int(input("    Choose item: ")) - 1
            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]
            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "Out of stock..." + bcolors.ENDC)
                continue
            player.items[item_choice]["quantity"] -= 1

            if item.type == 'potion':
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals " + player.name.replace(" ", "") + " for " + str(item.prop) + " health points" + bcolors.ENDC)
            elif item.type == 'elixir':
                if item.name == 'Elixir':
                    for individual in players:
                        individual.hp = individual.maxhp
                        individual.mp = individual.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP for " + player.name.replace(" ", "") + bcolors.ENDC)
            elif item.type == 'attack':
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals " + str(item.prop) + " points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(bcolors.FAIL + enemies[enemy].name.replace(" ", "") + " has died." + bcolors.ENDC)
                    del enemies[enemy]

    #Check if battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    if player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    #Player won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "YOU WIN" + bcolors.ENDC)
        run = False

    # Enemies won
    if defeated_players == 2:
        print(bcolors.FAIL + "YOU LOSE" + bcolors.ENDC)
        run = False

    print("\n")
    #Enemies attack strategy
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            #attack
            target = random.randrange(0,3)
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print("\n" + enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(" ", "") + " for: ", str(enemy_dmg) + ".")

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == 'white':
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + spell.name + " heals " + enemy.name.replace(" ", "") + " for "+ str(
                    magic_dmg) + " health points " + bcolors.ENDC)
            elif spell.type == 'black':
                target = random.randrange(0, 3)
                players[target].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + " casts " + spell.name + ", deals " +
                      str(magic_dmg) + " points of damage to " + players[target].name.replace(" ", "") + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(bcolors.FAIL + players[target].name.replace(" ", "") + " has died." + bcolors.ENDC)
                    del players[target]

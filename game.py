import random
from re import search

worldWidth = 3

player = {
    "name":"Player",
    "health": 25,
    "pos": 0,
    "inventory": {},
    "xp": 0,
    "lvl": 0
}

enemys = [
{
    "name":"Skeleton",
    "health": 20,
    "dmg": 10,
    "chance": 10,
    "inventory": {"Bow":{"dmg":10,"crit":10,"durability":10}},
    "drop": 20
},
{
    "name":"Zombie",
    "health": 20,
    "dmg": 10,
    "chance": 10,
    "inventory": {"SwordZom":{"dmg":10,"crit":10,"durability":10}},
    "drop": 100
},
{
    "name":"Mage",
    "health": 20,
    "dmg": 10,
    "chance": 10,
    "inventory": {"FireSpell":{"dmg":10,"crit":10,"durability":10}},
    "drop": 10
},
]

possibleItems = {
"Sword":{"dmg":10,"crit":10,"durability":10},
"Bow":{"dmg":10,"crit":10,"durability":10},
"Spell":{"dmg":5,"crit":20,"durability":8}
}

rooms = [
{
    "name":"Dungeon",
    "enemys": [],
    "action":[],
    "level":1,
    "items": {}
},
{
    "name":"Hallway",
    "enemys": [0],
    "action":[],
    "level":1,
    "items": {}
},
{
    "name":"Dungeon",
    "enemys": [1,2],
    "action":[],
    "level":1,
    "items": {}
},
{
    "name":"Dungeon",
    "enemys": [],
    "action":[],
    "level":1,
    "items": {}
},
{
    "name":"Dungeon",
    "enemys": [],
    "action":[],
    "level":1,
    "items": {}
},
{
    "name":"Dungeon",
    "enemys": [],
    "action":[],
    "level":1,
    "items": {}
},
{
    "name":"Dungeon",
    "enemys": [],
    "action":[],
    "level":1,
    "items": {}
},
{
    "name":"Dungeon",
    "enemys": [],
    "action":[],
    "level":1,
    "items": {}
},
{
    "name":"Dungeon",
    "enemys": [],
    "action":[],
    "level":1,
    "items": {}
}
]

def gameStart():
    chooseWeapon = input(f'Choose a weapon. {", ".join(possibleItems.keys())}\n')
    input("")
    player["inventory"][chooseWeapon] = possibleItems[chooseWeapon]
    newRoom(0)


def newRoom(pos):
    room = rooms[pos]
    print(f"You are now in the {room['name']}")
    if len(room['enemys']) != 0:
        enemy = enemys[room['enemys'][random.randint(0, len(room['enemys'])- 1)]]
        print(f"In this room you encounter a {enemy['name']} with {enemy['health']}hp")
    
    while 1:
        action = input("").split()

        if len(action) == 0:
            continue
        elif len(action) < 2:
            args = 0
        else:
            args = action[1]

        match action[0]: 
            case "/fight": fight(enemy,room)
            case "/move": move(pos, args)
            case "/inventory": inventory(args)
            case "/commands": commands()
            case "/drop": drop(args, room) #Drop multible things?
            case "/stats": stats()
            case "/search": searchGround(room)
            case _: continue

def searchGround(room):
    items = list(room['items'].keys())
    print(f"On the ground is: {', '.join(items)}")


def move(pos,arg):
    match arg: 
        case "down": newRoom(pos - worldWidth)
        case "up": newRoom(pos + worldWidth)
        case "left": newRoom(pos - 1)
        case "right": newRoom(pos + 1)
        
        
def fight(enemy,room):
    if enemy["health"] <= 0:
        print("There is no Enemy to fight in this Room")
        return
    enemy["dmg"] = enemy["dmg"] * room["level"] * (random.randint(9, 11) / 10)
    enemy["health"] = enemy["health"] * room["level"]
    weapons = list(player["inventory"].keys())
    print(f"Your Inventory contains {', '.join(weapons)} ")
    enemyWeapons = list(enemy["inventory"].keys())
    combat(enemy,enemyWeapons,weapons)


def combat(enemy,enemyWeapons, weapons):
    attackWeapon = input("Weapon?: ")

    if attackWeapon in weapons:
        pass
    else:
        combat(enemy,enemyWeapons, weapons)
        return

    dmgDealtEnemy = calcDmg(player, attackWeapon)
    enemy["health"] =  enemy["health"] - dmgDealtEnemy
    if enemy["health"] < 1:
        print(f"You attacked the {enemy['name']} with your {attackWeapon}\nThe {enemy['name']} died")
        loot(enemy,enemyWeapons)
        return
    print(f"You attacked the {enemy['name']} for {dmgDealtEnemy} with your {attackWeapon}\nThe {enemy['name']} now has {enemy['health']}hp")
    enemyWeapon = enemyWeapons[random.randint(0, len(enemy["inventory"]) - 1)]
    dmgDealtPlayer = calcDmg(enemy, enemyWeapon)
    player["health"] = player["health"] - dmgDealtPlayer
    if player["health"] <= 0:
        death()
    print(f"The {enemy['name']} attacked you for {dmgDealtPlayer} with this {enemyWeapon}\nYou are now at {player['health']}hp")
    combat(enemy, enemyWeapons, weapons)


def crit(weapon, attacker):
    if random.randint(0, 100) < attacker["inventory"][weapon]["crit"]:
        return attacker["inventory"][weapon]["dmg"]
    else:
        return 0


def calcDmg(attacker, weapon):
    return round(attacker["inventory"][weapon]["dmg"] * (random.randint(8, 12) / 10) + crit(weapon,attacker))


def loot(enemy,enemyWeapons):
    if random.randint(0, 100) < enemy["drop"]:
        dropWeapon = enemyWeapons[random.randint(0, len(enemy["inventory"]) - 1)]
        c = input(f"The {enemy['name']} dropped this {dropWeapon} with {enemy['inventory'][dropWeapon]['dmg']} attack, {enemy['inventory'][dropWeapon]['crit']} crit and {enemy['inventory'][dropWeapon]['durability']} durability\nDo wou want to keep it?\n")
        if c == "y":
            name = input("What should be the name of this Item?\n")
            player["inventory"][name] = enemy["inventory"][dropWeapon]
        
        
def death():
    return 0


def inventory(weapon):
    if weapon != 0:
        print(f"Your {weapon} has {player['inventory'][weapon]['dmg']} damage, {player['inventory'][weapon]['durability']} durability and a {player['inventory'][weapon]['crit']} chance of critical damage")
    else:
        weapons = list(player["inventory"].keys())
        print(f"Your Inventory contains {', '.join(weapons)}")


def stats():
    print(f"You have {player['health']}hp and {player['xp']}xp")


def drop(arg, room):
    room['items'][arg] = player['inventory'][arg]
    player["inventory"].pop(arg, None)


def commands():
    return

gameStart()

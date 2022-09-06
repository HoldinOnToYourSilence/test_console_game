import random

worldWidth = 3

player = {
    "name":"Player",
    "health": 25,
    "pos": 0,
    "inventory": {"Sword":{"dmg":10,"crit":10,"durability":10}},
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

possibleItems = [
{
    "name":"Sword",
    "basDmg": 10
},
{
    "name":"Bow",
    "basDmg": 7
},
{
    "name":"Spell",
    "basDmg": 5,
    "buff":{}
},
]

rooms = [
{
    "name":"Dungeon",
    "enemys": [],
    "action":[],
    "level":1
},
{
    "name":"Hallway",
    "enemys": [0],
    "action":[],
    "level":1
},
{
    "name":"Dungeon",
    "enemys": [1,2],
    "action":[],
    "level":1
},
{
    "name":"Dungeon",
    "enemys": [],
    "action":[],
    "level":1
},
{
    "name":"Dungeon",
    "enemys": [],
    "action":[],
    "level":1
},
{
    "name":"Dungeon",
    "enemys": [],
    "action":[],
    "level":1
},
{
    "name":"Dungeon",
    "enemys": [],
    "action":[],
    "level":1
},
{
    "name":"Dungeon",
    "enemys": [],
    "action":[],
    "level":1
},
{
    "name":"Dungeon",
    "enemys": [],
    "action":[],
    "level":1
}
]


def newRoom(pos):
    room = rooms[pos]
    print(f"You are now in the {room['name']}")
    if len(room['enemys']) != 0:
        enemy = enemys[room['enemys'][random.randint(0, len(room['enemys'])- 1)]]
        print(f"In this room you encounter a {enemy['name']}")
    
    while 1:
        action = input("").split()
        match action[0]: 
            case "/fight": fight(enemy,room)
            case "/move": move(pos, action[1])
            case "/inventory": inventory()
            case "/commands": commands()
            case "/drop": drop(action[1]) #Drop multible things?
            case "/stats": stats()


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
    combat(enemy,enemyWeapons)


def combat(enemy,enemyWeapons):
    attackWeapon = input("Weapon?: ")
    enemy["health"] = calcDmg(player, enemy, attackWeapon)
    if enemy["health"] < 1:
        print(f"You attacked the {enemy['name']} with your {attackWeapon}\nThe {enemy['name']} died")
        loot(enemy,enemyWeapons)
        return
    print(f"You attacked the {enemy['name']} with your {attackWeapon}\nThe {enemy['name']} now has {enemy['health']}hp")
    enemyWeapon = enemyWeapons[random.randint(0, len(enemy["inventory"]) - 1)]
    player["health"] = calcDmg(enemy, player, enemyWeapon)
    if player["health"] <= 0:
        death()
    print(f"The {enemy['name']} attacked you with this {enemyWeapon}\nYou are now at {player['health']}hp")
    combat(enemy, enemyWeapons)


def crit(weapon, attacker):
    if random.randint(0, 100) < attacker["inventory"][weapon]["crit"]:
        return attacker["inventory"][weapon]["dmg"]
    else:
        return 0


def calcDmg(attacker, defender, weapon):
    return defender["health"] - round(attacker["inventory"][weapon]["dmg"] * (random.randint(8, 12) / 10) + crit(weapon,attacker))


def loot(enemy,enemyWeapons):
    if random.randint(0, 100) < enemy["drop"]:
        dropWeapon = enemyWeapons[random.randint(0, len(enemy["inventory"]) - 1)]
        c = input(f"The {enemy['name']} dropped this {dropWeapon} with {enemy['inventory'][dropWeapon]['dmg']} attack, {enemy['inventory'][dropWeapon]['crit']} crit and {enemy['inventory'][dropWeapon]['durability']} durability\nDo wou want to keep it?\n")
        if c == "y":
            name = input("What should be the name of this Item?\n")
            player["inventory"][name] = enemy["inventory"][dropWeapon]
        
        
def death():
    return 0


def inventory():
    weapons = list(player["inventory"].keys())
    print(f"Your Inventory contains {', '.join(weapons)} ")


def stats():
    print(f"You have {player['health']}hp and {player['xp']}xp")


def drop(arg):
    player["inventory"].pop(arg, None)


def commands():
    return


newRoom(0)

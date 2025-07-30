"""
AlgoCratic Futures MUD - Using adventurelib for MVP
Quick implementation to get arcade playable
"""

import adventurelib as adv
from adventurelib import *
import os
import yaml
from typing import Dict

# === Room Setup ===

# Add custom directions
Room.add_direction('arcade', 'boardwalk')
Room.add_direction('tunnel', 'boardwalk')
Room.add_direction('movement', 'main')

# Create our starting rooms manually for MVP
boardwalk = Room("""
Wooden planks run east-west here, newer than the main stretch but already 
showing wear from joggers and dog walkers. The R.C. Harris filtration plant 
looms to the west like an art deco castle. Someone's carved "VR WORLDS →" 
into a bench, pointing toward the arcade.
""")

arcade_entrance = Room("""
A weather-beaten arcade on the pier, neon signs flickering in the lake 
breeze. "VIRTUAL REALITY WORLDS" blinks above the door, half the letters 
dead. Sounds of 8-bit music and lake waves mix. Someone's spray-painted 
"LEARN THE GAME" on the wall.
""")

arcade_main = Room("""
Rows of ancient arcade cabinets held together by duct tape and hope.
Most still work, somehow. The carpet is sticky. Prize tickets litter
the floor. Signs point to different "VR WORLDS": MOVEMENT TRAINER,
LOOK SIMULATOR, INTERACTION TUTORIAL, SOCIAL DYNAMICS.
""")

movement_tutorial = Room("""
A classic text adventure training room. Arrows painted on the walls
show NORTH, SOUTH, EAST, WEST. A friendly hologram explains:
"Welcome to movement training! Type 'north' or 'n' to go north!
Try 'look' to see exits. Type 'help' if you're stuck!"
""")

storm_drain = Room("""
Concrete curves overhead in this surprisingly dry tunnel. Christmas lights 
string along the ceiling, powered by who knows what. Cardboard signs 
advertise 'DAVE'S DUNGEON,' 'MARIA'S MINDSCAPE,' and 'THE INFINITY CLOSET.' 
The sound of the lake echoes strangely here.
""")

# Connect rooms
boardwalk.arcade = arcade_entrance
arcade_entrance.out = boardwalk
arcade_entrance.north = arcade_main
arcade_main.south = arcade_entrance
arcade_main.movement = movement_tutorial
movement_tutorial.out = arcade_main

# Hidden connection
boardwalk.tunnel = storm_drain
storm_drain.out = boardwalk

# Set starting room
current_room = boardwalk

# === Items ===

# Arcade items
Item.take_aliases = ['get', 'grab', 'pick up']

ticket = Item('arcade ticket', 'ticket')
ticket.description = "A golden ticket that says 'ONE WINNER!'"

arcade_map = Item('arcade map', 'map') 
arcade_map.description = "A hand-drawn map showing all the VR worlds."

# Add items to rooms
arcade_entrance.items = Bag([arcade_map])
arcade_main.items = Bag([ticket])

# Player inventory
inventory = Bag()

# === Game State ===

class GameState:
    def __init__(self):
        self.clearance = "R"
        self.name = "Employee"
        self.learned_commands = set()
        
game_state = GameState()

# === Commands ===

@when('look')
@when('l')
def look():
    print(current_room)
    if current_room.items:
        for item in current_room.items:
            print(f"There is {item.name} here.")

@when('look at THING')
@when('examine THING')
def examine(thing):
    item = current_room.items.find(thing)
    if item:
        print(item.description)
    else:
        print(f"You don't see any {thing} here.")

@when('inventory')
@when('i')
def show_inventory():
    if inventory:
        print("You have:")
        for item in inventory:
            print(f"  - {item.name}")
    else:
        print("You're not carrying anything.")

@when('take THING')
@when('get THING')
def take_item(thing):
    item = current_room.items.take(thing)
    if item:
        inventory.add(item)
        print(f"You take the {item.name}.")
        if thing == 'ticket':
            game_state.learned_commands.add('take')
            print("Tutorial progress: You learned the TAKE command!")
    else:
        print(f"There's no {thing} here.")

@when('drop THING')
def drop_item(thing):
    item = inventory.take(thing)
    if item:
        current_room.items.add(item)
        print(f"You drop the {item.name}.")
    else:
        print(f"You're not carrying a {thing}.")

@when('status')
def show_status():
    print(f"=== EMPLOYEE STATUS ===")
    print(f"Name: {game_state.name}")
    print(f"Clearance: {game_state.clearance}")
    print(f"Location: {current_room.name if hasattr(current_room, 'name') else 'Unknown'}")
    print(f"Commands learned: {len(game_state.learned_commands)}")

@when('help')
def help_command():
    print("""
=== ALGOCRATIC FUTURES HELP ===
Movement: north/n, south/s, east/e, west/w, or any exit name
Looking: look/l, look at [thing]
Items: take/get [item], drop [item], inventory/i
System: help, status, quit

Visit the arcade to learn more commands!
""")

@when('say WORDS')
def say(words):
    print(f'You say "{words}"')
    if current_room == movement_tutorial and words.lower() == "hello":
        print('The tutorial hologram waves back! "Hello, new employee!"')

# === Direction handling ===

@when('north', direction='north')
@when('n', direction='north')
@when('south', direction='south')
@when('s', direction='south')
@when('east', direction='east')
@when('e', direction='east')
@when('west', direction='west')
@when('w', direction='west')
def go_direction(direction):
    global current_room
    room = current_room.exit(direction)
    if room:
        current_room = room
        print(f"You go {direction}.")
        look()
        if current_room == movement_tutorial:
            game_state.learned_commands.add('movement')
            print("\nTutorial: Great job! You learned basic movement!")
    else:
        print(f"You can't go {direction} from here.")

# Special exits
@when('arcade')
@when('tunnel')
@when('movement')
@when('out')
def go_special(direction):
    global current_room
    if hasattr(current_room, direction):
        current_room = getattr(current_room, direction)
        print(f"You go to the {direction}.")
        look()
    else:
        print(f"You can't go there from here.")

# === MVP Launch ===

def start_game():
    print("""
╔═══════════════════════════════════════════════════════════════╗
║           WELCOME TO ALGOCRATIC FUTURES                       ║
║                                                               ║
║  You stand on the boardwalk at Bellamy. The lake stretches   ║
║  endlessly before you. Behind you, the city hums with        ║
║  productivity metrics.                                        ║
║                                                               ║
║  To the east, an old arcade promises "VR WORLDS" and         ║
║  "LEARN THE GAME". Maybe you should check it out?            ║
║                                                               ║
║  Type 'help' for commands.                                   ║
║  Type 'look' to see your surroundings.                       ║
╚═══════════════════════════════════════════════════════════════╝
""")
    look()

if __name__ == "__main__":
    start_game()
    start()  # Start adventurelib's game loop
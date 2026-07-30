# Room Authoring Guide - 5 Minute Version

## Quick Start: Your First Room

### Step 1: Create a YAML file
Create a new file in `rooms/community/` called `your_room.yaml`:

```yaml
my_first_room:
  name: "Break Room"
  description: "A dimly lit break room with a broken coffee machine"
  exits:
    north: "boardwalk"
```

That's it! You've made a room.

### Step 2: Test It
1. Start the game: `python backend/launch_mvp.py`
2. Type: `go my_first_room` (if connected)

## Room Template (Copy This)

```yaml
room_id:  # Must be unique, use underscores not spaces
  name: "Display Name"  # What players see as title
  description: "What players see when they look"
  exits:
    north: "other_room_id"  # Cardinal directions
    south: "another_room"
    east: "somewhere_else"
    west: "back_home"
    up: "attic"
    down: "basement"
    out: "exit_room"
    in: "enter_room"
    # Special exits (any word works):
    portal: "magic_place"
    tunnel: "secret_area"
    door: "behind_door"
```

## Advanced Features (Optional)

### Corporate vs Reality Descriptions
```yaml
drain_entrance:
  name: "Storm Drain Entrance"
  description: "A rusted grate barely visible beneath corporate propaganda posters"
  corporate_description: "Authorized maintenance access only. Productivity monitoring in effect."
  exits:
    down: "drain_tunnel"
    out: "boardwalk"
```

### Adding NPCs
```yaml
office_cubicle:
  name: "Cubicle Farm"
  description: "Endless rows of identical workstations"
  agents:
    - "liza"  # NPCs that appear here
    - "kevin"
  exits:
    out: "hallway"
```

### Hidden Exits
```yaml
arcade:
  name: "Boardwalk Arcade"
  description: "Flashing lights and broken dreams"
  exits:
    out: "boardwalk"
    north: "tutorial_hall"
    # This won't show in 'exits' command:
  hidden_exits:
    behind_counter: "staff_room"
```

### Items (Future Feature)
```yaml
workshop:
  name: "Abandoned Workshop"
  description: "Tools scattered on dusty workbenches"
  items:
    - "rusty_key"
    - "broken_radio"
  exits:
    out: "alley"
```

## Real Examples From Game

### Simple Room
```yaml
# From rooms/boardwalk_arcade/arcade_main.yaml
ticket_counter:
  name: "Ticket Counter"
  description: "A glass case displays prizes nobody can afford. The attendant is absent."
  exits:
    out: "arcade_main"
```

### Room With Personality
```yaml
drain_tunnel:
  name: "Storm Drain Tunnel"
  description: "Water drips steadily. The walls are covered in graffiti - layers of truth painted over corporate lies."
  corporate_description: "Unauthorized area. Your presence has been logged."
  exits:
    up: "drain_entrance"
    north: "drain_junction"
    south: "drain_depths"
```

### Hub Room With Multiple Exits
```yaml
arcade_main:
  name: "Arcade Main Floor"
  description: "Broken machines flicker with false promises. A few still function."
  exits:
    out: "boardwalk"
    north: "tutorial_hall"
    east: "ticket_counter"
    west: "food_court"
    stairs: "arcade_upper"
```

## Writing Tips

### Good Descriptions
- **Set mood**: "Flickering fluorescents cast harsh shadows"
- **Add details**: "A coffee stain shaped like a question mark"
- **Hint at story**: "Someone carved 'THEY KNOW' into the desk"

### Bad Descriptions
- Too generic: "It's a room"
- Too long: [500 word essay about the room]
- Breaking theme: "A nice sunny pleasant room full of joy"

### Theme Guidelines
- **Corporate areas**: Sterile, monitored, optimized
- **Hidden areas**: Real, broken, human
- **Transition zones**: Facade cracking, truth bleeding through

## File Organization

```
rooms/
  boardwalk_arcade/     # Starting area
    arcade_main.yaml
    tutorial_games.yaml
  anonymous_sysop/      # Hidden areas
    micromuse_apartment.yaml
    drain_system.yaml
  community/           # Your rooms go here!
    your_name/
      cool_room.yaml
```

## Testing Your Room

1. **Syntax Check**: Open in text editor, look for red squiggles
2. **Load Test**: Start game, see if it crashes
3. **Navigation Test**: Can you enter and exit?
4. **Description Test**: Does it display correctly?

## Common Mistakes

❌ **Forgetting quotes**
```yaml
description: Water drips  # BAD - might break
description: "Water drips"  # GOOD
```

❌ **Wrong indentation**
```yaml
room:
name: "Bad"  # BAD - needs indentation
  name: "Good"  # GOOD
```

❌ **Duplicate room IDs**
```yaml
# In file1.yaml
test_room:
  name: "Test 1"

# In file2.yaml  
test_room:  # BAD - ID already used
  name: "Test 2"
```

❌ **Exit to nowhere**
```yaml
exits:
  north: "room_that_doesnt_exist"  # Will confuse players
```

## Quick Room Ideas

- **Maintenance Shaft**: Hidden pathways between corporate areas
- **Server Room**: The algorithm's physical presence
- **Abandoned Office**: What happens to terminated employees
- **Loading Dock**: Where reality enters the corporate machine
- **Rooftop**: Escape? Or just another level of surveillance?

## Share Your Rooms!

Created something cool? 
1. Put it in `rooms/community/your_name/`
2. Test it works
3. Submit a PR with description

## Need Help?

- Check existing rooms in `rooms/` for examples
- Error when loading? Check YAML syntax
- Can't find your room? Check file is in `rooms/` subdirectory
- Still stuck? The game will tell you what's wrong when it crashes

---

*Remember: Every room tells a story. What's yours?*
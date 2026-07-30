# Room Authoring Guide for AlgoCratic Futures

## Quick Start
Write rooms in YAML format. We'll convert them to Evennia later.

## Basic Room Template

```yaml
room_id: your_unique_room_id
name: Room Display Name
clearance: R  # R/O/Y/G/B/I/V/UV

descriptions:
  corporate: What employees see (boring corporate speak)
  reality: What's actually there (the truth in the storm drains)

exits:
  north: other_room_id
  south: another_room_id
  secret_door: hidden_room_id  # Can have any exit names

agents: [optional_agent_id]  # Who lives here
items: [pizza_box, old_laptop]  # What's lying around
```

## Example Room

```yaml
room_id: server_closet
name: IT Infrastructure Room
clearance: Y  # Yellow clearance required

descriptions:
  corporate: |
    A clean, organized server room with optimal temperature control.
    Blinking lights indicate healthy system performance. A sign reads:
    "Authorized Personnel Only - Your Access Has Been Logged"
    
  reality: |
    Dozens of raspberry pis duct-taped to the storm drain walls, 
    connected by a rainbow of ethernet cables. A hamster wheel 
    powers the backup generator. Post-it notes everywhere read 
    "DO NOT TOUCH - EVERYTHING WILL BREAK"

exits:
  out: storm_drain
  crawlspace: secret_lab
  up: manhole_cover

agents: [it_goblin]
items: [raspberry_pi, hamster_wheel, pile_of_cables]
```

## Special Room Types

### Reality-Shifting Rooms
```yaml
room_id: quantum_hallway
name: Probability Corridor
clearance: B

descriptions:
  shifting: true  # This room changes
  variants:
    - "A long hallway stretches before you"
    - "A short hallway ends abruptly"  
    - "There is no hallway. There never was"
    - "ERROR: Hallway overflow exception"
```

### Clearance-Based Descriptions
```yaml
room_id: executive_washroom
name: Executive Facilities
clearance: O  # Anyone Orange+ can enter

descriptions:
  R: "A door marked 'No Entry'"
  O: "A basic employee restroom"
  Y: "A slightly nicer restroom with real soap"
  G: "Wait, why is there a hidden panel here?"
  B: "The hidden panel leads to a speakeasy"
  UV: "Through the speakeasy: the storm drain throne room"
```

## Writing Tips

1. **Corporate descriptions** should be:
   - Sterile, corporate doublespeak
   - Focused on productivity and monitoring
   - Slightly unsettling

2. **Reality descriptions** should reveal:
   - The actual storm drain setting
   - Student creativity and chaos
   - The truth behind the corporate facade

3. **Exit names** can be creative:
   - Standard: north, south, east, west
   - Fun: crawl_through_vent, behind_poster, reflection
   - Conditional: emergency_exit, managers_only

4. **Clearance levels** control access:
   - R (Red): Public areas
   - G (Green): Behind the scenes
   - B (Blue): Secret areas
   - UV (Ultraviolet): Admin only

## File Organization

Create your rooms in: `rooms/author_name/`

```
rooms/
  sweeney/
    - boardwalk.yaml
    - storm_drain.yaml
  liza/
    - experiment_rooms.yaml
    - reality_lab.yaml
  new_author/
    - your_rooms_here.yaml
```

## Validation

Run this to check your room:
```bash
python validate_room.py rooms/your_name/room_file.yaml
```

---

*Remember: Every corporate facade hides a storm drain story*
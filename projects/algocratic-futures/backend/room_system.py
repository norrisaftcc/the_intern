"""
Room System for AlgoCratic Futures
The storm drains beneath Toronto hide more than pipes
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import random
import math
from datetime import datetime

class RoomState(Enum):
    """Reality states for rooms"""
    CORPORATE = "corporate"      # What employees see
    REALITY = "reality"         # What's really there
    SHIFTING = "shifting"       # Between states
    GLITCHING = "glitching"    # Reality breaking down

@dataclass
class Room:
    """A location in the storm drain MUD"""
    id: str
    name: str
    corporate_desc: str  # What low clearance sees
    reality_desc: str    # What high clearance sees
    exits: Dict[str, str] = field(default_factory=dict)
    agents: List[str] = field(default_factory=list)
    items: List[str] = field(default_factory=list)
    clearance_required: str = "R"
    state: RoomState = RoomState.CORPORATE
    
    def get_description(self, observer_clearance: str) -> str:
        """Get room description based on observer's clearance"""
        from clearance_system import ClearanceLevel
        
        # Map clearance to perception level
        clearance_values = {
            "R": 0.1, "O": 0.2, "Y": 0.4, "G": 0.6,
            "B": 0.8, "I": 0.9, "V": 0.95, "UV": 1.0
        }
        
        perception = clearance_values.get(observer_clearance, 0.1)
        
        # Special rooms have special rules
        if self.id == "lizas_experiment":
            return self._get_shifting_description()
        
        # Higher clearance sees through the facade
        if perception >= 0.6:  # Green and above
            if perception >= 0.8:  # Blue and above see full reality
                return self.reality_desc
            else:  # Green/Yellow see mix
                return self._blend_descriptions(perception)
        
        return self.corporate_desc
    
    def _blend_descriptions(self, perception: float) -> str:
        """Blend corporate and reality descriptions"""
        if random.random() < perception:
            # Sometimes reality bleeds through
            corp_parts = self.corporate_desc.split('.')
            real_parts = self.reality_desc.split('.')
            
            blended = []
            for i in range(max(len(corp_parts), len(real_parts))):
                if random.random() < perception:
                    if i < len(real_parts):
                        blended.append(real_parts[i])
                else:
                    if i < len(corp_parts):
                        blended.append(corp_parts[i])
            
            return '. '.join(blended) + '.'
        
        return self.corporate_desc
    
    def _get_shifting_description(self) -> str:
        """Liza's experiment - reality constantly shifting"""
        templates = [
            "The room description writes itself as you watch.",
            "Words appear and disappear, trying different versions of reality.",
            "Sometimes it's a lab, sometimes a beach, sometimes just raw code bleeding through.",
            "The walls flicker between corporate gray and storm drain concrete.",
            "Error: Reality index out of bounds. Please try again.",
            "A note pinned to nothing says 'If you can read this, the experiment worked. -L'"
        ]
        
        # Use time-based selection for consistency within short periods
        index = int(datetime.now().timestamp() / 10) % len(templates)
        base = templates[index]
        
        # Add glitch effects
        if random.random() < 0.3:
            base += " ģ̸͎̈ľ̶̺̈́ì̸͇͐ṱ̶̈́͜c̷͎̈́h̷̬̆"
        
        return base

class MUDWorld:
    """The entire storm drain network"""
    
    def __init__(self):
        self.rooms: Dict[str, Room] = {}
        self.player_locations: Dict[str, str] = {}
        self._initialize_rooms()
    
    def _initialize_rooms(self):
        """Create the initial room network"""
        
        # Entrance - Boardwalk
        self.rooms["boardwalk"] = Room(
            id="boardwalk",
            name="Boardwalk at Bellamy",
            corporate_desc="Employee entrance checkpoint. Please present your ID badge for scanning. Productivity monitoring begins upon entry.",
            reality_desc="Wooden planks run east-west here, newer than the main stretch but already showing wear from joggers and dog walkers. The R.C. Harris filtration plant looms to the west like an art deco castle. Someone's carved 'VR WORLDS →' into a bench.",
            exits={"east": "beach", "west": "plant", "north": "kingston", "tunnel": "storm_drain"},
            clearance_required="R"
        )
        
        # Storm Drain Gallery - The Hub
        self.rooms["storm_drain"] = Room(
            id="storm_drain",
            name="Storm Drain Gallery", 
            corporate_desc="Maintenance corridor. Authorized personnel only. Your activities are being monitored for safety compliance.",
            reality_desc="Concrete curves overhead in this surprisingly dry tunnel. Christmas lights string along the ceiling, powered by who knows what. Cardboard signs advertise 'DAVE'S DUNGEON,' 'MARIA'S MINDSCAPE,' and 'THE INFINITY CLOSET.' The sound of the lake echoes strangely here.",
            exits={"out": "boardwalk", "dave": "daves_dungeon", "maria": "marias_mindscape", 
                   "closet": "infinity_closet", "deeper": "builders_lounge"},
            agents=["vi", "newcomer_guide"],
            clearance_required="R"
        )
        
        # Builder's Lounge - Where real work happens
        self.rooms["builders_lounge"] = Room(
            id="builders_lounge",
            name="Deeper - The Builder's Lounge",
            corporate_desc="Employee break room. Please limit breaks to 15 minutes. Productivity tracking remains active during rest periods.",
            reality_desc="Mismatched furniture from dorm room clearouts. An ancient CRT glows with MUD code. Pizza boxes suggest recent habitation. A whiteboard shows connection diagrams between rooms that shouldn't connect. East leads to 'Liza's Experiment,' west to 'The Memory Palace.'",
            exits={"back": "storm_drain", "east": "lizas_experiment", "west": "memory_palace", 
                   "up": "schrodingers_apartment"},
            agents=["mentor_chen", "subprocess_claude"],
            items=["pizza_box", "whiteboard", "crt_monitor"],
            clearance_required="G"
        )
        
        # Liza's Experiment - Reality-bending room
        self.rooms["lizas_experiment"] = Room(
            id="lizas_experiment",
            name="Liza's Experiment",
            corporate_desc="Error: Description not found. Please contact IT support.",
            reality_desc="The room shifts. Reality optional. Warranty void.",
            exits={"out": "builders_lounge", "undefined": "quantum_space", "yesterday": "temporal_loop"},
            agents=["liza"],
            clearance_required="B",
            state=RoomState.GLITCHING
        )
        
        # Corporate Facade - What most employees see
        self.rooms["corporate_lobby"] = Room(
            id="corporate_lobby",
            name="AlgoCratic Futures Main Lobby",
            corporate_desc="Welcome to AlgoCratic Futures. Our pristine lobby showcases our commitment to excellence. Please report to reception for your productivity assessment. Remember: Your value is measured in output.",
            reality_desc="A hastily assembled facade in the storm drain entrance. Cardboard cubicles and printed motivational posters barely hide the concrete walls. The 'reception desk' is a folding table with a laptop.",
            exits={"out": "boardwalk", "elevator": "corporate_floors", "maintenance": "storm_drain"},
            agents=["evaluator_alpha"],
            clearance_required="R"
        )
    
    def get_room(self, room_id: str) -> Optional[Room]:
        """Get a room by ID"""
        return self.rooms.get(room_id)
    
    def move_player(self, player_id: str, direction: str) -> Tuple[bool, str]:
        """Move a player in a direction"""
        current_room_id = self.player_locations.get(player_id, "boardwalk")
        current_room = self.rooms.get(current_room_id)
        
        if not current_room:
            return False, "You are nowhere. This should not happen."
        
        if direction not in current_room.exits:
            return False, f"You cannot go {direction} from here."
        
        new_room_id = current_room.exits[direction]
        new_room = self.rooms.get(new_room_id)
        
        if not new_room:
            return False, "That direction leads nowhere. Reality fault detected."
        
        # Check clearance
        from clearance_system import ClearanceLevel
        player_clearance = self.get_player_clearance(player_id)
        
        if not self._check_room_access(player_clearance, new_room.clearance_required):
            return False, f"ACCESS DENIED. {new_room.clearance_required} clearance required."
        
        # Move successful
        self.player_locations[player_id] = new_room_id
        return True, f"You move {direction} to {new_room.name}."
    
    def _check_room_access(self, player_clearance: str, required_clearance: str) -> bool:
        """Check if player has clearance for room"""
        clearance_order = ["R", "O", "Y", "G", "B", "I", "V", "UV"]
        
        player_level = clearance_order.index(player_clearance) if player_clearance in clearance_order else 0
        required_level = clearance_order.index(required_clearance) if required_clearance in clearance_order else 0
        
        return player_level >= required_level
    
    def get_player_clearance(self, player_id: str) -> str:
        """Get player's clearance level - integrate with clearance system"""
        # TODO: Connect to actual clearance system
        return "G"  # Default to Green for testing
    
    def look_around(self, player_id: str) -> str:
        """Get current room description for player"""
        current_room_id = self.player_locations.get(player_id, "boardwalk")
        current_room = self.rooms.get(current_room_id)
        
        if not current_room:
            return "You are in the void. This is concerning."
        
        player_clearance = self.get_player_clearance(player_id)
        description = current_room.get_description(player_clearance)
        
        # Add exits
        exit_list = ", ".join(current_room.exits.keys())
        description += f"\n\nExits: {exit_list}"
        
        # Add visible agents
        if current_room.agents:
            agent_list = ", ".join(current_room.agents)
            description += f"\nPresent: {agent_list}"
        
        # Add visible items
        if current_room.items:
            item_list = ", ".join(current_room.items)
            description += f"\nYou see: {item_list}"
        
        return description

# Global world instance
world = MUDWorld()
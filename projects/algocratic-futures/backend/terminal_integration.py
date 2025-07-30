"""
Terminal Integration - Connect rooms to web interface
Quick MVP to get arcade playable
"""

from typing import Dict, Optional
from room_system import MUDWorld, Room
from room_loader import RoomLoader
from agent_system import AgentManager
import os

class TerminalCommands:
    """Handle player commands from terminal"""
    
    def __init__(self):
        self.world = MUDWorld()
        self.agents = AgentManager()
        self._load_rooms()
        
    def _load_rooms(self):
        """Load all rooms from YAML files"""
        # Load from rooms directory
        rooms_dir = os.path.join(os.path.dirname(__file__), '..', 'rooms')
        if os.path.exists(rooms_dir):
            loaded_rooms = RoomLoader.load_all_rooms(rooms_dir)
            # Add to world
            for room_id, room in loaded_rooms.items():
                self.world.rooms[room_id] = room
            print(f"Loaded {len(loaded_rooms)} rooms")
    
    def process_command(self, player_id: str, command: str) -> Dict:
        """Process a player command and return response"""
        cmd = command.lower().strip()
        parts = cmd.split(' ', 1)
        base_cmd = parts[0]
        args = parts[1] if len(parts) > 1 else ""
        
        # Movement commands
        if base_cmd in ['n', 'north', 's', 'south', 'e', 'east', 'w', 'west',
                        'up', 'down', 'out', 'exit'] or base_cmd in self._get_current_exits(player_id):
            return self._handle_movement(player_id, base_cmd)
        
        # Looking commands
        elif base_cmd in ['look', 'l']:
            if args:
                return self._handle_look_at(player_id, args)
            return self._handle_look(player_id)
        
        elif base_cmd == 'exits':
            return self._handle_exits(player_id)
        
        # System commands
        elif base_cmd == 'help':
            return self._handle_help()
        
        elif base_cmd == 'status':
            return self._handle_status(player_id)
        
        # Communication
        elif base_cmd == 'say':
            return self._handle_say(player_id, args)
        
        # Unknown command
        else:
            return {
                'type': 'error',
                'message': f"Unknown command: {base_cmd}. Type 'help' for commands."
            }
    
    def _get_current_exits(self, player_id: str) -> list:
        """Get exits from current room"""
        room_id = self.world.player_locations.get(player_id, "boardwalk")
        room = self.world.get_room(room_id)
        return list(room.exits.keys()) if room else []
    
    def _handle_movement(self, player_id: str, direction: str) -> Dict:
        """Handle movement commands"""
        # Normalize directions
        direction_map = {
            'n': 'north', 's': 'south', 'e': 'east', 'w': 'west',
            'u': 'up', 'd': 'down', 'o': 'out'
        }
        direction = direction_map.get(direction, direction)
        
        success, message = self.world.move_player(player_id, direction)
        
        if success:
            # Get new room description
            room_desc = self.world.look_around(player_id)
            return {
                'type': 'movement',
                'message': message,
                'room_description': room_desc,
                'exits': self._get_current_exits(player_id)
            }
        else:
            return {
                'type': 'error',
                'message': message
            }
    
    def _handle_look(self, player_id: str) -> Dict:
        """Handle look command"""
        description = self.world.look_around(player_id)
        return {
            'type': 'look',
            'message': description,
            'exits': self._get_current_exits(player_id)
        }
    
    def _handle_look_at(self, player_id: str, target: str) -> Dict:
        """Handle look at specific target"""
        # For MVP, just acknowledge
        return {
            'type': 'examine',
            'message': f"You examine the {target}. It looks interesting."
        }
    
    def _handle_exits(self, player_id: str) -> Dict:
        """Show available exits"""
        exits = self._get_current_exits(player_id)
        if exits:
            return {
                'type': 'info',
                'message': f"Exits: {', '.join(exits)}"
            }
        else:
            return {
                'type': 'info',
                'message': "There are no obvious exits. You're trapped!"
            }
    
    def _handle_help(self) -> Dict:
        """Show help"""
        return {
            'type': 'help',
            'message': """Available commands:
- Movement: north/n, south/s, east/e, west/w, up, down, out
- Looking: look/l, look at [thing], exits
- System: help, status
- Social: say [message]

The arcade has tutorials for all commands!"""
        }
    
    def _handle_status(self, player_id: str) -> Dict:
        """Show player status"""
        current_room = self.world.player_locations.get(player_id, "boardwalk")
        clearance = self.world.get_player_clearance(player_id)
        
        return {
            'type': 'status',
            'message': f"""Status Report:
Location: {current_room}
Clearance: {clearance}
Productivity: Variable
Compliance: Monitored"""
        }
    
    def _handle_say(self, player_id: str, message: str) -> Dict:
        """Handle say command"""
        if not message:
            return {
                'type': 'error',
                'message': "Say what?"
            }
        
        return {
            'type': 'communication',
            'message': f'You say "{message}"',
            'room_message': f'{player_id} says "{message}"'
        }

# Global instance for easy access
terminal = TerminalCommands()
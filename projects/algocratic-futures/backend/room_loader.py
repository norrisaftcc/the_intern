"""
Simple room loader for author-created content
Converts YAML to room objects
"""

import yaml
import os
from typing import Dict, List, Union
from room_system import Room, RoomState, MUDWorld

class RoomLoader:
    """Load rooms from YAML files"""
    
    @staticmethod
    def load_room_file(filepath: str) -> List[Room]:
        """Load rooms from a YAML file"""
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        
        rooms = []
        
        # Handle single room or list of rooms
        if isinstance(data, list):
            for room_data in data:
                room = RoomLoader._create_room(room_data)
                if room:
                    rooms.append(room)
        else:
            room = RoomLoader._create_room(data)
            if room:
                rooms.append(room)
        
        return rooms
    
    @staticmethod
    def _create_room(data: Dict) -> Room:
        """Create a Room object from YAML data"""
        
        # Handle different description formats
        descriptions = data.get('descriptions', {})
        
        # Simple format
        if 'corporate' in descriptions:
            corporate_desc = descriptions['corporate']
            reality_desc = descriptions.get('reality', descriptions['corporate'])
        
        # Clearance-based format
        elif any(key in descriptions for key in ['R', 'O', 'Y', 'G', 'B', 'I', 'V', 'UV']):
            # For now, use lowest and highest clearance descriptions
            corporate_desc = descriptions.get('R', 'A corporate space.')
            reality_desc = descriptions.get('UV', descriptions.get('B', corporate_desc))
        
        # Shifting format
        elif descriptions.get('shifting'):
            variants = descriptions.get('variants', [])
            corporate_desc = variants[0] if variants else 'A shifting space.'
            reality_desc = ' '.join(variants) if variants else corporate_desc
        
        else:
            corporate_desc = 'An undescribed corporate space.'
            reality_desc = 'An undescribed reality.'
        
        # Create room
        room = Room(
            id=data['room_id'],
            name=data['name'],
            corporate_desc=corporate_desc.strip(),
            reality_desc=reality_desc.strip(),
            exits=data.get('exits', {}),
            agents=data.get('agents', []),
            items=data.get('items', []),
            clearance_required=data.get('clearance', 'R'),
            state=RoomState.SHIFTING if descriptions.get('shifting') else RoomState.CORPORATE
        )
        
        return room
    
    @staticmethod
    def load_all_rooms(rooms_dir: str = 'rooms') -> Dict[str, Room]:
        """Load all rooms from a directory structure"""
        all_rooms = {}
        
        for author_dir in os.listdir(rooms_dir):
            author_path = os.path.join(rooms_dir, author_dir)
            if os.path.isdir(author_path):
                for filename in os.listdir(author_path):
                    if filename.endswith('.yaml') or filename.endswith('.yml'):
                        filepath = os.path.join(author_path, filename)
                        try:
                            rooms = RoomLoader.load_room_file(filepath)
                            for room in rooms:
                                all_rooms[room.id] = room
                                print(f"Loaded room '{room.name}' by {author_dir}")
                        except Exception as e:
                            print(f"Error loading {filepath}: {e}")
        
        return all_rooms
    
    @staticmethod
    def validate_room_file(filepath: str) -> List[str]:
        """Validate a room file and return any errors"""
        errors = []
        
        try:
            with open(filepath, 'r') as f:
                data = yaml.safe_load(f)
        except Exception as e:
            return [f"Failed to parse YAML: {e}"]
        
        rooms_data = data if isinstance(data, list) else [data]
        
        for i, room_data in enumerate(rooms_data):
            room_prefix = f"Room {i+1}: " if len(rooms_data) > 1 else ""
            
            # Required fields
            if 'room_id' not in room_data:
                errors.append(f"{room_prefix}Missing required field 'room_id'")
            if 'name' not in room_data:
                errors.append(f"{room_prefix}Missing required field 'name'")
            
            # Validate descriptions
            descriptions = room_data.get('descriptions', {})
            if not descriptions:
                errors.append(f"{room_prefix}Missing 'descriptions' field")
            elif not any(key in descriptions for key in 
                        ['corporate', 'reality', 'R', 'shifting']):
                errors.append(f"{room_prefix}Descriptions must include corporate/reality or clearance levels")
            
            # Validate exits
            exits = room_data.get('exits', {})
            if not isinstance(exits, dict):
                errors.append(f"{room_prefix}'exits' must be a dictionary")
            
            # Validate clearance
            clearance = room_data.get('clearance', 'R')
            valid_clearances = ['R', 'O', 'Y', 'G', 'B', 'I', 'V', 'UV']
            if clearance not in valid_clearances:
                errors.append(f"{room_prefix}Invalid clearance '{clearance}'")
        
        return errors

# Validation script
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python room_loader.py <room_file.yaml>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    errors = RoomLoader.validate_room_file(filepath)
    
    if errors:
        print("Validation errors found:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("✓ Room file is valid!")
        rooms = RoomLoader.load_room_file(filepath)
        print(f"Loaded {len(rooms)} room(s):")
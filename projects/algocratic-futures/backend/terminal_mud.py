#!/usr/bin/env python3
"""
Terminal MUD - Uses the room system with YAML files
A simple command-line interface for exploring AlgoCratic Futures
"""

import sys
from terminal_integration import terminal
from typing import Optional

class TerminalMUD:
    """Simple terminal interface for the MUD"""
    
    def __init__(self):
        self.player_id = "player1"  # Simple single-player for MVP
        self.running = True
        
    def display_response(self, response: dict):
        """Display a response from the terminal command processor"""
        response_type = response.get('type', 'unknown')
        message = response.get('message', '')
        
        if response_type == 'movement':
            print(f"\n{message}")
            if 'room_description' in response:
                print(f"\n{response['room_description']}")
        elif response_type == 'look':
            print(f"\n{message}")
        elif response_type == 'error':
            print(f"\n! {message}")
        else:
            print(f"\n{message}")
        
        # Show exits if available
        if 'exits' in response and response['exits']:
            print(f"\nExits: {', '.join(response['exits'])}")
    
    def process_input(self, command: str):
        """Process a single command"""
        if command.lower() in ['quit', 'exit', 'q']:
            self.running = False
            print("\nGoodbye, employee. Your productivity has been recorded.")
            return
        
        response = terminal.process_command(self.player_id, command)
        self.display_response(response)
    
    def run(self):
        """Main game loop"""
        print("""
╔═══════════════════════════════════════════════════════════════╗
║           ALGOCRATIC FUTURES - TERMINAL ACCESS                ║
║                                                               ║
║  Welcome to the storm drains. The corporate facade is thin   ║
║  down here. Type 'help' for commands.                        ║
║                                                               ║
║  Employee ID: {self.player_id}                               ║
║  Clearance: PENDING                                           ║
╚═══════════════════════════════════════════════════════════════╝
""")
        
        # Show initial room
        response = terminal.process_command(self.player_id, "look")
        self.display_response(response)
        
        # Main loop
        while self.running:
            try:
                command = input("\n> ").strip()
                if command:
                    self.process_input(command)
            except KeyboardInterrupt:
                print("\n\n[CTRL+C detected. Type 'quit' to exit properly.]")
            except EOFError:
                self.running = False
                print("\n\n[Connection terminated]")

def main():
    """Launch the terminal MUD"""
    mud = TerminalMUD()
    mud.run()

if __name__ == "__main__":
    main()
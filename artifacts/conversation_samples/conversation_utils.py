#!/usr/bin/env python3
"""
Conversation Utilities for CSI Agent Dialogs

This module provides utilities for working with conversation trees in JSON format.
It includes functions for validating, visualizing, and simulating conversations.
"""

import json
import os
import argparse
from typing import Dict, List, Optional, Any


def load_conversation(file_path: str) -> Dict[str, Any]:
    """Load a conversation JSON file and return its contents."""
    try:
        with open(file_path, 'r') as f:
            conversation = json.load(f)
        return conversation
    except Exception as e:
        print(f"Error loading conversation file: {e}")
        return {}


def validate_conversation(conversation: Dict[str, Any]) -> List[str]:
    """Validate a conversation structure and return a list of validation errors."""
    errors = []
    
    # Check required top-level keys
    required_keys = ["conversation_id", "title", "participants", "nodes"]
    for key in required_keys:
        if key not in conversation:
            errors.append(f"Missing required key: {key}")
    
    if "participants" in conversation:
        # Check participants structure
        for i, participant in enumerate(conversation["participants"]):
            if "agent_id" not in participant:
                errors.append(f"Participant {i} missing agent_id")
            if "character_name" not in participant:
                errors.append(f"Participant {i} missing character_name")
    
    if "nodes" in conversation:
        # Check nodes structure and transitions
        node_ids = set()
        for i, node in enumerate(conversation["nodes"]):
            # Check required node keys
            if "node_id" not in node:
                errors.append(f"Node {i} missing node_id")
            else:
                node_ids.add(node["node_id"])
            
            if "speaker" not in node:
                errors.append(f"Node {i} missing speaker")
            
            if "content" not in node:
                errors.append(f"Node {i} missing content")
            
            # Check transitions
            if "transitions" in node:
                for j, transition in enumerate(node["transitions"]):
                    if "target_node" not in transition:
                        errors.append(f"Node {node.get('node_id', i)} transition {j} missing target_node")
                    if "condition" not in transition:
                        errors.append(f"Node {node.get('node_id', i)} transition {j} missing condition")
        
        # Check for transition targets that don't exist
        for node in conversation["nodes"]:
            if "transitions" in node:
                for transition in node["transitions"]:
                    if transition.get("target_node") != "exit" and transition.get("target_node") not in node_ids:
                        errors.append(f"Node {node.get('node_id')} has transition to non-existent node: {transition.get('target_node')}")
    
    return errors


def generate_mermaid(conversation: Dict[str, Any]) -> str:
    """Generate a Mermaid graph representation of the conversation."""
    if not conversation:
        return "graph TD\n    A[Empty Conversation]"
    
    # Create a mapping of agent_id to character_name
    agent_names = {}
    for participant in conversation.get("participants", []):
        agent_id = participant.get("agent_id")
        character_name = participant.get("character_name")
        if agent_id and character_name:
            agent_names[agent_id] = character_name
    
    mermaid = f"graph TD\n    title[{conversation.get('title', 'Conversation')}]\n    style title fill:#f9f,stroke:#333,stroke-width:2px\n"
    
    # Add nodes
    for node in conversation.get("nodes", []):
        node_id = node.get("node_id", "unknown")
        speaker = node.get("speaker", "unknown")
        content = node.get("content", "")
        
        # Truncate content if too long
        if len(content) > 50:
            content = content[:47] + "..."
        
        # Escape quotes and other characters
        content = content.replace("\"", "'").replace("\n", " ")
        
        # Get speaker name
        speaker_name = agent_names.get(speaker, speaker)
        
        mermaid += f"    {node_id}[\"{speaker_name}: {content}\"]\n"
    
    # Add transitions
    for node in conversation.get("nodes", []):
        node_id = node.get("node_id", "unknown")
        
        for transition in node.get("transitions", []):
            target = transition.get("target_node", "unknown")
            condition = transition.get("condition", "always")
            
            if target == "exit":
                mermaid += f"    {node_id} --> |{condition}| exit([Exit])\n"
            else:
                mermaid += f"    {node_id} --> |{condition}| {target}\n"
    
    return mermaid


def simulate_conversation(conversation: Dict[str, Any], start_node: str = "1", auto_respond: bool = False) -> None:
    """Simulate a conversation by navigating through nodes and transitions."""
    if not conversation:
        print("Empty conversation, nothing to simulate.")
        return
    
    # Create node lookup
    nodes = {node["node_id"]: node for node in conversation.get("nodes", [])}
    
    # Get agent names
    agent_names = {}
    for participant in conversation.get("participants", []):
        agent_id = participant.get("agent_id")
        character_name = participant.get("character_name")
        if agent_id and character_name:
            agent_names[agent_id] = character_name
    
    # Start simulation
    print(f"\n=== Simulating: {conversation.get('title', 'Conversation')} ===\n")
    
    current_node_id = start_node
    history = []
    
    while current_node_id != "exit":
        if current_node_id not in nodes:
            print(f"Error: Node {current_node_id} not found. Ending simulation.")
            break
        
        current_node = nodes[current_node_id]
        speaker = current_node.get("speaker", "unknown")
        content = current_node.get("content", "")
        
        # Get speaker name
        speaker_name = agent_names.get(speaker, speaker)
        
        # Print message
        print(f"\n{speaker_name}: {content}\n")
        
        # Store in history
        history.append({
            "node_id": current_node_id,
            "speaker": speaker,
            "content": content
        })
        
        # Handle transitions
        transitions = current_node.get("transitions", [])
        if not transitions:
            print("No transitions available. Ending simulation.")
            break
        
        if len(transitions) == 1 and transitions[0].get("condition") == "always":
            # Automatic transition
            current_node_id = transitions[0].get("target_node", "exit")
        else:
            # User choice
            print("Available transitions:")
            for i, transition in enumerate(transitions):
                condition = transition.get("condition", "unknown")
                target = transition.get("target_node", "unknown")
                description = transition.get("description", "")
                print(f"{i+1}. {description} ({condition} → {target})")
            
            if auto_respond:
                # Automatically select first transition
                choice = 1
                print(f"Auto-selecting option {choice}")
            else:
                # Get user input
                choice = input("\nSelect a transition (or 'q' to quit): ")
                if choice.lower() == 'q':
                    print("Simulation ended by user.")
                    break
                
                try:
                    choice = int(choice)
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue
            
            if 1 <= choice <= len(transitions):
                current_node_id = transitions[choice-1].get("target_node", "exit")
            else:
                print(f"Invalid choice. Please select 1-{len(transitions)}.")
                continue
    
    print("\n=== Simulation Complete ===\n")
    
    # Print conversation summary
    print(f"Conversation had {len(history)} exchanges.")
    
    return history


def export_conversation(conversation: Dict[str, Any], output_format: str = "md") -> str:
    """Export a conversation to a readable format like Markdown."""
    if not conversation:
        return "Empty conversation, nothing to export."
    
    # Get agent names
    agent_names = {}
    for participant in conversation.get("participants", []):
        agent_id = participant.get("agent_id")
        character_name = participant.get("character_name")
        if agent_id and character_name:
            agent_names[agent_id] = character_name
    
    if output_format == "md":
        output = f"# {conversation.get('title', 'Conversation')}\n\n"
        output += f"_{conversation.get('description', '')}_\n\n"
        
        # List participants
        output += "## Participants\n\n"
        for participant in conversation.get("participants", []):
            agent_id = participant.get("agent_id", "unknown")
            character_name = participant.get("character_name", "unknown")
            fork_type = participant.get("fork_type", "unknown")
            output += f"- **{character_name}** ({agent_id}, {fork_type} fork)\n"
        
        output += "\n## Conversation\n\n"
        
        # Create node lookup
        nodes = {node["node_id"]: node for node in conversation.get("nodes", [])}
        
        # Traverse conversation from node 1
        current_node_id = "1"
        visited = set()
        
        def traverse_conversation(node_id, depth=0):
            nonlocal output, visited
            
            if node_id in visited or node_id == "exit" or node_id not in nodes:
                return
            
            visited.add(node_id)
            node = nodes[node_id]
            
            speaker = node.get("speaker", "unknown")
            content = node.get("content", "")
            
            # Get speaker name
            speaker_name = agent_names.get(speaker, speaker)
            
            # Add the message
            output += f"**{speaker_name}**: {content}\n\n"
            
            # Follow first transition
            transitions = node.get("transitions", [])
            if transitions:
                next_node_id = transitions[0].get("target_node", "exit")
                traverse_conversation(next_node_id, depth + 1)
        
        traverse_conversation(current_node_id)
        
        return output
    
    return "Unsupported export format."


def main():
    """Main function to run the conversation utilities from the command line."""
    parser = argparse.ArgumentParser(description="Conversation utilities for CSI agent dialogs.")
    parser.add_argument("action", choices=["validate", "visualize", "simulate", "export"],
                       help="Action to perform on the conversation file")
    parser.add_argument("file", help="Path to the conversation JSON file")
    parser.add_argument("--output", "-o", help="Output file for visualize or export actions")
    parser.add_argument("--auto", "-a", action="store_true", help="Automatically select first transition in simulation")
    
    args = parser.parse_args()
    
    # Load the conversation file
    conversation = load_conversation(args.file)
    
    if not conversation:
        print(f"Failed to load conversation from {args.file}")
        return
    
    # Perform the requested action
    if args.action == "validate":
        errors = validate_conversation(conversation)
        if errors:
            print("Validation errors found:")
            for error in errors:
                print(f"- {error}")
        else:
            print("Conversation is valid!")
    
    elif args.action == "visualize":
        mermaid = generate_mermaid(conversation)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(mermaid)
            print(f"Mermaid diagram saved to {args.output}")
        else:
            print(mermaid)
    
    elif args.action == "simulate":
        simulate_conversation(conversation, auto_respond=args.auto)
    
    elif args.action == "export":
        output = export_conversation(conversation)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Conversation exported to {args.output}")
        else:
            print(output)


if __name__ == "__main__":
    main()
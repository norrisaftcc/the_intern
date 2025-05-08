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


def analyze_conversation(conversation: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze a conversation to extract statistics and patterns."""
    if not conversation:
        return {"error": "Empty conversation, nothing to analyze."}
    
    # Initialize statistics
    stats = {
        "node_count": 0,
        "participant_counts": {},
        "emote_count": 0,
        "branching_nodes": 0,
        "avg_content_length": 0,
        "transitions": {
            "always": 0,
            "user_choice": 0,
            "keyword": 0,
            "other": 0
        },
        "common_emotes": {},
        "path_analysis": {
            "linear_path_length": 0,
            "max_branch_choices": 0,
            "exit_points": 0
        }
    }
    
    # Count participants
    for participant in conversation.get("participants", []):
        agent_id = participant.get("agent_id", "unknown")
        stats["participant_counts"][agent_id] = 0
    
    # Add "user" to participants if not present
    if "user" not in stats["participant_counts"]:
        stats["participant_counts"]["user"] = 0
    
    # Analyze nodes
    total_content_length = 0
    nodes = conversation.get("nodes", [])
    stats["node_count"] = len(nodes)
    
    for node in nodes:
        speaker = node.get("speaker", "unknown")
        content = node.get("content", "")
        
        # Count by speaker
        if speaker in stats["participant_counts"]:
            stats["participant_counts"][speaker] += 1
        else:
            stats["participant_counts"][speaker] = 1
        
        # Analyze content length
        total_content_length += len(content)
        
        # Count emotes using regex pattern [*text*]
        import re
        emotes = re.findall(r'\[\*(.*?)\*\]', content)
        stats["emote_count"] += len(emotes)
        
        # Track specific emotes
        for emote in emotes:
            emote_text = emote.strip().lower()
            if emote_text in stats["common_emotes"]:
                stats["common_emotes"][emote_text] += 1
            else:
                stats["common_emotes"][emote_text] = 1
        
        # Analyze transitions
        transitions = node.get("transitions", [])
        if len(transitions) > 1:
            stats["branching_nodes"] += 1
            stats["path_analysis"]["max_branch_choices"] = max(
                stats["path_analysis"]["max_branch_choices"],
                len(transitions)
            )
        
        for transition in transitions:
            condition = transition.get("condition", "other")
            if condition in stats["transitions"]:
                stats["transitions"][condition] += 1
            else:
                stats["transitions"]["other"] += 1
            
            if transition.get("target_node") == "exit":
                stats["path_analysis"]["exit_points"] += 1
    
    # Calculate averages
    if stats["node_count"] > 0:
        stats["avg_content_length"] = total_content_length / stats["node_count"]
    
    # Find longest linear path
    def find_longest_linear_path(node_id, visited=None):
        if visited is None:
            visited = set()
        
        node_lookup = {node["node_id"]: node for node in conversation.get("nodes", [])}
        
        if node_id in visited or node_id == "exit" or node_id not in node_lookup:
            return 0
        
        visited.add(node_id)
        node = node_lookup[node_id]
        transitions = node.get("transitions", [])
        
        if len(transitions) == 1 and transitions[0].get("condition") == "always":
            next_node_id = transitions[0].get("target_node")
            return 1 + find_longest_linear_path(next_node_id, visited)
        else:
            return 1
    
    stats["path_analysis"]["linear_path_length"] = find_longest_linear_path("1")
    
    # Sort common emotes
    stats["common_emotes"] = dict(
        sorted(stats["common_emotes"].items(), key=lambda x: x[1], reverse=True)[:10]
    )
    
    return stats


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
        
        # Add conversation statistics
        stats = analyze_conversation(conversation)
        output += "\n## Conversation Statistics\n\n"
        output += f"- **Nodes**: {stats['node_count']}\n"
        output += f"- **Branching Points**: {stats['branching_nodes']}\n"
        output += f"- **Emotes Used**: {stats['emote_count']}\n"
        output += f"- **Average Message Length**: {stats['avg_content_length']:.1f} characters\n"
        
        output += "\n### Speaker Distribution\n\n"
        for speaker, count in stats["participant_counts"].items():
            speaker_name = agent_names.get(speaker, speaker)
            output += f"- {speaker_name}: {count} messages\n"
        
        if stats["common_emotes"]:
            output += "\n### Common Emotes\n\n"
            for emote, count in list(stats["common_emotes"].items())[:5]:
                output += f"- \"{emote}\": {count} occurrences\n"
        
        return output
    
    elif output_format == "stats":
        # Return only the statistics in a formatted string
        stats = analyze_conversation(conversation)
        output = f"Statistics for: {conversation.get('title', 'Conversation')}\n\n"
        output += f"Total Nodes: {stats['node_count']}\n"
        output += f"Branching Points: {stats['branching_nodes']}\n"
        output += f"Emotes Used: {stats['emote_count']}\n"
        output += f"Average Message Length: {stats['avg_content_length']:.1f} characters\n\n"
        
        output += "Speaker Distribution:\n"
        for speaker, count in stats["participant_counts"].items():
            speaker_name = agent_names.get(speaker, speaker)
            output += f"- {speaker_name}: {count} messages\n"
        
        return output
    
    return "Unsupported export format."


def main():
    """Main function to run the conversation utilities from the command line."""
    parser = argparse.ArgumentParser(description="Conversation utilities for CSI agent dialogs.")
    parser.add_argument("action", choices=["validate", "visualize", "simulate", "export", "analyze", "compare"],
                       help="Action to perform on the conversation file")
    parser.add_argument("file", help="Path to the conversation JSON file")
    parser.add_argument("--output", "-o", help="Output file for visualize or export actions")
    parser.add_argument("--auto", "-a", action="store_true", help="Automatically select first transition in simulation")
    parser.add_argument("--format", "-f", choices=["json", "text", "md"], default="text", 
                       help="Output format for analysis (default: text)")
    parser.add_argument("--compare-with", "-c", help="Path to another conversation file to compare with")
    
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
        output_format = "md"
        if args.format == "stats":
            output_format = "stats"
            
        output = export_conversation(conversation, output_format)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Conversation exported to {args.output}")
        else:
            print(output)
    
    elif args.action == "analyze":
        stats = analyze_conversation(conversation)
        
        if args.format == "json":
            import json
            output = json.dumps(stats, indent=2)
        elif args.format == "md":
            output = f"# Analysis of {conversation.get('title', 'Conversation')}\n\n"
            output += f"## Basic Statistics\n\n"
            output += f"- **Nodes**: {stats['node_count']}\n"
            output += f"- **Branching Points**: {stats['branching_nodes']}\n"
            output += f"- **Emotes Used**: {stats['emote_count']}\n"
            output += f"- **Average Message Length**: {stats['avg_content_length']:.1f} characters\n"
            output += f"- **Longest Linear Path**: {stats['path_analysis']['linear_path_length']} nodes\n"
            output += f"- **Maximum Branch Choices**: {stats['path_analysis']['max_branch_choices']}\n"
            output += f"- **Exit Points**: {stats['path_analysis']['exit_points']}\n\n"
            
            output += f"## Speaker Distribution\n\n"
            for speaker, count in stats["participant_counts"].items():
                output += f"- **{speaker}**: {count} messages\n"
            
            output += f"\n## Transition Types\n\n"
            for condition, count in stats["transitions"].items():
                output += f"- **{condition}**: {count}\n"
            
            if stats["common_emotes"]:
                output += f"\n## Common Emotes\n\n"
                for emote, count in list(stats["common_emotes"].items())[:5]:
                    output += f"- \"{emote}\": {count} occurrences\n"
        else:  # text format
            output = f"Analysis of: {conversation.get('title', 'Conversation')}\n\n"
            output += f"Basic Statistics:\n"
            output += f"  Nodes: {stats['node_count']}\n"
            output += f"  Branching Points: {stats['branching_nodes']}\n"
            output += f"  Emotes Used: {stats['emote_count']}\n"
            output += f"  Average Message Length: {stats['avg_content_length']:.1f} characters\n"
            output += f"  Longest Linear Path: {stats['path_analysis']['linear_path_length']} nodes\n"
            output += f"  Maximum Branch Choices: {stats['path_analysis']['max_branch_choices']}\n"
            output += f"  Exit Points: {stats['path_analysis']['exit_points']}\n\n"
            
            output += f"Speaker Distribution:\n"
            for speaker, count in stats["participant_counts"].items():
                output += f"  {speaker}: {count} messages\n"
            
            output += f"\nTransition Types:\n"
            for condition, count in stats["transitions"].items():
                output += f"  {condition}: {count}\n"
            
            if stats["common_emotes"]:
                output += f"\nCommon Emotes:\n"
                for emote, count in list(stats["common_emotes"].items())[:5]:
                    output += f"  \"{emote}\": {count} occurrences\n"
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Analysis saved to {args.output}")
        else:
            print(output)
    
    elif args.action == "compare":
        if not args.compare_with:
            print("Error: --compare-with/-c argument is required for compare action")
            return
            
        comparison_conversation = load_conversation(args.compare_with)
        if not comparison_conversation:
            print(f"Failed to load comparison conversation from {args.compare_with}")
            return
            
        stats1 = analyze_conversation(conversation)
        stats2 = analyze_conversation(comparison_conversation)
        
        output = f"Comparison: {conversation.get('title', 'Conversation 1')} vs. {comparison_conversation.get('title', 'Conversation 2')}\n\n"
        
        output += f"Basic Statistics:\n"
        output += f"  Nodes: {stats1['node_count']} vs. {stats2['node_count']}\n"
        output += f"  Branching Points: {stats1['branching_nodes']} vs. {stats2['branching_nodes']}\n"
        output += f"  Emotes Used: {stats1['emote_count']} vs. {stats2['emote_count']}\n"
        output += f"  Average Message Length: {stats1['avg_content_length']:.1f} vs. {stats2['avg_content_length']:.1f} characters\n"
        output += f"  Longest Linear Path: {stats1['path_analysis']['linear_path_length']} vs. {stats2['path_analysis']['linear_path_length']} nodes\n\n"
        
        # Compare common emotes
        common_emotes1 = set(stats1["common_emotes"].keys())
        common_emotes2 = set(stats2["common_emotes"].keys())
        shared_emotes = common_emotes1.intersection(common_emotes2)
        
        if shared_emotes:
            output += f"Shared Emotes:\n"
            for emote in shared_emotes:
                output += f"  \"{emote}\": {stats1['common_emotes'].get(emote, 0)} vs. {stats2['common_emotes'].get(emote, 0)} occurrences\n"
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Comparison saved to {args.output}")
        else:
            print(output)


if __name__ == "__main__":
    main()
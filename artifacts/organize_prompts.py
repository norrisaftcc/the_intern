#!/usr/bin/env python3
"""
Prompt Organization Script for CSI Artifacts

This script organizes the prompt files in the artifacts directory into
a more structured format based on character and prompt type.

Usage:
    python organize_prompts.py
"""

import os
import shutil
import sys
from pathlib import Path

# Define the root directory
ARTIFACTS_DIR = Path(__file__).parent

# Define the target structure
STRUCTURE = {
    "character_prompts": {
        "kai": {
            "alpha": [],
            "beta": [],
            "gamma": []
        },
        "liza": {
            "alpha": [],
            "beta": [],
            "gamma": []
        },
        "wyatt": []
    },
    "world_building": [],
    "meta_prompts": [],
    "emote_patterns": [],
    "examples": {
        "social": [],
        "technical": [],
        "creative": []
    }
}

# Define file mappings (source path -> destination category)
FILE_MAPPINGS = {
    # Kai prompts
    "kai/kaiprompt-knowngood.txt": ("character_prompts/kai/alpha", "kai_alpha_complete.txt"),
    "kai/kai_api_mode.txt": ("character_prompts/kai/beta", "kai_beta_api.txt"),
    "kai/kai_readme.md": ("character_prompts/kai/gamma", "kai_gamma_basic.md"),
    "kai/kai_prompt_sd.txt": ("character_prompts/kai/gamma", "kai_gamma_image_prompt.txt"),
    
    # Liza prompts
    "liza/liza-complete-prompt.md": ("character_prompts/liza/alpha", "liza_alpha_complete.md"),
    "liza/liza_beta2_readme.md": ("character_prompts/liza/beta", "liza_beta_readme.md"),
    "liza/liza-v4-o1-gamma.md": ("character_prompts/liza/gamma", "liza_gamma_social.md"),
    "liza/liza-v3-gamma.md": ("character_prompts/liza/gamma", "liza_gamma_basic.md"),
    "liza/liza-v2-personalitypromptonly.md": ("character_prompts/liza/gamma", "liza_gamma_personality.md"),
    "liza/liza-portrait-prompt.md": ("examples/creative", "liza_portrait_prompt.md"),
    
    # Wyatt prompts
    "liza/wyatt_readme.md": ("character_prompts/wyatt", "wyatt_character_prompt.md"),
    
    # World building
    "csi-lore/csi-lore.md": ("world_building", "csi_fork_taxonomy.md"),
    "csi-lore/csi-lore-orb.md": ("world_building", "csi_orb_lore.md"),
    "the_wiki.md": ("world_building", "csi_wiki.md"),
    
    # Meta prompts
    "_lessons_learned/# chatgpt metaprompts.md": ("meta_prompts", "chatgpt_metaprompts.md"),
    "notion/readme-notion-bot.md": ("meta_prompts", "notion_metaprompt.md"),
    
    # Examples
    "Vi/vi-samples.txt": ("examples/creative", "vi_creative_samples.txt"),
    "pile/#Gamma Checkpoint.md": ("examples/social", "checkpoint_examples.md")
}

def create_directory_structure():
    """Create the new directory structure."""
    for category, subcategories in STRUCTURE.items():
        category_path = ARTIFACTS_DIR / "organized" / category
        category_path.mkdir(parents=True, exist_ok=True)
        
        if isinstance(subcategories, dict):
            for subcategory, subsubcategories in subcategories.items():
                subcategory_path = category_path / subcategory
                subcategory_path.mkdir(parents=True, exist_ok=True)
                
                if isinstance(subsubcategories, list):
                    pass  # Files will be added later
                elif isinstance(subsubcategories, dict):
                    for subsubcategory in subsubcategories:
                        subsubcategory_path = subcategory_path / subsubcategory
                        subsubcategory_path.mkdir(parents=True, exist_ok=True)
        elif isinstance(subcategories, list):
            pass  # Files will be added later

def copy_files():
    """Copy files to their new locations based on mappings."""
    for source_rel, (dest_category, dest_filename) in FILE_MAPPINGS.items():
        source_path = ARTIFACTS_DIR / source_rel
        dest_path = ARTIFACTS_DIR / "organized" / dest_category / dest_filename
        
        if source_path.exists():
            print(f"Copying {source_path.name} to {dest_path}")
            try:
                shutil.copy2(source_path, dest_path)
            except Exception as e:
                print(f"Error copying {source_path}: {e}")
        else:
            print(f"Warning: Source file {source_path} not found")

def create_readme():
    """Create a README file in the organized directory."""
    readme_content = """# Organized CSI Prompts

This directory contains organized prompts from the CSI artifacts collection.

## Structure

- **character_prompts/**: Character-specific prompts
  - **kai/**: Cyberpunk detective character
  - **liza/**: Animation specialist character
  - **wyatt/**: Country-western coding character
- **world_building/**: CSI universe lore and taxonomy
- **meta_prompts/**: Techniques for creating effective prompts
- **emote_patterns/**: Examples of character emote patterns
- **examples/**: Sample prompts by category

## Usage

Each prompt file is named according to its character and fork type (if applicable).
Alpha forks have full capabilities, Beta forks have limited RAG access,
and Gamma forks are personality-only implementations.

Refer to the main PROMPT_CATALOG.md file in the parent directory for more information.
"""
    readme_path = ARTIFACTS_DIR / "organized" / "README.md"
    with open(readme_path, "w") as f:
        f.write(readme_content)

def main():
    """Main function to run the organization process."""
    print("Starting organization of CSI prompts...")
    
    # Create the base directory
    organized_dir = ARTIFACTS_DIR / "organized"
    if organized_dir.exists():
        print(f"Warning: {organized_dir} already exists. Overwrite? (y/n)")
        response = input().lower()
        if response != 'y':
            print("Aborting.")
            sys.exit(0)
        shutil.rmtree(organized_dir)
    
    organized_dir.mkdir(exist_ok=True)
    
    # Create directory structure
    create_directory_structure()
    
    # Copy files
    copy_files()
    
    # Create README
    create_readme()
    
    print("Organization complete. New structure is in the 'organized' directory.")
    print("Please check PROMPT_CATALOG.md for a detailed breakdown of available prompts.")

if __name__ == "__main__":
    main()
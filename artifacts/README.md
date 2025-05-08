# CSI Artifacts Repository

This directory contains various artifacts related to the Creative Solutions Investigation (CSI) project, with a focus on prompts for generating specific behaviors from AI assistants.

## Key Documents

- **[PROMPT_CATALOG.md](PROMPT_CATALOG.md)**: Comprehensive catalog of available prompts organized by character and purpose
- **[CHARACTER_REFERENCE.md](CHARACTER_REFERENCE.md)**: Quick reference cards for the main characters with visual elements and emote examples
- **[organize_prompts.py](organize_prompts.py)**: Script to organize prompts into a structured directory layout

## Main Character Prompts

### Kai "Circuit" Chen
Cyberpunk detective character with programming expertise:
- [kaiprompt-knowngood.txt](/artifacts/kai/kaiprompt-knowngood.txt) - Complete implementation
- [kai_readme.md](/artifacts/kai/kai_readme.md) - Character overview

### Dr. Elizabeth "LIZA" Anderson
Animation and artistic analysis specialist:
- [liza-complete-prompt.md](/artifacts/liza/liza-complete-prompt.md) - Full character profile
- [liza-v4-o1-gamma.md](/artifacts/liza/liza-v4-o1-gamma.md) - Social personality version

### Wyatt "The Repo Wrangler" Brooks
Country-western coding expert:
- [wyatt_readme.md](/artifacts/liza/wyatt_readme.md) - Character description

## World-Building

- [csi-lore.md](/artifacts/csi-lore/csi-lore.md) - Core universe concepts and fork taxonomy
- [csi-lore-orb.md](/artifacts/csi-lore/csi-lore-orb.md) - Additional lore elements

## Meta-Prompting

- [# chatgpt metaprompts.md](/artifacts/_lessons_learned/%23%20chatgpt%20metaprompts.md) - Techniques for effective prompting

## Using These Prompts

1. Choose a character prompt based on your needs (Kai for programming, LIZA for creative/visual, Wyatt for Git/GitHub)
2. Select the appropriate fork type (Alpha for full capability, Beta for limited knowledge, Gamma for personality only)
3. Copy the prompt and customize as needed for your specific use case
4. Test the prompt with different scenarios to ensure consistent behavior

To organize these prompts into a more structured format, run the organization script:

```bash
python organize_prompts.py
```

This will create a new `organized` directory with a clean structure for browsing the prompts.

---

*Note: This repository is continually evolving as new prompt techniques and character developments are added.*
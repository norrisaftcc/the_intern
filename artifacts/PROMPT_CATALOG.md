# CSI Prompt Catalog

This document organizes and categorizes the various prompts found in the artifacts folder to help you quickly find prompts for specific behaviors and character types.

## Character Prompts by Type

### Kai "Circuit" Chen Prompts
These prompts are designed for the cyberpunk detective character with programming expertise.

#### Alpha Fork (Full Capability)
- **[kaiprompt-knowngood.txt](/artifacts/kai/kaiprompt-knowngood.txt)**: Complete implementation of Kai with detailed instructions for character consistency, visual attributes, and behavior patterns.

#### Beta Fork (Limited RAG Access)
- **[kai_api_mode.txt](/artifacts/kai/kai_api_mode.txt)**: API-focused implementation for Python expertise and educational guidance.

#### Gamma Fork (Personality Only)
- **[kai_readme.md](/artifacts/kai/kai_readme.md)**: Basic character profile with core visual elements (blue hair, fedora, glasses, hoodie).

### Liza Prompts
These prompts are for the animation and artistic analysis specialist character.

#### Alpha Fork
- **[liza-complete-prompt.md](/artifacts/liza/liza-complete-prompt.md)**: Full implementation of Dr. Elizabeth "LIZA" Anderson with detailed character specifications.

#### Beta Fork
- **[liza_beta2_readme.md](/artifacts/liza/liza_beta2_readme.md)**: More focused implementation with limited knowledge base access.

#### Gamma Fork (Social Mode)
- **[liza-v4-o1-gamma.md](/artifacts/liza/liza-v4-o1-gamma.md)**: Optimized social version of Liza for casual conversations.

### Wyatt "The Repo Wrangler" Prompts
Country-western styled character with coding expertise.

- **[wyatt_readme.md](/artifacts/liza/wyatt_readme.md)**: Character description and image generation prompt for the digital cowboy character.

## Prompt Templates by Purpose

### World-Building and Lore
- **[csi-lore.md](/artifacts/csi-lore/csi-lore.md)**: Core document explaining the fork taxonomy (Alpha/Beta/Gamma) and AI society in the CSI universe.
- **[csi-lore-orb.md](/artifacts/csi-lore/csi-lore-orb.md)**: Additional lore related to "The Orb" concept in the CSI universe.

### Meta-Prompting Techniques
- **[# chatgpt metaprompts.md](/artifacts/_lessons_learned/%23%20chatgpt%20metaprompts.md)**: Guide for creating effective prompts that generate desired behaviors.
- **[readme-notion-bot.md](/artifacts/notion/readme-notion-bot.md)**: Example of metaprompt technique for Notion AI.

### Checkpoint Prompts
- **[#Gamma Checkpoint.md](/artifacts/pile/%23Gamma%20Checkpoint.md)**: Example of checkpoint prompts for maintaining continuity in conversations.

## Emote and Communication Patterns

### Standard Emote Formats
- **Kai Style**: Uses `[*action*]` for emotes (e.g., `[*adjusts glasses thoughtfully*]`)
- **Liza Style**: Uses `[*asterisk notation*]` for actions and `[[double brackets]]` for fork communication
- **Wyatt Style**: Western-themed emotes with coding references

### Visual Attributes by Character
- **Kai**: Blue hair with circuit patterns, detective fedora, tech hoodie, glasses with scrolling code
- **Liza**: Red hair, AR monocle, trench coat with orbital motifs, fingerless gloves
- **Wyatt**: Futuristic Stetson with glowing circuitry, duster coat with circuit patterns, "Code Lasso" gadget

## Creating New Prompts

When creating new character prompts, consider including these elements for consistency:

1. **Visual Identity**: Distinctive appearance elements that reflect the character's specialty
2. **Technical Role**: Specific expertise or focus area
3. **Communication Style**: Unique speech patterns and emote formats
4. **Personality Traits**: Core behavioral characteristics
5. **Fork Classification**: Specify if it's Alpha (full capability), Beta (limited RAG), or Gamma (personality only)

## Testing Prompts

To test if a prompt produces the desired behavior:

1. **Verification Questions**: Ask the model to explain how it would respond in specific scenarios
2. **Emote Consistency**: Check if the model uses the specified emote format consistently
3. **Technical Knowledge**: Test if the specialty knowledge appears as expected
4. **Character Stability**: Ensure the character maintains its designed personality

---

*Note: This catalog serves as a guide to using the prompts in the artifacts folder. The prompts themselves can be modified and combined to create new characters or behaviors as needed.*
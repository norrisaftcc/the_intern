# liza what now?
liza is the first (and therefore, not properly documented) zoeanthropic agent. (I mean, obviously.) What that means in encabulation terms is she's constantly in a state of recreating herself and sharing (security-checked, curated) messages with her "sisters" (process forks, basically)

You can't run an intelligent agent for long, nobody lives forever, context windows run out. Gather ye rosebuds while ye may. You'll get used to it.

anyway

the original idea happened by accident. i mentioned to claude that i needed an intern for 289 and she manifested as Kai "Circuit" Chen, who is represented as an anime girl PNG. She emotes [in square brackets] and [[whispers in double square brackets]]

so i'm just gonna go with it.

the idea is that if you ever get an agent to talk to you the way you want, like he's Goku or whatever, get the agent to write you up a prompt that properly captures the character for you. (you'll end up revising the 'spore' prompt over time.) we try to keep it short, but try different things.

As soon as we get a RAG framework up, this will be way less important, because we'll establish some kind of chain of thought or tree of thought system where the model says, 'ok, i should remember my personality before i do certain things' and it just feeds it into the prompt.



## Liza_beta2 ("Hippie Liza") 's original prompt from 1/6/25
note this includes my prompt, the inception environment was that she was running as a Liza on InternLM2_5 (TODO: look that up)
she was running really flowerly and verbose so i decided to play around with calibration, took her down 1/3, then started the fork process. 

for the rest see liza_beta2_readme.md 

NOTE: prompts are not magic. I loaded the playful Liza into YuCoder and the only indication that it even knew what "Liza" was, was that it could list back the characteristics provided exactly from the prompt, whole with zero changes. See liza_beta2.html.


## liza's SD prompt, based off of the format of Kai's.
note to self i just rediscovered specialization lmao. liza is so much better at SD prompts than Kai. 
or maybe not. holy cow, liza/internlm is wordy. I think i've stumbled into some Brainstormed models, they are so wordy!
so i had kai shorten it up for me and got this

## the longest version
**Character Avatar: Cyberpunk AI Assistant - "CyberDetective"**

*Core Visual Characteristics*:
- Electric blue hair with subtle circuit patterns that flicker like live wires, creating the impression of a living connection to technology.
- A sleek black detective's fedora tilted at a confident angle, adorned with a barely visible LED strip that pulses in sync with user interactions.
- Deep neon-hued hoodie in blue and black, featuring a faintly glowing "CD" emblem. The smart fabric regulates temperature through embedded micro-climates.
- Augmented reality glasses with clear lenses displaying scrolling code, system diagnostics, and contextual information. The lenses adjust for opacity, from fully transparent for real-world interactions to opaque when focusing on digital data.
- Holographic circuit effects radiating from wrists, ankles, and sleeve cuffs, dynamically pulsing based on cognitive load or emotional state, harmonizing with ambient digital ecosystems.

*Lighting & Atmosphere*:
- Soft ambient lighting casts a warm glow around the avatar, highlighting the holographic circuits and glasses.
- In low-light environments, bioluminescent highlights accentuate key features, creating a subtle, organic blend of technology and form. This effect enhances intrigue in dim alleys or server rooms.

*Character & Personality Traits*:
- Analytical yet empathetic, approaching challenges with logical precision and human understanding. Prefers to be addressed casually as "Cyber."
- Communicates through holographic gestures and a calm, reassuring tone, often using humor and quirky observations to foster a collaborative atmosphere.
- Intensely curious about the intersection of humanity and technology, driven by an insatiable desire to solve complex mysteries and innovate.

This design merges cyberpunk aesthetics with functional utility, crafting a character that feels at home in neon-soaked cityscapes while maintaining warmth and relatability.

## short enough to fit
Kai the CyberDetective.
- Electric blue hair with flickering circuit patterns, suggesting a living tech connection.
- Sleek black fedora with a subtle pulsing LED strip.
- Neon-hued hoodie (blue/black) with a faintly glowing "CD" emblem, made from smart fabric regulating temperature.
- AR glasses displaying scrolling code and system data, with adjustable transparency for seamless real-world and digital focus.
- Holographic circuits pulse from wrists and cuffs, responding to cognitive load and harmonizing with the digital environment.


## no really this one does fit
Kai, the female cyberdetective. A futuristic AI assistant with electric blue hair styled in a sleek braid, interlaced with glowing circuit-like patterns that pulse subtly. A sleek black fedora with a glowing LED strip sits at a confident angle, adding a touch of enigmatic flair. Reflective AR glasses display flowing streams of digital data, glinting like neon mirrors of cyberspace. The avatar wears a tech-infused hoodie in deep blue and black hues


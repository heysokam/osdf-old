# Open Source defrag's mod code

## Goals:
### Code & License:
- Respect FOSS philosophy. Open source and community focus.
- Eliminate all traces of q3a-sdk licensing constraints.
- Rewrite the code 1:1, with the aid of reverse-engineered code only where strictly necessary.
- Community based, where anyone can become a contributor.

### Gameplay:
- Maintain gameplay 1:1.
- Achieve compatibility with existing maps. Avoid requiring any form of map porting for existing content.
- Community collaboration in bug-fixing and further development of the mod.

## Reference Repositories
## Base:
- ioquake3: https://github.com/ioquake/ioq3.git  
Base development starting point (q3e has no gpl gamecode)

- Q3Arena 1.32b GPL release:  https://github.com/id-Software/Quake-III-Arena.git  
Base Gameplay code (ioq3 has gameplay modifications)

- Lumia's Momentum Mod GPL codebase: https://github.com/chovelyoukai/defragmmod  
Most accurate non-id3-engine implementation to date

- oDFe: https://github.com/JBustos22/oDFe.git
Base engine that was forked to start osdf-engine

## Helper:
Repositories that can aid in the success of this project:
- Existing reverse engineering effort: https://github.com/krsh732/DF_Reverse_Stuff
- Q3vm disassembler: https://github.com/brugal/q3vm 
- Existing OpenDF attempt, based on OpenArena: https://github.com/oitzujoey/opendf
- Existing CPM gameplay implementation: https://github.com/rdntcntrl/ratoa_gamecode.git

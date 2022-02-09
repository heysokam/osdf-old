# Open Source defrag's mod code

## Goals:
### Code & License:
- Respect FOSS philosophy. Open source and community focus.
- Eliminate all traces of q3a-sdk licensing constraints.
- Either reverse-engineer or rewrite the code.
- Community based, where anyone can become a contributor.

### Gameplay:
- Maintain gameplay 1:1. The code is not accessible, but can be reverse-engineered or rewritten.
- Achieve compatibility with existing maps. Avoid requiring any form of map porting as much as possible.
- Community collaboration in bug-fixing and further development of the mod.

## Reference Repositories
## Base:
- ioquake3: https://github.com/ioquake/ioq3.git  
Base development starting point (q3e has no gpl qvm creation utilities)

- Q3Arena 1.32b GPL release:  https://github.com/id-Software/Quake-III-Arena.git  
Base Gameplay code (ioq3 has gameplay modifications)

- Lumia's Momentum Mod GPL codebase: https://github.com/chovelyoukai/defragmmod  
Most accurate non-id3-engine implementation to date

- oDFe: https://github.com/JBustos22/oDFe.git
Preferred engine to run binaries.  

## Helper:
Repositories that can aid in the success of this project:
- Existing reverse engineering effort: https://github.com/krsh732/DF_Reverse_Stuff
- Q3vm disassembler: https://github.com/brugal/q3vm 
- Existing OpenDF attempt, based on OpenArena: https://github.com/oitzujoey/opendf
- Existing CPM gameplay implementation: https://github.com/rdntcntrl/ratoa_gamecode.git
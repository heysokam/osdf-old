# How to code:
  - Make gamecode modifications in ioq3
  - Compile with their qvm makefile
  - Place the files in a compiled q3e folder to start the mod
_This mod makes no modification to the engine itself._  
_It only modifies gamecode._

# ioq3 Gamecode: 
  (supposedly) contains modifications to vanilla gameplay    #TODO: confirm this
  Gamecode Folders: cgame, game, q3_ui

# q3e engine:
  ?? no modifications needed (in theory)


# Licensing things:  
The goal of this project is to release defrag from its closed source constraints.  
This mod contains no trace of q3a-sdk license, and aims to remain that way forever.  

## Rewrite or Reverse engineer?  


# Is this defrag?  
Yes  
# No, but really, is this defrag?  
Well, no... but also, in a way, yes.  
Let me explain:  

Goals:
- Respect FOSS philosophy. Open source and community focus.
- Community based, where anyone can contribute.
- Avoid defrag branding where possible, to stop controversy.  
- Maintain gameplay 1:1. The code is not accessible, but can be reverse-engineered.
- Achieve compatibility with existing maps. Avoid requiring any form of map porting.

## Extra info:
Donald: if you want to stick it to the man, why not start a public reverse engineering project of defrag?
lex: https://github.com/krsh732/DF_Reverse_Stuff
Donald: that's a very good start, but i think it needs to be more strict: the OOT64 and Diablo (2?) reverse engineering projects went through the rom function by function, and kept track of exactly which functions compiled and which were cleaned up etc.
For a project like this to get off the ground, i think the scope of it needs to be clear and trackable
This disassembler already goes function by function, so it would be a matter of bringing this info to the repository
https://github.com/brugal/q3vm 


AM: with all the motivation of people here we can just rewrite defrag from scratch
Donald: with rewriting from scratch you risk invalidating all records(
lex: the great revolution, abolish the old order. honestly, whichever we go, either rewriting or reverse - it will be better than not doing it



sOkam!: For the rewrite version:
I have a codebase that works fairly accurately (made by Lumia, in Momentum Mod, and his code is open source) that is made also in C
As a starting point, it would be a matter of creating a new q3mod, and adding that codebase to it
With that code, and the reverse repository, an accurate rewrite doesn't sound too crazy

I already tried it, and compiled the engine, but don't know if a mod should be distributed as dll and, therefore, the code structured in a different way, or if that's actually fine and the expected way to do it 
(so little info, and what's there is old af)
If anyone here has exp compiling mods, plz dm

AM: qvm is preferable, as universal
AM: found some https://github.com/oitzujoey/opendf while searching for reimplementation attempt by slick
sOkam!: oh that's a great deal of work already figured out. tysm!



AM: also qvm to not deal with precision variations caused by compiler/params choice

sOkam!: doesn't defrag already distribute as engine anyway, and therefore is subject to the mentioned variations? 
Aciz: the engines just run the mod, and mod is what determines how physics and what not run

AM: engine still affects some calculations, but main part is in mod ofc
was noticed in couple of cases: steep ramps top interaction, wallbugs, slick flush with the surface
this is when changes were introduced w/o changing anything explicitly
original engine was built with fast math preset, which induced double precision in some calculations
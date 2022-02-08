# Compile & code:
  - Make gamecode modifications in ioq3  
  - Compile with their qvm makefile (root/compile.py will do this)  
  - Place the files in a compiled q3e folder to start the mod (root/compile.py will do this)  
_This mod makes no modification to the engine itself._  
_It only modifies gamecode._  

# Gamecode (ioq3/q3a): 
  Gamecode Folders: cgame, game, q3_ui  
  ioq3 (supposedly) contains modifications to vanilla gameplay    #TODO: confirm this  

# q3e engine:
  ?? no modifications needed (in theory)  

# Compile Settings:
if you go in ioq3 and run `make BUILD_CLIENT=0 BUILD_SERVER=0 BUILD_GAME_SO=0`, this will build qvm tools + qvms only

# Rewrite or Reverse engineer?  

# Guide
Start from ioquake3 repo.

The mod code is in:
- code/game  
- code/cgame  
- code/q3_ui (baseq3)
- code/ui (Team Arena)  
- code/qcommon/q_shared.*
- code/qcommon/q_math.*.
- The code/qcommon/q_* files are code/game/q_* in the Q3 SDK.

Disable building the ioquake3 server and client executable using `make BUILD_SERVER=0 BUILD_CLIENT=0` (or setting those in Makefile).  
The ioquake3 Makefile also has the benefit of building mod DLLs using gcc or clang which have better error messages and can be used with a debugger (gdb, lldb).

By default QVMs built using ioquake3 Makefile cannot run on the original Quake 3 engine (due to slightly modified QVM format). To run on original Quake 3 (and ioquake3) you need to pass -vq3 (vanilla q3) to $(Q3ASM) in Makefile when linking QVMs.

The mod code from ioquake3 has additional bug fixes and improvements over the original Quake 3 1.32, licensed under the GPL which is needed for standalone games, and allows using code from other GPL games/mods. 
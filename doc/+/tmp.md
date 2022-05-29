# TODO:
- Figure out if there is a way to extract QVM compiling tools from ioq3, to become independent from its code.

# Compile & code:
  - Make gamecode modifications in ioq3  
  - Compile with their qvm makefile (root/compile.py will do this)  
  - Place the files in a compiled q3e folder to start the mod (root/compile.py will do this)  
_This mod makes no modification to the engine itself._  
_It only modifies gamecode._  

# Gamecode (ioq3/q3a): 
  Gamecode Folders: cgame, game, q3_ui  
  ioq3 (supposedly) contains modifications to vanilla gameplay    #TODO: confirm this  

# oDFe engine:
  ?? no modifications needed (in theory)  

# Compile Settings:
if you go in ioq3 and run `make BUILD_CLIENT=0 BUILD_SERVER=0 BUILD_GAME_SO=0`, this will build qvm tools + qvms only


# QVM verification
`fs_debug 1`
`\which vm/filename.qvm`
Only if said module is currently running
The game qvm isn't running with local client connected to a remote server,  
and cgame qvm isn't running if at main menu

# DearIMGUI:
To add DearIMGUI:  
## QVM:
Files:    q3_ui/ui_main.c  
Makefile vars: CLIENT_CFLAGS, CLIENT_LIBS
Cannot modify expected structure
## Engine:
Files:    code/client/cl_ui.c
Make:     ??
Connect it with a check for what type of ui to use.


# QVM tools only
QVM toolchain: lcc, rcc, q3asm

G: if you go in ioq3 and run make BUILD_CLIENT=0 BUILD_SERVER=0 BUILD_GAME_SO=0, this will build qvm tools + qvms only
sOkam!: could i get gamecode directly from gpl vanilla, and make it work by compiling in whatever engine?
G: yes. you don't compile in an engine
f: you don't need any engine to comile qvms. only qvm toolchain - lcc, rcc, q3asm. engine only runs qvms
G: you compile qvms first, then can run your .qvm files in any engine.  eg. ~/.q3a/baseq3/vm/cgame.qvm (edited)
by doing this. and when you run q3e/etc, the engine will load them

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

# Per folder Information
Each folder can contain a file explaining what the contents of that folder are  
This is not strict or mandatory, but recommended for intuitiveness when analyzing the project.
Think of it as "Is this folder's structure or content intuitive to understand? No? Then write an info file in that folder, to help other people navigate it."

# Separate folders appropriately


---

# Default Folders
root    # This repository's root folder. Where all other dirs are stored  
bin     # Where the compiled binaries will be output  
doc     # Project documentation files  
src     # Source code of the project  
ref     # Reference code and other important information  

---

# src Subfolders
cfg     # Default configuration files for the mod.  
engine  # Stores a fork of oDFe, to support further development of the osdf project.  
game    # Contains a modified version of ioquake3's gamecode, used as a base for the mod.  
condump # For storing important quake console dumps  
pseudo  # Pseudocode/algorithms, for work in progress features  
lib     # Libraries required for the scripts stored in the root of this folder  

---

# engine Subfolders
Contains only the necessary files for the engine to be compiled, -without- any gamecode.  
botlib   # AI related code
cgame    # Client game code
client   # Client engine code
dep      # Deprecated code from oDFe before forking
lib      # Engine libraries
qcommon  # Various engine utility, common to engine/game
rendc    # Code common to all renderers
rend1    # Opengl1 renderer
rend2    # OpenGL2 renderer
rendv    # Vulkan renderer
sdl      # SDL related code
server   # Server engine code
sgame    # Server and shared gamecode
ui       # UI specific code (actually "gamecode")
unix     # Unix platform specific code
win32    # Windows platform specific code

# game Subfolders
Only listing the ones that are unique to the game folder
ui       # Contains the reworked UI code
ui_q3    # Original q3ui code (osdf main menu)
ui_ta    # Original teamarena code

# New Code folders
## src/game/sgame/phy
Contains all code related to the movement physics.  
All of this code happens inside a single `Pmove()` instance, and starts with `phy_PmoveSingle()` inside `bg_pmove.c`.  
This is very different to every other defrag mod, that has all of the physics integrated into one single code flow.  

This change started to preserve vq3 and cpm from being affected by bugs in the new physics, but turned out to be extremely useful for the other physics too, because they make the code much cleaner to navigate, and much easier to reason about.  
Instead of having some gigantic functions full of edge cases that don't apply to what you are looking for, you just follow the code into the correct function and read whats in front of you.  

The goal of this `Pmove()` hook is to move the code flow completely outside of the `bg_pmove.c` file, which was already 2500 lines before adding any defrag specific code, and really hard to navigate.   
_(to give some perspective: At some point, the file got up to 5k lines, and that was early dev with just cpm/vq3)_

Each physics has its own separate flow, and should be kept separate to ensure that bugs don't bleed from one physics into the other.  
Each of those flows are also kept in their own separate files, unless they use the exact same code from other files. In which case they just call for those functions instead.  
See `*/phy/vq1.c` or `*/phy/vq4.c` for codeflow examples that are completely different to q3a in almost every function  
See `*/phy/vjk.c` for a codeflow that follows q3a almost entirely, except for a couple of exceptions  

## src/game/cgame Subfolders
hud       # Code related to the ingame hud. It only has strafehud code, but eventually should contain everything else
qvm       # Deprecated qvm specific files. Disconnected from the buildsystem
teamarena # Deprecated teamarena specific code. Disconnected from the buildsystem

## src/game/ui Subfolders
Contains code related to the new ui framework.  
It is currently compiled on demand, and not included by default.  

The structure tries to modularize the framework, within the limitations of C.  
As such, C code files are stored in subfolders named `*/c/`, while their roots contain a header file for each of the "modules" contained within that `*/c/` subfolder.

This results in structures like:
```
Folder with two modules:   main and callbacks
*/ui/c/main.c       <--- UI Main implementation
*/ui/c/callbacks.c  <--- Callback implementation
*/ui/main.h         <--- Declarations of methods accesible from outside main.c
*/ui/callbacks.h    <--- Declarations of methods accessible from outside callbacks.c

Folder with one module:   elements
*/ui/framework/c/action.c    <-- Action element implementation code
*/ui/framework/c/cursor.c    <-- Cursor element implementation code
*/ui/framework/c/radiobtn.c  <-- Radio Button element implementation code
*/ui/framework/elements.h    <-- Declarations of accesible methods for all elements
```

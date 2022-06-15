# Cloning
This repository doesn't contain game or engine code itself.  
Remember that you need to clone this repo AND all submodules contained in it.  
```bash
git clone --recurse-submodules -j8 THELINK
```

# System Requirements
SCons (min version unknown, 4.3.0 tested and works)  
Python 3.10 minimum _Read: PEP604_  
mingw-w64 (for cross compilation from linux to windows)  

## Libraries (either linux or mingw-w64 versions):
```
# Global
libpcre, libsdl2, libcurl, libjpeg
m

# Windows
wsock32, gdi32, winmm, ole32, ws2_32, psapi, comctl32
wldap32, crypt32   # Curl support libs

# Linux
dl
```

# Build Instructions (simplified)
```bash
cd REPO/src
scons KEYWORD
```
Common Keywords:
```
debug   release   game   game-dist
```

# Build Instructions (explanation)
For any command that runs with `scons` directly, you will need to first change folder to:  
```bash
cd REPO/src  
```
The buildsystem can be configured by adding a `REPO/src/scons_local.py` file, so that you don't lose your local config during repository updates.

There is a skeleton file at `REPO/src/lib/skel/scons_local.py`. You can copy/paste that, and go from there. Or start a new empty file, and add those things you need.

Read the top of the file `REPO/src/SConstruct` for a detailed description of the buildsystem naming scheme, and how its supposed to be used.

## From Linux
```bash
scons KEYWORD  # See scons -h for options
```

### From: Linux. For: Linux
```bash
scons
```
Builds every target listed build_default=[].  
See `REPO/src/lib/helper/config_scons.py` for the default options that will be built.  
If the list is modified to empty (see scons_local.py) then it will build as if `debug` keyword was used.  

```bash
# Defaults to "Current system only (aka Linux)"
scons release # Builds release version of the engine and gamecode
scons engine  # Builds release version of the engine
scons game    # Builds release version of the gamecode
```

### From: Linux. For: Windows
_Temporary solution, until `platform=` is implemented_  
_It will build both windows AND linux versions, but its reliable to cross-compile_  
```bash
scons distribute    # engine and gamecode
scons game-dist     # gamecode only
scons engine-dist   # engine only
```
**Note: MinGW cross-compilation for Windows, from Linux**  
The old buildsystem used static linking, but we are linking dynamically instead  
_(as it is explicitely recommended by the developers of many of the used libraries. eg: sdl2)_.  

If you are cross compiling, you will need mingw-w64 versions of the required libraries installed and accessible by mingw.  
And they don't exist pre-packed in some distros, so be mindful of that when choosing where to build from.  
Installing and compiling with mingw-w64 in some distros is not an easy process (not looking at you, Ubuntu / WSL), and this buildsystem cannot possibly handle and automate the installation of all of that for you.  
If you require cross-compilation like this from your distro, Google will be your friend.  

### Debug build
```
# Defaults to "Current system only (aka Linux)"
scons debug         # Builds debug version of both engine and gamecode
scons engine-dbg    # Builds debug version of the engine only
scons game-dbg      # Builds debug version of the gamecode only
```

## From Windows
_(To be done)_  
The current buildsystem doesn't have support for compilation from windows.  

MSYS: To be done  
Cygwin: Unknown territory  
WSL: Will never be supported. SCons behaves really weird inside WSL (and ubuntu in general).  

# Automation helper (Bash only)
_TODO: Documentation._  
_For now, read the file comments to understand what it does._  
```bash
nim REPO/src/build.nims
```
Requires Nim _(install with choosenim, for your sanity)_  

Only useful when you want to **automate** local installation or distribution of the mod.  
It can be called with different switches, to control what it does.  
Currently supports bash only, since it depends on general bash tools to do some of its operations  
_(see REPO/src/lib/helper/bash.nim to see what bash commands are required exactly)_

TL;DR: It's a bash script, with much better syntax, that allows:
```md
- Calling the buildsystem from any folder, without needing to cd
- Installing the built files into a desired local folder
- Downloading the latest curl and sdl windows libraries for distribution
- Building both engine and game for all supported platforms
- Packing the necessary files into a user-facing `.zip` file, that they can just extract and play
  - Handles revision numbers of the zip file
  - Packs all cfg files
  - Packs the engine and game binaries for all platforms
```

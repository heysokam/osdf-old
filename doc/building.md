# Cloning
This repository doesn't contain game or engine code itself.  
Remember that you need to clone this repo AND the submodules contained in it.  
```bash
git clone --recurse-submodules THELINK
```

# System Requirements
SCons       : min version is unknown _4.3.0 tested and works_  
Python      : 3.10 minimum _Read: PEP604_  
mingw-w64   : compilation for windows (either native windows, or linux-to-windows)  

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

# General Build Instructions
## Simplified
```bash
cd REPO/src
scons KEYWORD
```
Common Keywords:
```
release   game   game-dist   debug   
```

## Explanation
### Building
For any command that runs with `scons` directly, you will need to first change folder to:  
```bash
cd REPO/src  
```
For building only the default targets:
```bash
scons
```
Builds every target listed build_default=[].  
See customization for more info.

The buildsystem can be controlled further with several CLI options:
**Keywords:**
```bash
scons KEYWORD  # See scons -h for options
```
The most commonly used are:
```bash
scons release # Builds release version of the engine and gamecode
scons engine  # Builds release version of the engine
scons game    # Builds release version of the gamecode
```
They default to building for the current system only (platform & architecture).

### Customization
The buildsystem can be configured by adding a `REPO/src/scons_local.py` file, so that you don't lose your local config during repository updates.

There is a skeleton file at `REPO/src/lib/skel/scons_local.py`. You can copy/paste that, and go from there. Or start a new empty file, and add the variables that you need.

Read the top of the file `REPO/src/SConstruct` for a detailed description of the buildsystem naming scheme, and how its supposed to be used.

#### Default targets
See `REPO/src/lib/helper/config_scons.py` for the default options that will be built.  
If the list is modified to empty (see scons_local.py) then it will build as if `debug` keyword was used.  


## From Linux
### Linux-to-Linux
See general instructions for building.
You will need to have installed the development version of the libraries listed in the dependencies section.

### Linux-to-Windows
_Temporary solution, until `platform=` is implemented_  
_It will build both windows AND linux versions, but its reliable to cross-compile_  
```bash
scons distribute    # engine and gamecode
scons game-dist     # gamecode only
scons engine-dist   # engine only
```

The old buildsystem used static linking, but we are linking dynamically instead  
_(as it is explicitely recommended by the developers of many of the used libraries. eg: sdl2)_.  
You will need mingw-w64 versions of the required libraries installed and accessible by mingw.  

#### From Arch-based distros
_(must be AUR compatible)_
Install `mingw-w64`
Install the `mingw-w64` versions of the libraries needed from AUR:
```bash
mingw-w64-sdl2, mingw-w64-curl, mingw-w64-libjpeg, mingw-w64-pcre 
```

#### From other distros
Compiling is possible from any distro, as long as you figure out how to install the full mingw-w64 toolchain, including the required dependencies.  

Some of the required libraries don't exist pre-packed in some distros, for usage by mingw-w64.  
Be mindful of that when you choose where to build from.  

Installing and compiling with mingw-w64 in some distros is not an easy process (not looking at you, Ubuntu / WSL).  
This buildsystem cannot possibly handle and automate the installation of all of that for you.  
If you require cross-compilation, your distro's package manager and Google will be your friends.  

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

### Native:
_(tested on powershell)_
#### Install Python 3.10+:  
Double check that `py` manager is being marked for installation.  

#### Install SCons:
Check what default version of python that your system is using.  
```bash
python --version
```
Only use this if your default python version is 3.10+ or over.  
You will likely need to uninstall if its not.  
```bash
pip install scons
```
If your default python version is not 3.10+, then do:  
```bash
py --list                       # To check that you in fact have a 3.10 or superior version installed
py -3.10 -m pip install scons   # Change the `-3.10` part with whatever version your system gives you, but it must be 3.10 minimum
```
If you only ended up with one SCons version installed:
: Use `scons` normally from now own.

If you ended with more than one SCons version installed:
: Uninstall all the incorrect versions
: ... or always use `py -3.10 -m scons` (or whatever version) everytime you run the buildsystem

#### Install chocolatey:
Download from their website, follow instructions

#### Install mingw with chocolatey:
```bash
choco install mingw
```

#### To build
See general build instructions

### MSYS
_To be done_  
(2022.06.16) Issues + log (msys2):  
- Current maximum python version in msys repositories is 3.9, but we require 3.10 (PEP604). Will need to wait  
- libjpeg is not in msys repositories, so would need to be compiled static  
- libpcre is in msys repositories, but didn't figure out how to install it (package `mingw-w64-pcre` wasn't found, but its listed in the web)  
- libsdl2 is in msys repositories. Didn't try to install  
- libcurl installed correctly. Will probably need libcurl-devel  

### Cygwin
**Unknown territory**  
Possibly worse than MSYS2 (due to mingw-w64 libraries) maybe? But completely unknown  

### WSL
**Will not be supported**  
Ubuntu doesn't have pre-packed support for any of the required cross-compilation libraries, and sometimes not even mingw-w64  
This renders the distro almost useless for cross-compilation from-WSL-to-win.  
Native from-ubuntu-for-linux(WSL):   _(just for clarification)_ 
The libraries exist, should work, but not recommended and untested.  
Remember that running software from within WSL, for the host Windows, performs very poorly.  

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
_(see REPO/src/lib/helper/bash.nim to see exactly which bash commands are required to run)_

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

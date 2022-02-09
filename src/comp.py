# Module-only guard
#   This script should be used as an import module.
#   Exit if script is not imported as such:
if __name__ == "__main__": exit("ERR:: This script is not meant to be executed independently")
# :::::::::::::::::


# Imports
import cfg          # Script Configuration
import bash         # Bash helper functions

# Compiling
## QVM
##   Creates OS independent bytecode, that can be then run by any engine that supports it (ioq3/q3a have different qvm versions)
#Syntax# 
#  make BUILD_CLIENT=0 BUILD_SERVER=0 BUILD_GAME_SO=0 BUILD_DIR=../../bin BASEGAME=osdf
makeQVM= "make BUILD_CLIENT=0 BUILD_SERVER=0 BUILD_GAME_SO=0"+space+"BUILD_DIR="+binDir +space+"BASEGAME="+modName # Make only QVM-game and QVM-tools

def compileQVM():
    bash(makeQVM)

# Distribution
## Pack source code copy
def packSource(outDir, outFile):
    pass

## Pack QVM  
def packQVM(outDir, outFile):
    pass

## Pack Mod
def packMod(outDir, outFile):
    pass

### Compile Engine syntax
makeWin32= "make PLATFORM=mingw32 ARCH=x86"      # To win32
makeWin64= "make PLATFORM=mingw32 ARCH=x86_64"   # To win64
make32= ""
make64= ""
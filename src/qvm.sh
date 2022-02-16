#!/bin/bash

# Configuration
## Mod
versionNumber="0.0.1"
modname="osdf"
fullname="opensource-defrag"

## Folders Configuration
basepath="/app/vg/os-defrag" # installation folder
# code folders
releasesDir="../bin/releases"
devRoot="$HOME/gd/osdf"
srcRoot="$devRoot/src"
srcDir="$srcRoot/osdf-ioq3"
cfgDir="$srcRoot/cfg"
# bin output
binDir="$devRoot/bin"
compileDir="$binDir/release-linux-x86_64"  # set by the compiler (makefile)
bkpDir="$binDir/vm-bkp"
vmFile="vm"   # without extension
PK3file="$compileDir/$modname/$vmFile.pk3"  # created by the make block of this script

# ::::::::::::::::::::
# Helper code
## Aliases
alias cp="cp -v"
alias mv="mv -v"
alias md="mkdir -v"
alias zip="zip -v"
alias echo="echo -e"
startFolder="$(pwd)"
## Functions
hold() {
  while [[ true ]]; do 
    echo -e "]] Script ended. Press any key to exit."; 
    read -r -n 1; done; }
quit() { 
  echo -e "$1";
  notify-send "$1"
  if [[ -v HOLD ]]; then
    hold; exit
  else exit; fi; }
## Bash options
shopt -s nullglob # Make empty results not output a '*' character. With this, they return "" (empty/null)
if [[ -v DBG ]] && [[ -v NOOP ]]; then
  echo "DBG + NOOP mode: Active"
  PS4='+ Line ${LINENO}: ${BASH_COMMAND} => '
  set -vxn
elif [[ -v DBG ]]; then
  echo "DBG mode: Active"
  PS4='+ Line ${LINENO}: ${BASH_COMMAND} => '
  set -vx # Verbose + Xtrace mode for debugging. TMI for regular use.
elif [[ -v NOOP ]]; then
  echo "NOOP mode: Active"
  PS4='+ Line ${LINENO}: ${BASH_COMMAND} => '
  set -vn
fi
# ::::::::::::::::::::


# ::::::::::::::::::::
# Make
# ::::::::::::::::::::
# Enter ioq3 folder
cd "$srcDir" || quit "ERR:: Failed to enter $srcDir" && echo ":: Entered folder: $(pwd)"
# Make qvm
#make BUILD_CLIENT=0 BUILD_SERVER=0 BUILD_GAME_SO=0 BUILD_DIR=$binDir BASEGAME=$modname
make

# Enter qvm compile target folder
cd "$compileDir"/$modname || quit "ERR:: Failed to enter $compileDir/$modname" && echo ":: Entered folder: $(pwd)"

# Zip qvm files with .pk3 extension
targetFile=$vmFile.pk3
zip -r $targetFile vm && echo ":: Created file: $(pwd)/$targetFile"

# Copy .pk3 to vm.bkp, with version control
cp -u --backup=t $targetFile "$bkpDir"/$targetFile 
echo -e "\n:: Created $targetFile backup file inside $bkpDir"

# Avoid installing when called with "make" option
if [ "$1" = "make" ]; then
quit ":: QVM made, but not installed or packed.";
fi


# ::::::::::::::::::::
# Install 
# ::::::::::::::::::::
#  This is not executed when calling with "make" argument.
origin="$compileDir/$modname/$targetFile"
target="$basepath/$modname/$targetFile"
cp -u "$origin" "$target" || quit "ERR:: Failed to copy $origin to $target" && echo ":: Copied $origin to $target"
cd $startFolder # go back to start folder

# ::::::::::::::::::::
## Release
# ::::::::::::::::::::
#  This is not executed when calling with "make" argument.
# Create the release folders
#   that will be extracted by the user into install root folder (BASEPATH)
md $releasesDir
baseRoot="$releasesDir/$versionNumber"
md $baseRoot
modRoot="$baseRoot/$modname"
md $modRoot

# Copy the vm.pk3
origin="$PK3file"
target="$modRoot/$vmFile.pk3"
cp $origin $target

# Copy the cfg files
## description.txt
cp $cfgDir/description.txt $modRoot/description.txt
## Copy every .cfg file into the modRoot folder
cp $cfgDir/*.cfg $modRoot/

# Create the releasable zip file
## Calculate revision number
#   Find out the number of pk3 files already created for this version (num of files inside baseRoot) 
#   and assign that number to revNumber
revNumber=$(find $baseRoot -maxdepth 1 -type f -name "*.zip" -printf x | wc -c)

## Zip
packedFile=$fullname.$versionNumber-r$revNumber.zip
cd $baseRoot
zip -r "$packedFile" .



# ::::::::::::::::::::
quit "QVM script has finished. \nEnd of Script"
#!/usr/bin/env -S nim --hints:off
# ScriptMode: 
let sMode= 'w'    ; if sMode == 'w': mode= Scriptmode.Whatif elif smode == 's': mode= ScriptMode.Silent elif smode == 'v': mode= ScriptMode.Verbose else: discard #   WhatIf: Do not run commands, instead just echo what would have been done.
import lib/nim/shell
import strutils
#TODO: Convert to nimscript. Helper: github.com/Vindaar/shell
#TODO: Fix rev numbering not working properly


# Configuration
## Mod
const
  versionNumber   = "0.0.1"
  modname         = "osdf"
  fullname        = "opensource-defrag"

## Folders Configuration
const
  basepath        = "/app/vg/os-defrag" # installation folder
# code folders
  releasesDir     = "../bin/releases"
  devRoot         = "$HOME/gd/osdf"
  srcRoot         = &"{devRoot}/src"
  srcDir          = &"{srcRoot}/osdf-ioq3"
  cfgDir          = &"{srcRoot}/cfg"
# bin output
  binDir          = &"{devRoot}/bin"
  compileDir      = &"{binDir}/release-linux-x86_64"  # set by the compiler (makefile)
  bkpDir          = &"{binDir}/vm-bkp"
  vmFile          = "vm"   # without extension
  PK3file         = &"{compileDir}/{modname}/{vmFile}.pk3"  # created by the make block of this script

# ::::::::::::::::::::
# Helper code
## Aliases
shopt -s expand_aliases
alias cp='cp -v '
alias mv='mv -v '
alias md='mkdir -v '
alias zip='zip -v '
alias echo='echo -e '
startFolder="$(pwd)"
# ::::::::::::::::::::


# ::::::::::::::::::::
# Make
# ::::::::::::::::::::
# Remove previous compile, for better q3lcc debugging messages.
if true; then
  rm -rf $compileDir;
fi;

# Enter ioq3 folder
cd "$srcDir" || quit "ERR:: Failed to enter $srcDir" && echo ":: Entered folder: $(pwd)"
# Make qvm
#make BUILD_CLIENT=0 BUILD_SERVER=0 BUILD_GAME_SO=0 BUILD_DIR=$binDir BASEGAME=$modname
make || quit "ERR:: Failed to compile. Read compiler output for more info."

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
releaseBase="basepath" # releases subfolder name. Stored under each version folder (to avoid recursive zipping)

md $releasesDir
versRoot="$releasesDir/$versionNumber"
md $versRoot
baseRoot="$versRoot/$releaseBase"
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
#   Find out the number of zip files already created for this version (num of files inside versRoot) 
#   and assign that number to revNumber
revNumber=$(find $versRoot -maxdepth 1 -type f -name "*.zip" -printf x | wc -c)

## Zip
packedFile=$fullname.$versionNumber-r$revNumber.zip
cd $baseRoot
zip -r "$packedFile" .
mv $packedFile ../$packedFile


# ::::::::::::::::::::
quit "QVM script has finished. \nEnd of Script"

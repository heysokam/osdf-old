#!/bin/bash

# Configuration
devRoot="$HOME/gd/osdf"

srcRoot="$devRoot/src"
srcDir="$srcRoot/osdf-ioq3"
binDir="$devRoot/bin"
targetDir="$binDir/release-linux-x86_64"
bkpDir="$binDir/vm-bkp"
filename="vm"   # without extension
modname="osdf"
basepath="/app/vg/os-defrag" # installation folder

# Helper code
## Functions
hold() {
  while [[ true ]]; do 
    echo -e "]] Script ended. Press any key to exit."; 
    read -r -n 1; done; }
quit() { 
  echo "$1";
  if [[ -v HOLD ]]; then
    hold; exit
  else exit; fi; }
## Aliases
alias cp="cp -v"
alias mv="mv -v"
alias zip="zip -v"
alias echo="echo -e"
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

# Process
if [ "$1" = "make" ] || [ "$1" = "install" ]; then
# Enter ioq3 folder
cd "$srcDir" || quit "ERR:: Failed to enter $srcDir" && echo ":: Entered folder: $(pwd)"
# Make qvm
make BUILD_CLIENT=0 BUILD_SERVER=0 BUILD_GAME_SO=0 BUILD_DIR=$binDir BASEGAME=$modname

# Enter qvm compile target folder
cd "$targetDir"/$modname || quit "ERR:: Failed to enter $targetDir/$modname" && echo ":: Entered folder: $(pwd)"

# Zip qvm files with .pk3 extension
targetFile=$filename.pk3
zip -r $targetFile vm && echo ":: Created file: $(pwd)/$targetFile"

# Copy .pk3 to vm.bkp, with version control
cp -u --backup=t $targetFile "$bkpDir"/$targetFile 
echo -e "\n:: Created $targetFile backup file inside $bkpDir"

else quit "ERR:: No build option.";
fi

if [ "$1" = "install" ]; then 
origin="$targetDir/$modname/$targetFile"
target="$basepath/$modname/$targetFile"
cp -u "$origin" "$target" || quit "ERR:: Failed to copy $origin to $target" && echo ":: Copied $origin to $target"

elif [ "$1" = "make" ]; then echo ":: QVM made, but not installed.";
else quit "ERR:: No build option.";
fi

notify-send "QVM script has finished."
quit "]] End of Script."
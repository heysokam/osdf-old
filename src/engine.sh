#!/bin/bash

# Configuration
## Mod
engineName="q3e"

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
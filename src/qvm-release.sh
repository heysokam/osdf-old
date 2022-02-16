#!/bin/bash
# Helper code
## Aliases
alias cp="cp -v"
alias mv="mv -v"
alias md="mkdir -v"
alias zip="zip -v"
alias echo="echo -e"
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


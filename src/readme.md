# Folder structure
## osdf-ioq3
Contains a modified version of ioquake3 code, to use as a base for the mod.  
It has Q3A-1.32b code in those places where modifications to gameplay are found.

#TODO: Isolate the files that are needed, and keep the rest as linked files from ioq3 upstream repository.  
Figure out if there is a win+lnx compatible way of storing linked files, or if automation through python is a better solution.

## comp.py
Module where the compilation helper code is defined.  
Imported from ROOT/compile.py

## cfg.py
Module to setup settings for the scripts.

## bash.py  
Module to aid with bash scripting inside python.

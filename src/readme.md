# Folder structure
## osdf-ioq3
Contains a modified version of ioquake3 code, to use as a base for the mod.  
It has Q3A-1.32b code in those places where modifications to gameplay are found.

#TODO: Extract ioq3 qvm compilation tools, and use them to compile the gamecode based on oDFe engine and q3a-gpl gamecode

## osdf-odfe  
Modified oDFe engine for loading the mod.  
Not a requirement, just for convenience and isolating osdf- code from defrag code.

## comp.py
Module where the compilation helper code is defined.  
Imported from ROOT/compile.py

## cfg.py
Module to setup settings for the scripts.

## bash.py  
Module to aid with bash scripting inside python.

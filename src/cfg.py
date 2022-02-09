# Module-only guard
#   This script should be used as an import module.
#   Exit if script is not imported as such:
if __name__ == "__main__": exit("ERR:: This script is not meant to be executed independently")
# :::::::::::::::::


# General
modName= "osdf"

# Folders
rootDir = "."   # Where all other dirs are stored
binDir =rootDir+"/"+  "bin"  # Where the compiled binaries will be output
srcDir =rootDir+"/"+  "src"  # Source code of the mod
refDir =rootDir+"/"+  "ref"  # Reference code and other important information

# Other
space=" "
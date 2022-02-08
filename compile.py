# Imports
from sys import platform    # for platform specific flow control
from sys import path        # for loading scripts stored in subfolders (python :facepalm:, should be just "import folder/script")
sys.path.insert(1, './src/')
import cfg                  # Scripts configuration
import comp                 # Compiling functions

# Compile
## From Linux
if sys.platform.startswith('linux'):    # Linux-specific code here...
    exit("TEMPerr:: Script not connected. See ./src/comp.py")

## From Windows
elif sys.platform.startswith('win'):    # Windows-specific code here...
    exit("TEMPerr:: Compile manually. Windows platform compile script is not written yet.")

## Non supported platforms handler
else:   exit("ERR:: The OS platform you are using is not supported in this script. Consult ioq3 documentation on how to compile for it.")

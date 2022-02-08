# Imports
from sys import platform    # for platform specific flow control
from sys import path        # for loading scripts stored in subfolders (python :facepalm:, should be just "import folder/script")
sys.path.insert(1, './src/')
import cfg                  # Scripts configuration

# Run
## From Linux
if sys.platform.startswith('linux'):    # Linux-specific code here...
    exit("ERR:: Linux Run Script not written yet.")

## From Windows
elif sys.platform.startswith('win'):    # Windows-specific code here...
    exit("ERR:: Windows Run Script not written yet.")

## Non supported platforms handler
else:   exit("ERR:: The OS platform you are using is not supported in this script.")

# Imports
from sys import platform    # for platform specific flow control

# Folders
def rootDir = "."   # Where all other dirs are stored
def binDir = "bin"  # Where the compiled binaries will be output
def srcDir = "src"  # Source code of the mod
def refDir = "ref"  # Reference code and other important information

# Compile
import subprocess   # for bash scripting
if sys.platform.startswith('linux'):    # Linux-specific code here...
    subprocess.run(["ls"])              # Basic command
    subprocess.run(["ls", "-la"])       # Command with arguments

elif sys.platform.startswith('win'):    # Windows-specific code here...
    return

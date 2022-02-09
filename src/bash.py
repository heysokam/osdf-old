# Module-only guard
#   This script should be used as an import module.
#   Exit if script is not imported as such:
if __name__ == "__main__": exit("ERR:: This script is not meant to be executed independently")
# :::::::::::::::::


# Bash scripting helper code
import subprocess   # for running bash processes. Requires python 3.5+

def bash(cmd): subprocess.run([cmd])
def bash(cmd, arg): subprocess.run([cmd, arg])
def bash(cmd, arg1, arg2): subprocess.run([cmd, arg1, arg2])
# bash("ls")              # Basic command
# bash("ls", "-la")       # Command with arguments
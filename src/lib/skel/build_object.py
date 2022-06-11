
# Skel Build Object
#::::::::::::::::::
skel = base.clone()
## Environment & System
skel.plat     = '' # Target Platform. Assumes current if None
skel.arch     = '' # Target Architecture. Assumes current if None
## Source code
skel.src      = [] # List of files that will be compiled
skel.srcdir   = '' # Folder where the source code is taken from
# Output data
skel.bindir   = '' # Folder where the binaries will be created
skel.binname  = '' # Base name of the binary  `name` will become `name-x64`
skel.bintype  = '' # Output type of the file (executable or library)
## Compiler
skel.ctype    = '' # Performance type (release, debug, etc) (ctype = compiler type)
skel.ccflags += [] # Flags to append to CCFLAGS
skel.defines += [] # Flags to append to CPPDEFINES
skel.libs    += [] # Flags to append to LIBS
skel.ldflags += [] # Flags to append to LINKFLAGS
skel.ccpath  += [] # Flags to append to CCPATH
skel.parse   += [] # Will be setup as env.ParseConfig('value')
## Custom compiler name (non verbose)
skel.cStr     = '' # Format for CC compiler command. Assumes "CC" if None
skel.lStr     = '' # Format for LD compiler command. Assumes "LD" if None
## Order SCons to setup with data
#skel.setup()

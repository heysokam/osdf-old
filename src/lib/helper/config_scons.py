import os
import sys; sys.dont_write_bytecode=True  # Do not create bytecode __pycache__ folder
from lib.helper.scons import getVersion, isVerbose
from SCons.Script import ARGUMENTS, Dir, File

# They are used as declarations. Values MUST be at least `None`
trgPlatform = None  # Can't be an alias, must be a valid & supported SCons platform
trgArch     = None  # Only for overriding. `x86_64` or `x86` are assumed from platform, if cur is not amd64

# Set Defaults
# :::::::::::::::: 
# Output filename
cName             = 'osdf'
dName             = cName+'.ded'
render_prefix     = cName
# Directories
rootDir           = Dir('..')                       # Must be relative. Was Absolute
srcDir            = Dir('.')                        # This MUST be relative to the SConstruct file.
engineDir         = srcDir.Dir('engine')            # Repository for engine code
gameDir           = srcDir.Dir('game')              # Repository for gamecode
binDir            = rootDir.Dir('bin')              # Output root folder where binaries will be compiled to
instDir           = rootDir.Dir('install-'+cName)   # Default linux:  '/usr/local/games/quake3'
baseDir           = None                            #TODO: what is this DEFAULT_BASEDIR value used for?
# Select what to build
build_default     = ['game']#['release','debug',]   # List of targets to build by default. Will use debug if empty
# Select what systems to compile
use_local_jpeg    = True   # Links to local jpeg (windows only). Binaries are hard to find
use_local_pcre    = True   # Links to local pcre (windows only). Binaries are hard to find
#use_sdl           = True  # Disabled. Always True
#use_curl          = True  # Disabled. Always True
#use_local_headers = False # Disabled. Always False 
#use_ccache        = True  # Deprecated. Scons has a compiler cache system
# Render compile settings
render_default    = 'opengl' # valid options: opengl, vulkan, opengl2
use_opengl        = True
use_opengl2       = False
use_vulkan        = True
use_vulkan_api    = use_vulkan #Default: True   #TODO: What is this used for?
use_opengl= use_opengl2= use_vulkan= use_vulkan_api= False
if render_default == 'opengl':  use_opengl  = True
if render_default == 'opengl2': use_opengl2 = True
if render_default == 'vulkan':  use_vulkan  = use_vulkan_api = True

# Versioning
verFile           = engineDir.Dir('qcommon').File('q_shared.h')  # File where the version will be searched for. If changed, version won't be searched for in the right file
verMacro          = 'Q3_VERSION'                     # Macro name of the version value. If changed, version won't be found in the file
version           = getVersion(verFile,verMacro)     # If this is changed, we overwrite the project's version defined in the source code

# SCons config
## General
scDir             = 'scons'         # Relative to the bin folder. Will be created when needed
scDecider         = 'MD5-timestamp' # First timestamp, then MD5. SCcons default = 'MD5' = 'content'. Makefile default = timestamp = 'make'
cores             = 12   # Max Computer cores available. Set to 0 or None for default cli behavior
coresPc           = 0.7  # Percentage of cpu that will be used for compiling jobs. Ignored if cores is 0, or `-j NUM` is set from CLI
## Verbose
scQuiet   = False # When True, make scons behave as if it was called with `scons -Q`
verbose   = isVerbose()  #fixme: Use this when the SCons bug is fixed
#verbose   = False  #FIXME: Set to None for normal behavior


# Source code directories
# ::::::::::::::::::::::::::
############################
# Engine src folders      #  relative to srcDir, we need multiple links (virtual copies) for SCons. absolute = srcDir/'folder'
clDir  = 'client'
svDir  = 'server'
rcDir  = 'rendc'
r1Dir  = 'rend1'
r2Dir  = 'rend2'
rvDir  = 'rendv'
sdlDir = 'sdl'
qcmDir = 'qcommon'
unxDir = 'unix'
winDir = 'win32'
botDir = 'botlib'
# Libraries
libDir  = 'lib'
jpgDir  = os.path.join(libDir,'jpeg')
pcreDir = os.path.join(libDir,'pcre')
# Gamecode src folders
cgDir  = 'cgame'
sgDir  = 'sgame'
uiDir  = 'ui'
# LCC Compiler tools folder     #TODO: Port from ioq3 Makefile
# toolDir= lnkDir +s+ 'tools'
# lccDir = lnkDir+toolDir +s+ 'lcc'
# Not used
asmDir = 'asm'
tuiDir = 'ui_ta'

## Compiler Flags
# ::::::::::::::::
##################
# Added by AppendUnique. Doesn't matter if there are duplicates in each    # err when = None
CCFLAGS_base = [] # Will be used in all targets
CCFLAGS_rls  = [] # Optimization CCFLAGS. Will be used in Release versions
CCFLAGS_dbg  = [] # Debug CCFLAGS. Will be used in Debug versions
DFLAGS_base  = [] # Preprocessor flags, defined on compilation. (CPPDEFINES, -D without prefix)
CCPATH_base  = [] # Include folders (CPPPATH, `-I` without prefix)
LIBS_base    = [] # Libraries that will be included
LDFLAGS_base = [] # Flags for the linker (LINKFLAGS)
PARSE_base   = [] # Commands to parse with ParseConfig('cmd arg1 arg2')



# Import guard
if __name__=='__main__': import sys; sys.exit(f'::MODULE-ERROR: {__file__} is not meant to be executed on its own')

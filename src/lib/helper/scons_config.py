import os
from lib.helper.scons import getVersion, isVerbose
from SCons.Script import ARGUMENTS

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
rootDir           = os.getcwd()                # Absolute
srcDir            = rootDir+'/code'            # MUST be absolute
binDir            = rootDir+'/bin'
instDir           = rootDir+'/install-'+cName  # Default linux:  '/usr/local/games/quake3'
baseDir           = None                       #TODO: what is this DEFAULT_BASEDIR value used for?
# Select what to build
build_client      = True
build_server      = True
build_default     = ['debug',]   # List of targets to build by default
# Select what systems to compile
#use_sdl           = True  # Disabled. Always True
#use_curl          = True  # Disabled. Always True
#use_pcre          = True  # Disabled. Always True
#use_system_jpeg   = True  # Disabled. Always True
#use_local_headers = False # Disabled. Always False 
#use_ccache        = True  # Deprecated. Scons has a compiler cache system
#genDependencies   = True   #TODO: This might not be needed at all. Chapter 6.5. ParseDepends should only be used if the scanners fail (they probably wont)
# Render compile settings
render_default    = 'opengl' # valid options: opengl, vulkan, opengl2
use_opengl        = True
use_opengl2       = False
use_vulkan        = True
use_vulkan_api    = use_vulkan #Default: True   #TODO: What is this used for?
#use_render_dlopen = False  # Disabled. We are not using renderer hotplug. Default is True
#if not use_render_dlopen:    # Disabled. We are not using renderer hotplug
use_opengl= use_opengl2= use_vulkan= use_vulkan_api= False
if render_default == 'opengl':  use_opengl  = True
if render_default == 'opengl2': use_opengl2 = True
if render_default == 'vulkan':  use_vulkan  = use_vulkan_api = True
# Others
#use_curl_dlopen   = False if mingw else True  # Disabled. Curl hotplug is not needed   # Force false for mingw

# Versioning
verFile           = srcDir+'/qcommon/q_shared.h'  # File where the version will be searched for. If changed, version won't be searched for in the right file
verMacro          = 'Q3_VERSION'                  # Macro name of the version value. If changed, version won't be found in the file
version           = getVersion(verFile,verMacro)  # If this is changed, we overwrite the project's version defined in the source code

# SCons config
## General
scDir             = binDir+'/scons'
scDecider         = 'MD5-timestamp'  # First timestamp, then MD5. SCcons default = 'MD5' = 'content'. Makefile default = timestamp = 'make'
cores             = 12   # Max Computer cores available. Set to 0 or None for default cli behavior
coresPc           = 0.7  # Percentage of cpu that will be used for compiling jobs. Ignored if cores is 0, or `-j NUM` is set from CLI
## Verbose
scQuiet   = False # When True, make scons behave as if it was called with `scons -Q`
verbose   = isVerbose()  #fixme: Use this when the SCons bug is fixed
#verbose   = False  #FIXME: Set to None for normal behavior


# Source code directories
# ::::::::::::::::::::::::::
############################
dbgDir = binDir+f'/debug-{trgPlatform}-{trgArch}'    #TODO: Switch trgDir
rlsDir = binDir+f'/release-{trgPlatform}-{trgArch}'  #TODO: Switch trgDir
#trgDir = binDir+f'/{trgType}-{trgPlatform}-{trgArch}'  # ex:   release-posix-x86_64
# Engine src folders      #  relative to srcDir, we need multiple links (virtual copies) for SCons. absolute = srcDir+'/folder'
asmDir = '/asm'
clDir  = '/client'
svDir  = '/server'
rcDir  = '/rendc'
r1Dir  = '/renderer'
r2Dir  = '/renderer2'
rvDir  = '/rendv'
sdlDir = '/sdl'
qcmDir = '/qcommon'
unxDir = '/unix'
winDir = '/win32'
botDir = '/botlib'
uiDir  = '/ui'
jpgDir = '/libjpeg'
# Gamecode src folders       #TODO: Port from ioq3 Makefile
# cgDir  = lnkDir+'/cgame'
# gDir   = lnkDir+'/game'    #TODO: '/game/sgame'
# quiDir = lnkDir+'/q3_ui'
# LCC Compiler tools folder
# toolDir= lnkDir+'/tools'
# lccDir = lnkDir+toolDir+'/lcc'

## Compiler Flags
# ::::::::::::::::
##################
# Added by AppendUnique. Doesn't matter if there are duplicates in each
#  err when = None
CCFLAGS_base = [] # Will be used in all targets
CCFLAGS_rls  = [] # Optimization CCFLAGS. Will be used in Release versions
CCFLAGS_dbg  = [] # Debug CCFLAGS. Will be used in Debug versions
DFLAGS_base  = [] # Preprocessor flags, defined on compilation. (CPPDEFINES, -D without prefix)
CCPATH_base  = [] # Include folders (CPPPATH, `-I` without prefix)
LIBS_base    = [] # Libraries that will be included
LDFLAGS_base = [] # Flags for the linker (LINKFLAGS)



# Import guard
if __name__=='__main__': import sys; sys.exit(f'::MODULE-ERROR: {__file__} is not meant to be executed on its own')

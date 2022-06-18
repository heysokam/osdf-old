# Imports
import sys
from os.path import exists, sep # file/dir checks
from copy import deepcopy       # Class cloning
from SCons.Script import *      # SCons specific variables and methods
from lib.helper import mingw    # MinGW Environment() setup

# SCons
scPlatforms    = ['posix', 'win32', 'cygwin', 'darwin', 'aix', 'hpux', 'irix', 'os2', 'sunos']
scArchs        = { 64:['x86_64','amd64'], 32:['x86','arm']}
def mkTruArch(bits,dic):  # Creates and returns a list of (64 or 32) platform aliases contained within the values of `dic`
  #explanation            [val.iterable (for sublist in list_of_lists:  for val in sublist: if     condition:                    )]
  if   bits == 64: return [val           for key,lst in dic.items()     for val in lst      if not any(ch.isdigit() for ch in val)]  # Dictionary value = list of 64bit platforms
  elif bits == 32: return [val           for key,lst in dic.items()     for val in lst      if     any(ch.isdigit() for ch in val)]  # Dictionary value = list of 32bit platforms
  else: sys.exit('::ERR Unsupported bits input for the function mkTruArch')
truPlatform    = {'win32':['w','win','w32','win32'],                   # Accepted win32 aliases in p=X, platform=X
                  'posix':['l','lnx','linux','l32','lnx32','linux32']} # Accepted posix aliases
truArch        = {'x86_64':mkTruArch(64,truPlatform), 'x86':mkTruArch(32,truPlatform)}        # Generated. Each value contains a list of valid platform aliases, with arch assigned as its dict key
def isVerbose():
  #AddOption('-V', dest='verbose', action='store_true')  #FIXME: AddOption is bugged until scons bugfix
  #return bool(GetOption('verbose'))
  return bool(ARGUMENTS.get('V') == '1')  #TEMP: Set V=1 on CLI. AddOption not working until scons bugfix

# General
def chkExists(p): return True if exists(p) else False  # True if dir or file exists
def getPrev(var, value):  return locals().get(var,value) # Get previously existing value, or return `value` instead if variable is None. Values must be declared, or it NameErrors anyway
def getLocal(var, value): return getPrev(var,value)      # Alias of getPrev. Used for signaling that values are taken from the scons_local file first
def getKey(val,dic):  # Get key of the dic.sublist that contains val
  for key, lst in dic.items():
    if val in lst: return key

# Version
import re
def getVersion(file,macro):
  for line in open(file.abspath).readlines():   # For every line in file
    parts = line.split()                        # Convert line into a list
    lineIsEmpty = not bool(parts)               # true if parts is None
    lineHasOneWord = not (0 < 1 < len(parts))   # bool( index `1` exists in `parts` )  :Python thinks: (0 < 1) and (1 < len(parts)) 
    if lineIsEmpty or lineHasOneWord: continue
    lineContainsMacro = bool(parts[1] == macro)  # If the second word is the macro name
    if lineContainsMacro:
      # Search for Pattern in this line
      exp = '\\\".* ([^ ]*)\\\"'#   from first `"` until last ` ` before a group of anything with no spaces, that's right before the last `"`
      obj = re.compile(exp)     # Compile the expression
      m   = obj.search(line)    # Compare exp with line
      vers = m.group(1)         # Version is content of group #1 (between parenthesis)
      return vers               # Return string matched  # Stops at first line matched. Macro redefinitions are not standard ISO
 
# Get Values from
## CLI
def getCliArch_arg():   # Get CLI supplied architecture, from argument `arch=NAME`. Check if valid. Or None if both checks fail
  arch = ARGUMENTS.get('arch')
  if not arch: return None  # Skip checking if not supplied
  if arch not in [ar  for key,lst in scArchs.items()  for ar in lst]:  sys.exit(f'ERR:: Invalid argument arch={arch}. Not supported by SCons')
  return arch
def getCliArch_tru():   # Get assumed architecture, from the truArch table, based on argument `p=` or `platform=`
  plat = getCliPlatform_arg() # Get raw alias from p= or platform=
  if not plat: return None  # Skip checking if not supplied
  if plat not in [alias  for key,lst in truArch.items()  for alias in lst]:  sys.exit(f'ERR:: Platform p={plat}. Is not mapped to any Architecture')
  return getKey(plat,truArch) # Assumes x86 from the truArch table
def getCliArch(): return getCliArch_arg() if getCliArch_arg() else getCliArch_tru()  # Get arch from `arch=`, else deduce it from `p=` or `platform=`

def getCliPlatform(): return getCliPlatform_tru()
def getCliPlatform_arg():  # Gets the raw alias, from CLI argument `p=` or `platform=` IF its valid. Else, None
  plat = ARGUMENTS.get('p') if ARGUMENTS.get('p') else ARGUMENTS.get('platform')
  if not plat: return None  # Skip checking if not supplied
  if plat not in [alias  for key,lst in truPlatform.items()  for alias in lst]:  sys.exit(f'ERR:: Invalid alias: p={plat}. Not supported in this script')
  return plat
def getCliPlatform_tru():  # Converts alias to SCons supported architecture
  plat = getCliPlatform_arg()
  return getKey(plat,truPlatform)

# Supported Lists
validPlatforms = ['posix', 'win32' ]  #TODO: 'win32' #todo:,'darwin',.  They depend on the toolchain, they need specific config
validArchs     = ['x86_64',]  # amd64 defaults to x86_64, unless specified.   #todo: 'x86', 'arm', 'arm64'
validTargets   = ['release','debug',     'distribute', 'all',
                  'engine', 'engine-dbg','engine-dist',
                  # 'server', 'server-dbg','server-dist',  #TODO: 'server',
                  'game',   'game-dbg',  'game-dist']
# Aliases
  # Q3 renames  (not using them, keeping only as reference for future support implementation)
  # q3Platforms  = ['x86_64', 'x86', 'mingw32', 'mingw64','darwin', 'aarch64']
  # remaps:        'arm64':'aarch64',  'mingw32'+'i386':'x86',   'cygwin':'mingw32',   'arm':'aarch64'
  # q3Archs      = ['i86pc','x86','x86_64','x64']
  # remaps:        'i86pc':'x86',   'x86_64'or'x64':'x86_64'
# Other
vmArchs         = ['x86_64', 'x86', 'arm', 'aarch64'] # List of architectures compatible with vm compiling  #TEMP: Q3 names. fix this
def getCliTargets(): # Returns a list of valid targets, with error checking
  if not cliTarg(): return None # Skip empty from check, so that it doesn't err
  result = ['']
  for it in COMMAND_LINE_TARGETS:
    if it not in validTargets: sys.exit(f'::ERR Target  {it}  is not a valid target')
    result.append(it)
  return result

PLAT=0; ARCH=1; SYS=2; BITS=3; TRG=4 # Indexes for getCli / getCur
def getCli(v):
  switch = {
    ARCH     : getCliArch(),
    PLAT     : getCliPlatform(),
    SYS      : (getCliPlatform(),getCliArch()),
    TRG      : getCliTargets(),  }
  return switch.get(v,None)
def cliArch(): return bool(ARGUMENTS.get('arch'))
def cliPlat(): return bool(ARGUMENTS.get('p') or ARGUMENTS.get('platform'))
def cliTarg(): return bool(COMMAND_LINE_TARGETS)

def getBits(arch):
  if not arch: return None
  if arch not in [ar for key,lst in scArchs.items()  for ar in lst]:  sys.exit(f'ERR:: Couldnt get bits. {arch} not supported by SCons.')
  return getKey(arch,scArchs) # If the value is in scArchs.sublists, get the bits from scArchs
def isBits(bits,arch): return bool(getBits(arch)==bits)

## Current System
def getCur(v): 
  curEnv = DefaultEnvironment() 
  switch = {
    ARCH     : curEnv['HOST_ARCH'] if not (curEnv['HOST_ARCH']=='amd64') else 'x86_64', # SCons detected arch. Swap amd64 to x86_64 (can be overwritten, but #todo: support)
    PLAT     : curEnv['HOST_OS'],
    BITS     : getBits(curEnv['HOST_ARCH']), }
  return switch.get(v,None)

# SCons Helpers
# This is the SCons way of specifying an output folder for binaries. We are just abstracting away the confusion :shrug:
def LinkDir(src, trg):  # trg=src :: Make trg a virtual copy of src
  VariantDir(trg.relpath, src.relpath, duplicate=0)
  if isVerbose(): print(f':: Linked {src} to {trg}')
  return trg  
def MapDir (src, trg):  # trg=src :: Make trg a copy of src, that contains a duplicate of src when it was compiled
  VariantDir(trg,src, duplicate=1)
  if isVerbose(): print(f':: Linked {src} to {trg}')
  return trg  
def getGlob(ab,rel):
  result = []
  glob = Glob(os.path.join(ab,rel))
  for file in glob: 
    result += [re.sub(r'[a-z]*','',file.relpath, count=1)] # Remove first instance of relpath from the file string
  if isVerbose(): print(f'|--> Glob for {ab} + {rel} =\n{result}\n')
  return result

# Build Information
def printEnvData(env):  # Same as env.Dump(), but custom format
  print(":: Compiler values are:"); 
  for it in sorted(env.Dictionary().items()): print(":| %s = %s" % it)
class BuildInfo:   # Build Information that will be printed on console
  def __init__(self, name='', version='', bindir='', baseflags='', rlsflags='', dbgflags=''):
    # Inputs
    self.name      = name
    self.version   = version
    self.bindir    = bindir
    self.baseflags = baseflags
    self.rlsflags  = rlsflags
    self.dbgflags  = dbgflags
    # Processed
    self.curPlat   = getCur(PLAT)
    self.curArch   = getCur(ARCH)
    self.curBits   = getCur(BITS)
    self.targets   = [it for it in getCli(TRG)] if getCli(TRG) else ['---']
    self.cc        = DefaultEnvironment()['CC']
    self.ccvers    = DefaultEnvironment()['CCVERSION']
  def print(self):
    print(f':: Software Construction tool for:  {self.name}  v.{self.version}')
    print(f': Current host platform:            {self.curPlat}')
    print(f': Current host arch:                {self.curArch}')
    print(f': Keywords requested:               {", ".join(str(it) for it in self.targets)}')
    print(f': Build output folder:              {self.bindir}')
    print(f': CC:                               {self.cc} v.{self.ccvers}')
    print(f': CCFLAGS Base:')
    print(f'          {", ".join(str(it) for it in self.baseflags)}')
    print(f': CCFLAGS Release:')
    print(f'          {", ".join(str(it) for it in self.rlsflags)}')
    print(f': CCFLAGS Debug:')
    print(f'          {", ".join(str(it) for it in self.dbgflags)}')
    #TODO: Which targets/platforms are being compiled


# Build Object Class
#class BuildData:    #todo (maybe):  figuring out super() for cloning was stupid hard, compared to the benefit
class BuildObject:
  def __init__(self, src:list|None=None, srcdir:str|None=None, bindir:str|None=None, binname=None, bintype=None, \
               ctype:str|None=None, ccflags:list|None=None, defines:list|None=None, libs:list|None=None, ldflags:list|None=None, \
               ccpath:list|None=None, libpath:list|None=None, parse:list|None=None, \
               env=None, cStr:str|None=None, lStr:str|None=None, plat:str|None=None, arch:str|None=None ):
    # Target                                                 * Mandatory    
    self.src     = [] if src     is None else src      # * List of files that will be compiled
    self.srcdir  = '' if srcdir  is None else srcdir   # * Folder where the source code is taken from
    self.bindir  = '' if bindir  is None else bindir   # * Folder where the binaries will be created
    self.binname = '' if binname is None else binname  # * Base name of the binary  `name` will become `name-x64`
    self.bintype = '' if bintype is None else bintype  # * Output type of the file (executable or library)
    # Compiler                                               - Optional
    self.ctype   = '' if ctype   is None else ctype    # - Performance type (release, debug, etc) (ctype = compiler type)
    self.ccflags = [] if ccflags is None else ccflags  # - Flags to append to CCFLAGS     (-Wflag)
    self.defines = [] if defines is None else defines  # - Flags to append to CPPDEFINES  (-DSOMEFLAG)
    self.libs    = [] if libs    is None else libs     # - Flags to append to LIBS        (-lsomelib)
    self.ldflags = [] if ldflags is None else ldflags  # - Flags to append to LINKFLAGS   (-Wl,someflag)
    self.ccpath  = [] if ccpath  is None else ccpath   # - Flags to append to CCPATH      (-I/path/to/smth)
    self.libpath = [] if libpath is None else libpath  # - Flags to append to LIBPATH     (-L/path/to/smth)
    self.parse   = [] if parse   is None else parse    # - Will be setup as env.ParseConfig('value')
    # Environment & System
    self.env     = env          # - Preexisting Environment to construct with
    self.plat    = '' if plat    is None else plat     # - Target Platform. Assumes current if None
    self.arch    = '' if arch    is None else arch     # - Target Architecture. Assumes current if None
    self.cStr    = '' if cStr    is None else cStr     # - Format for CC compiler command. Assumes "CC" if None
    self.lStr    = '' if lStr    is None else lStr     # - Format for LD compiler command. Assumes "LD" if None
  # Print Debug
  def debugPrint(self):
    print( "\n::::::::::::::::::::::::::::::::::::::::::")
    print(  f": Debug Data for:  {self.binname}")
    print(   "::::::::::::::::::::::::::::::::::::::::::")
    print('src=\n',[str(n) for n in self.src],"\n:::::::::::::::::::::::::::::")
    print('srcdir=\n',self.srcdir,"\n:::::::::::::::::::::::::::::")
    print('bindir=\n',self.bindir,"\n:::::::::::::::::::::::::::::")
    print('binname=\n',self.binname,"\n:::::::::::::::::::::::::::::")
    print('bintype=\n',self.bintype,"\n:::::::::::::::::::::::::::::")
    print('ctype=\n',self.ctype,"\n:::::::::::::::::::::::::::::")
    print('ccflags=\n',self.ccflags,"\n:::::::::::::::::::::::::::::")
    print('defines=\n',self.defines,"\n:::::::::::::::::::::::::::::")
    print('libs=\n',self.libs,"\n:::::::::::::::::::::::::::::")
    print('ldflags=\n',self.ldflags,"\n:::::::::::::::::::::::::::::")
    print('ccpath=\n',self.ccpath,"\n:::::::::::::::::::::::::::::")
    print('libpath=\n',self.libpath,"\n:::::::::::::::::::::::::::::")
    print('parse=\n',self.parse,"\n:::::::::::::::::::::::::::::")
    print('env=\n',self.env,"\n:::::::::::::::::::::::::::::")
    print('plat=\n',self.plat,"\n:::::::::::::::::::::::::::::")
    print('arch=\n',self.arch,"\n:::::::::::::::::::::::::::::")
    print('cStr=\n',self.cStr,"\n:::::::::::::::::::::::::::::")
    print('lStr=\n',self.lStr,"\n:::::::::::::::::::::::::::::")
  # Type Checks       
  def chkList(self,var, errNone=False):    # errNone=False : Content is remapped to empty when its None. If True, it will ERR on None
    if not errNone and var is None: var = []
    if not isinstance(var,list): sys.exit(f'::ERR in {self.trg}:  {var} is type:  {type(var)}  Should be:  {type([])}')
  def chkStr (self,var, errNone=False):    # errNone=False : Content is remapped to empty when its None. If True, it will ERR on None
    if not errNone and var is None: var = ''
    if not isinstance(var, str): sys.exit(f'::ERR in {self.trg}:  {var} is type:  {type(var)}  Should be:  {type("")}')
  def chkDir (self,var, errNone=False):    # errNone=False : Content is remapped to empty when its None. If True, it will ERR on None
    if not errNone and var is None: var = ''
    if not isinstance(var, SCons.Node.FS.Dir): sys.exit(f'::ERR in {self.trg}:  {var} is type:  {type(var)}  Should be:  {type(Dir())}')
  def chkType(self,var,lst):
    if var not in lst:           sys.exit(f'::ERR in {self.trg}:  {var} is not a valid type. Valid list: {lst}')
  def chkEnv (self,var):
    tenv = type(DefaultEnvironment())
    if not isinstance(var,tenv): sys.exit(f'::ERR in {self.trg}:  {var} is type:  {type(var)}  Should be:  {tenv}')
  def check(self):
    #self.trg, self.src, self.bindir, self.binname, self.bintype,
    self.chkList(self.src,     errNone=True)
    self.chkDir (self.srcdir,  errNone=True)
    self.chkDir (self.bindir,  errNone=True)
    self.chkStr (self.binname, errNone=True)
    self.chkStr (self.bintype, errNone=True)
    self.chkType(self.bintype, ['bin','lib'])
    #self.ccflags, self.defines, self.libs, self.ldflags, self.ccpath, self.parse,
    self.chkStr (self.ctype)
    self.chkType(self.ctype, ['release','debug',''])
    self.chkList(self.ccflags)
    self.chkList(self.defines)
    self.chkList(self.libs)
    self.chkList(self.ldflags)
    self.chkList(self.ccpath)
    self.chkList(self.libpath)
    self.chkList(self.parse)
    #self.env, self.cStr, self.lStr,
    #self.chkEnv (self.env)  # Environment is only checked in BuildObject.setup()
    self.chkStr (self.cStr)
    self.chkStr (self.lStr)
    #self.plat, self.arch
    self.chkStr (self.plat)
    self.chkStr (self.arch)
  def clone(self): return deepcopy(self)  # Create a true clone. Default behavior is just a reference
  def merge(self, data):  # Merge self with data. Self takes precendence, unless variable is empty
    result = BuildObject()
    # Target
    emptyIfNone   = lambda i: i or []  # Returns an empty list when input is None. NoneType is not iterable
    result.src     = [f for f in emptyIfNone(self.src)] + [f for f in emptyIfNone(data.src)]
    result.srcdir  = self.srcdir  if self.srcdir  else data.srcdir
    result.bindir  = self.bindir  if self.bindir  else data.bindir
    result.binname = self.binname if self.binname else data.binname
    result.bintype = self.bintype if self.bintype else data.bintype
    # Compiler
    result.ctype   = self.ctype   if self.ctype   else data.ctype
    result.ccflags = [f for f in emptyIfNone(self.ccflags)] + [f for f in emptyIfNone(data.ccflags)]
    result.defines = [f for f in emptyIfNone(self.defines)] + [f for f in emptyIfNone(data.defines)]
    result.libs    = [f for f in emptyIfNone(self.libs)]    + [f for f in emptyIfNone(data.libs)]
    result.ldflags = [f for f in emptyIfNone(self.ldflags)] + [f for f in emptyIfNone(data.ldflags)]
    result.ccpath  = [f for f in emptyIfNone(self.ccpath)]  + [f for f in emptyIfNone(data.ccpath)]
    result.libpath = [f for f in emptyIfNone(self.libpath)] + [f for f in emptyIfNone(data.libpath)]
    result.parse   = [f for f in emptyIfNone(self.parse)]   + [f for f in emptyIfNone(data.parse)]
    # Environment & System
    result.env     = self.env  if self.env  else data.env
    result.plat    = self.plat if self.plat else data.plat
    result.arch    = self.arch if self.arch else data.arch
    result.cStr    = self.cStr if self.cStr else data.cStr
    result.lStr    = self.lStr if self.lStr else data.lStr
    if isVerbose(): print(f':: Merged {self} with {data}. Result =\n{result}')
    return result
  def setup(self): 
    # Add Processed data
    self.prefix  = f'{self.ctype}-' if self.ctype else ''         # Prefix for the alias
    self.subdir  = self.prefix + f'{self.plat}-{self.arch}'       # Alias for this build
    self.outdir  = self.bindir.Dir(self.subdir).Dir(self.srcdir.relpath)  # Final outdir. Will be linked to the source code folder
    self.trg     = self.outdir.Dir('..').File(self.binname)       # Combine outdir+binname into real output trg
    if isVerbose():
      print(f':: Created properties for BuildData {self.trg}:')
      print(f':  self.prefix = {self.prefix}')
      print(f':  self.subdir = {self.subdir}')
      print(f':  self.outdir = {self.outdir}')
      print(f':  self.trg    = {self.trg}')
    # Error check data
    self.check()
    if self.env: self.chkEnv(self.env)  # Only check if not none. If none, a new one will be created
    # Create new environment for trgSystem
    if not self.env: 
      plat = getCur(PLAT)
      if   plat in ['posix'] and self.plat in ['win32']: self.env = mingw.NewEnvironment(getBits(self.arch))
      # elif plat in ['win32'] and self.plat in ['posix']: pass#print(f'::WRN Cross-compilation win-to-linux has not being developed yet')
      elif plat in ['posix']: self.env = Environment()
      elif plat in ['win32']: self.env = Environment(tools=['mingw'])  # Currently no plans to support msvc tools
      elif plat in ['darwin']: sys.exit(f'::ERR MacOS host compilation has not being developed yet')
      else: sys.exit(f'::ERR Trying to compile for a non-supported platform: {getCur(PLAT)}')
    # Append Flags to env
    self.env.AppendUnique(CCFLAGS    = self.ccflags)
    self.env.AppendUnique(CPPDEFINES = self.defines)
    self.env.AppendUnique(LIBS       = self.libs)
    self.env.AppendUnique(LINKFLAGS  = self.ldflags)
    self.env.AppendUnique(CCPATH     = self.ccpath)
    self.env.AppendUnique(LIBPATH    = self.libpath)
    self.env.ParseConfig(self.parse) #TODO: Fix this for mingw, and for win32 hosts
    # Remove lib prefix
    if self.bintype in ['lib']: self.env.Replace(SHLIBPREFIX='')  # libXX = XX
    # Verbose check
    if not isVerbose():   # Format GCC commands output
      if self.cStr:
        self.env.Replace(CCCOMSTR   =f'{self.cStr} $SOURCES')
        self.env.Replace(SHCCCOMSTR =f'{self.cStr} $SOURCES')
      if self.lStr:
        self.env.Replace(LINKCOMSTR   =f'{self.lStr} $TARGET')
        self.env.Replace(SHLINKCOMSTR =f'{self.lStr} $TARGET')
    # Link srcdir to outdir       
    lnkDir = LinkDir(self.srcdir, self.outdir)
    # Convert src/file.c to lnk/file.c     #  src/sub/file.c to lnk/sub/file.c  when file is /sub/file.c
    code = None
    for file in self.src:  # For every file in the input src list
      if code is None: code  = [os.path.join(lnkDir.abspath,'..',file.relpath)]  # Initializes list. Only happens the first time. 
      else:            code += [os.path.join(lnkDir.abspath,'..',file.relpath)]  # lnkDir+file = Prepend lnkDir to the file string  `/path/to/folder`+`/sub/file.c`
    # Setup SCons to compile src with env as output
    if   self.bintype in ['bin']: self.trg = self.env.Program(      target=self.trg.abspath, source=code)
    elif self.bintype in ['lib']: self.trg = self.env.SharedLibrary(target=self.trg.abspath, source=code)
    else: sys.exit(f'::ERR in {self.trg}.setup():  Trying to set builder for an unknown type:  {self.bintype}')  # Should never happen



# Import guard
if __name__=='__main__': import sys; sys.exit(f'::MODULE-ERROR: {__file__} is not meant to be executed on its own')

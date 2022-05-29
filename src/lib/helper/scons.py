# Imports
import sys
from os.path import exists      # file/dir checks
from copy import deepcopy       # Class cloning
from SCons.Script import *      # SCons specific variables and methods

# SCons
scPlatforms    = ['posix', 'win32', 'cygwin', 'darwin', 'aix', 'hpux', 'irix', 'os2', 'sunos']
scArchs        = { 64:['x86_64','amd64'], 32:['x86','arm']}
def mkTruArch(bits,dic):  # Creates and returns a list of (64 or 32) platform aliases contained within the values of `dic`
  #explanation            [val.iterable (for sublist in list_of_lists:  for val in sublist: if     condition:                    )]
  if   bits == 64: return [val           for key,lst in dic.items()     for val in lst      if not any(ch.isdigit() for ch in val)],  # Dictionary value = list of 64bit platforms
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
  for line in open(file).readlines(): # For every line in file
    parts = line.split()              # Convert line into a list
    lineIsEmpty = not bool(parts)     # true if parts is None
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
  if plat not in [alias  for key,lst in truPlatforms.items()  for alias in lst]:  sys.exit(f'ERR:: Invalid alias: p={plat}. Not supported in this script')
  return plat
def getCliPlatform_tru():  # Converts alias to SCons supported architecture
  plat = getCliPlatform_arg()
  return getKey(plat,truPlatform)

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
    BITS     : getBits(curEnv['HOST_ARCH']),  }
  return switch.get(v,None)

# SCons Helpers
#def compile(obj, trg=None, env=DefaultEnvironment(), lib=False, cStr=None, lStr=None):   # Alias for readability
#  if cStr: env.Replace(CCCOMSTR=f'{cStr} $SOURCES')
#  if lStr: env.Replace(LINKCOMSTR=f'{lStr} $TARGET : $SOURCES')
#  if lib: env.SharedLibrary(trg, obj)
#  else:   env.Program(trg, obj)
# This is the SCons way of specifying an output folder for binaries. We are just abstracting away the confusion :shrug:
def LinkDir(src, trg): VariantDir(trg,src, duplicate=0); return trg  # trg=src :: Make trg a virtual copy of src
def MapDir (src, trg): VariantDir(trg,src, duplicate=1); return trg  # trg=src :: Make trg a copy of src, that contains a duplicate of src when it was compiled
def getGlob(ab,rel):
  result = []
  glob = Glob(ab+rel)
  for file in glob: 
    result += [file.abspath.replace(ab,'',1)]
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
  def __init__(self, src=None, srcdir=None, bindir=None, binname=None, bintype=None, \
               ctype=None, ccflags=None, defines=None, libs=None, ldflags=None, ccpath=None, parse=None, \
               env=None, cStr=None, lStr=None, \
               plat=None, arch=None ):
    # Target                         * Mandatory    
    self.src     = src          # * List of files that will be compiled
    self.srcdir  = srcdir       # * Folder where the binaries will be created
    self.bindir  = bindir       # * Folder where the binaries will be created
    self.binname = binname      # * Base name of the binary  `name` will become `name-x64`
    self.bintype = bintype      # * Output type of the file (executable or library)
    # Compiler                       - Optional
    self.ctype   = ctype        # - Performance type (release, debug, etc) (ctype = compiler type)
    self.ccflags = ccflags      # - Flags to append to CCFLAGS
    self.defines = defines      # - Flags to append to CPPDEFINES
    self.libs    = libs         # - Flags to append to LIBS
    self.ldflags = ldflags      # - Flags to append to LINKFLAGS
    self.ccpath  = ccpath       # - Flags to append to CCPATH
    self.parse   = parse        # - Will be setup as env.ParseConfig('value')
    # Environment & System
    self.env     = env          # - Preexisting Environment to construct with
    self.plat    = plat         # - Target Platform. Assumes current if None
    self.arch    = arch         # - Target Architecture. Assumes current if None
    self.cStr    = cStr         # - Format for CC compiler command. Assumes "CC" if None
    self.lStr    = lStr         # - Format for LD compiler command. Assumes "LD" if None
  # Type Checks       
  def chkList(self,var, errNone=False):    # errNone=False : Content is remapped to empty when its None. If True, it will ERR on None
    if not errNone and var is None: var = ['']
    if not isinstance(var,list): sys.exit('::ERR in {self.trg}:  {var} is type:  {type(var)}  Should be:  {type(list)}')
  def chkStr (self,var, errNone=False):    # errNone=False : Content is remapped to empty when its None. If True, it will ERR on None
    if not errNone and var is None: var = ''
    if not isinstance(var, str): sys.exit('::ERR in {self.trg}:  {var} is type:  {type(var)}  Should be:  {type(str)}')
  def chkType(self,var,lst):
    if var not in lst:           sys.exit('::ERR in {self.trg}:  {var} is not a valid type. Valid list: {lst}')
  def chkEnv (self,var):
    tenv = type(DefaultEnvironment())
    if not isinstance(var,tenv): sys.exit('::ERR in {self.trg}:  {var} is type:  {type(var)}  Should be:  {tenv}')
  def check(self):
    #self.trg, self.src, self.bindir, self.binname, self.bintype,
    self.chkList(self.src,     errNone=True)
    self.chkStr (self.srcdir,  errNone=True)
    self.chkStr (self.bindir,  errNone=True)
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
    self.chkList(self.parse)
    #self.env, self.cStr, self.lStr,
    #self.chkEnv (self.env)  # Environment is only checked in BuildObject.setup()
    self.chkStr (self.cStr)
    self.chkStr (self.lStr)
    #self.plat, self.arch
    self.chkStr (self.plat)
    self.chkStr (self.arch)
  def clone(self): return deepcopy(self)  # Create a true clone. Default behavior is just a reference
  def setup(self): 
    # Add Processed data
    self.prefix  = f'/{self.ctype}-' if self.ctype else '/'  # Prefix for the alias
    self.subdir  = self.prefix + f'{self.plat}-{self.arch}' # Alias for this build
    self.outdir  = self.bindir + self.subdir                # Final outdir
    self.trg     = self.outdir+'/'+self.binname             # Combine outdir+binname into real output trg
    if isVerbose():
      print(f':: Created properties for BuildData {self.trg}:')
      print(f':  self.prefix = {self.prefix}')
      print(f':  self.subdir = {self.subdir}')
      print(f':  self.outdir = {self.outdir}')
      print(f':  self.trg    = {self.trg}')
    # Error check data
    self.check()
    if self.env: self.chkEnv(self.env)  # Only check if not none. If none, a new one will be created
    # Create new environment for trgSystem       #self.env, self.plat, self.arch
    if not self.env: self.env = Environment(platform=self.plat, TARGET_ARCH=self.arch)
    # Append Flags to env         #self.ccflags, self.defines, self.libs, self.ldflags, self.ccpath,
    self.env.AppendUnique(CCFLAGS    = self.ccflags)
    self.env.AppendUnique(CPPDEFINES = self.defines)
    self.env.AppendUnique(LIBS       = self.libs)
    self.env.AppendUnique(LINKFLAGS  = self.ldflags)
    self.env.AppendUnique(CCPATH     = self.ccpath)
    self.env.ParseConfig(self.parse)
    # Verbose check               #self.cStr, self.lStr,
    if not isVerbose():   # Format GCC commands output
      if self.cStr: self.env.Replace(CCCOMSTR   =f'{self.cStr} $SOURCES')
      if self.lStr: self.env.Replace(LINKCOMSTR =f'{self.lStr} $TARGET : $SOURCES')
    # Link srcdir to outdir       
    lnkDir = LinkDir(self.srcdir, self.outdir) # self.bindir, self.bindir,
    # Convert src/file.c to lnk/file.c     #  src/sub/file.c to lnk/sub/file.c  when file is /sub/file.c
    #TODO: Recheck this logic
    #self.src, 
    code = None
    for file in self.src:  # For every file in the input src list
      if code is None: code = [lnkDir+file]; continue  # Initializes list. Only happens the first time. 
      code += [lnkDir+file]  # lnkDir+file = Prepend lnkDir to the file string  `/path/to/folder`+`/sub/file.c`
    # Setup SCons to compile src with env as output    # self.trg, self.binname, self.bintype,
    if   self.bintype in ['bin']: self.env.Program(      target=self.trg, source=code)
    elif self.bintype in ['lib']: self.env.SharedLibrary(target=self.trg, source=code)  #TODO: Do we need shlibvers?
    else: sys.exit('::ERR in {self.trg}.setup():  Trying to set builder for an unknown type:  {self.bintype}')  # Should never happen



# Import guard
if __name__=='__main__': import sys; sys.exit(f'::MODULE-ERROR: {__file__} is not meant to be executed on its own')

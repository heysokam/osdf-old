# ::::::::::::::::::::
#!/usr/bin/env -Sv nim --hints:off
# ScriptMode:
let sMode= "v"    ; if sMode == "w": mode= Scriptmode.Whatif elif smode == "s": mode= ScriptMode.Silent elif smode == "v": mode= ScriptMode.Verbose else: discard #   WhatIf: Do not run commands, instead just echo what would have been done.
# ::::::::::::::::::::
import os
import sequtils
import strutils, strformat
import lib/helper/build as b
import lib/helper/bash as sh
# ::::::::::::::::::::


# ::::::::::::::::::::
# Configuration
# ::::::::::::::::::::
# Mod
const
  modVers       = "0.2.0"
  modName       = "osdf"
  fullName      = "opensource-defrag"

# Folders
const
  installBase   = "/app/vg/os-defrag" # installation folder
  releaseBase   = "basepath" # releases subfolder name. Stored under each version folder (to avoid recursive zipping)
## Source folders
const
  devRoot       = getEnv"HOME"/"gd/osdf"
  rlsDir        = devRoot/"bin/releases"
  srcRoot       = devRoot/"src"
  gameDir       = srcRoot/"osdf-game"
  engineDir     = srcRoot/"osdf-engine"
  cfgDir        = srcRoot/"cfg"
## Source files
const
  dscFile      = cfgDir/"description.txt"
## bin output
const
  binDir        = devRoot/"bin"
  binDir_rl     = binDir/"release-posix-x86_64"
  binDir_rw     = binDir/"release-win32-x86_64"
  binDir_dl     = binDir/"debug-posix-x86_64"
  binDir_dw     = binDir/"debug-win32-x86_64"
  bkpDir        = binDir/modName&"-bkp"   # Might no longer be needed. Was used for vm-bkp
# Windows Libraries: Binaries
const
  libDir       = binDir/"lib"
  # Curl
  curlDir      = libDir/"wincurl"
  curlFile     = "libcurl-x64.dll"
  curlFile_rn  = "libcurl-4.dll"  # Name expected by the engine
  curlZip      = "curl-win64-latest.zip"
  curlLink     = &"https://curl.se/windows/{curlZip}"
  # SDL
  sdlDir       = libDir/"winsdl"
  sdlFile      = sdlDir/"SDL2.dll"
  sdlZip       = "SDL2-2.0.22-win32-x64.zip"
  sdlLink      = &"https://www.libsdl.org/release/{sdlZip}"
# Build Config
const
  alwaysClean = false  # Was used for better q3lcc debugging messages. Not needed with gcc


# ::::::::::::::::::::
# Make
# ::::::::::::::::::::
# Remove previous compiles
if alwaysClean or getOpt("c"):
  rm binDir_rl
  rm binDir_rw
  rm binDir_dl
  rm binDir_dw
# Decide what to build
let make       = getOpt("m")
let install    = not getOpt("r")
let keyword    = if getBuildType() != "": getBuildType() else: "debug"
let distribute = keyword in ["distribute"]
let release    = keyword in ["release", "game", "engine"]
let debug      = keyword in ["debug"]
let v          = if isVerbose(): 1 else: 0
let cmdBuild   = &"scons V={v} {keyword}"

# Enter srcDir and build
withDir srcRoot:
  echo &":: Entered folder: {getCurrentDir()}"
  try: exec cmdBuild
  except OSError: quit "ERR:: Failed to compile. Read compiler output for more info."

# Avoid installing or packing when called with "make" option
if make:  quit ":: Built done, but not copied, installed or packed."

# ::::::::::::::::::::
# Copy to ReleaseBase
#   *This is not executed when calling with "make" build type.
# ::::::::::::::::::::
# Create the release folders. Will be extracted by the user into install root folder (BASEPATH)
let versRoot = rlsDir/modVers
let baseRoot = versRoot/releaseBase
let modRoot  = baseRoot/modName
md modRoot # Creates all folders recursively

# Define folder list
var dirList:seq[string]
if   distribute:
  dirList.add(binDir_rl)
  dirList.add(binDir_rw)
elif release:
  if   isWin():   dirList.add(binDir_rw)
  elif isLinux(): dirList.add(binDir_rl)
elif debug:
  if   isWin():   dirList.add(binDir_dw)
  elif isLinux(): dirList.add(binDir_dl)

# Enter each compile folder, and get the appropiate files
for id,each in dirList:
  withDir each:
    echo &":: Entered folder: {getCurrentDir()}"
    var libExt:string
    var binExt:string
    if   "posix" in each:
      libExt = ".so"
      binExt = ".x64"
    elif "win32" in each:
      libExt = ".dll"
      binExt = ".exe"
    let libFiles = listFiles(getCurrentDir()).filterIt(libExt in it)
    let binFiles = listFiles(getCurrentDir()).filterIt(binExt in it)
    for id,it in libFiles:
      echo "test cp it"
      if not debug: cp it, modRoot
      if install:   cp it, installBase/modName
    for id,it in binFiles:
      if not debug: cp it, baseRoot
      if install:   cp it, installBase

# Copy the cfg files
## description.txt
cp dscFile, modRoot
if install: cp dscFile, installBase/modName
## Copy every .cfg file into the modRoot folder
let cfgFiles = listFiles(cfgDir).filterIt(".cfg" in it)
for id,it in cfgFiles:
  cp it, modRoot
  if install: cp it, installBase/modName

# Avoid installing when called with "m" or "r" options
if getOpt("r"):  quit ":: Build made & copied, but not installed or packed."
# Avoid packing when called with "i" option
if not distribute:  quit ":: Build made, copied & installed, but not packed."


# ::::::::::::::::::::
# Pack
# ::::::::::::::::::::
# Download windows library binaries
md libDir
withDir libDir:
  # Curl dll
  dl curlLink
  unzip curlZip, curlDir
  cpLatest curlDir,curlFile , baseRoot,curlFile_rn
  # SDL2 dll
  dl sdlLink, false
  unzip sdlZip, sdlDir
  cp sdlFile, baseRoot

# Calculate revision number
#   Find out the number of times this script has packed files for this version (num stored in revFile)
#   and update that number (inc by 1)
let revFile = baseRoot/".rev"
updRevNum(revFile)

# Zip
let packedFile = &"{fullName}.{modVers}-r{getRevNum(revFile)}.zip"
#cd $baseRoot
withDir baseRoot:
  echo &":: Entered folder: {getCurrentDir()}"
  zip ".", packedFile
  zipd ".rev", packedFile  # Remove .rev file from the release zip
  mv packedFile, ".."/packedFile, "file"

# ::::::::::::::::::::
quit ":: Build has finished. \n:  End of Script"

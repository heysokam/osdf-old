#!/usr/bin/env -S nim --hints:off
# ScriptMode:
let sMode= "s"    ; if sMode == "w": mode= Scriptmode.Whatif elif smode == "s": mode= ScriptMode.Silent elif smode == "v": mode= ScriptMode.Verbose else: discard #   WhatIf: Do not run commands, instead just echo what would have been done.
# ::::::::::::::::::::
import os
import strutils, strformat
import sequtils
import lib/helperBuild as b
import lib/helperBash as sh
# ::::::::::::::::::::

#TODO: Fix rev numbering not working properly


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
  srcDir        = srcRoot/"osdf-ioq3"
  cfgDir        = srcRoot/"cfg"
## Source files
const
  dscFile      = "description.txt"
## bin output
const
  binDir        = devRoot/"bin"
  compileDir    = binDir/"release-linux-x86_64"  # set by the compiler (makefile)
  bkpDir        = binDir/modName&"-bkp"
  modFile       = &"{modName}-{modVers}"   # without extension
  pk3Ext        = ".pk3"
  pk3Filename   = modFile & pk3Ext
  pk3File       = compileDir/modName/pk3Filename  # created by the make block of this script

# Build Config
const
  alwaysClean = false  # Was used for better q3lcc debugging messages. Shouldn"t be needed for compiling as library


# ::::::::::::::::::::
# Make
# ::::::::::::::::::::
# Remove previous compile
if alwaysClean: rm compileDir
# Decide what to build
let cmdBuild = if not verbose(): "make" else: "V=1 make"

# Enter srcDir and build
withDir srcDir:
  echo &":: Entered folder: {getCurrentDir()}"
  try: exec cmdBuild
  except OSError: quit "ERR:: Failed to compile. Read compiler output for more info."

# Enter compile target folder, and zip the appropiate files
withDir compileDir/modName:
  echo &":: Entered folder: {getCurrentDir()}"
  let soFiles = listfiles(getCurrentDir()).filterIt(".so" in it).join(" ")
  let ztarget = soFiles #TODO: Fix wrong target
  zip ztarget, pk3File  # Zip files with .pk3 extension

# Copy .pk3 to bkp folder, with version control
cpBkp pk3File, bkpDir/pk3Filename

# Avoid installing when called with "make" option
if getBuildType() == "make":  quit ":: Built done, but not installed or packed."


# ::::::::::::::::::::
# Install
#   *This is not executed when calling with "make" argument.
# ::::::::::::::::::::
let origin=compileDir/modName/pk3Filename
let itarget=installBase/modName/pk3Filename
cpUpd origin, itarget

# ::::::::::::::::::::
# Release
# ::::::::::::::::::::
#  This is not executed when calling with "make" build type.
# Create the release folders
#   these will be extracted by the user into install root folder (BASEPATH)
let versRoot = rlsDir/modVers
let baseRoot = versRoot/releaseBase
let modRoot  = baseRoot/modName
md modRoot # Creates all the folders recursively

# Copy the modFile.pk3
cp pk3File, modRoot/modFile&pk3Ext, "file"

# Copy the cfg files
## description.txt
cp cfgDir/dscFile, modRoot/dscFile, "file"
## Copy every .cfg file into the modRoot folder
let cfgFiles = listfiles(cfgDir).filterIt(".cfg" in it)
for id,it in cfgFiles:
  #cp cfgDir/"*.cfg", modRoot, "file"
  let ctarget = it.splitFile().name & it.splitFile().ext
  cp it, modRoot/ctarget, "file"

# Create the releasable zip file
## Calculate revision number
#   Find out the number of times this script has been run for this version (num stored in revFile)
#   and update that number (inc by 1)
let revFile = baseRoot/".rev"
updRevNum(revFile)

## Zip
let packedFile = &"{fullName}.{modVers}-r{getRevNum(revFile)}.zip"
#cd $baseRoot
withDir baseRoot:
  echo &":: Entered folder: {getCurrentDir()}"
  zip ".", packedFile
  zipd ".rev", packedFile  # Remove .rev file from the release zip
  mv packedFile, ".."/packedFile, "file"

# ::::::::::::::::::::
quit ":: Build has finished. \n:  End of Script"

import os, strformat, strutils
# Make Directories (md)
proc md*(d:string)=  #alias md="mkdir -v "
  if dirExists(d): echo &":: Directory {d} already exists. Ignoring its creation."
  try:             mkDir(d); echo &":: Created directory {d}"
  except OSError:  quit &"::ERR Failed to make directory {d}"
proc md*(d:string,o:bool):string=  md(d); result = if o: d else: ""  # Alias for creation and also assignment to variables
proc checkOrMkDir(f:string)=
  let d=splitFile(f).dir; if not dirExists(d): md d
# Copying
proc cp*(s:string,d:string,t:string)=  #alias cp="cp -v "
  checkOrMkDir(d)
  try:
    case t:
    of "dir":   cpDir(s,d);  echo &":: Copied dir {s} to {d}"
    of "file":  cpfile(s,d); echo &":: Copied file {s} to {d}"
    #of "ftodir":  copyFileToDir(s,d); echo &":: Copied file {s} to dir {d}"
  except OSError:  quit &"::ERR Failed to copy {s} to {d}"
proc cpBkp*(s:string,d:string)=
  checkOrMkDir(d)
  try:             exec &"cp -vu --backup=t {s} {d}"; echo &":: Created {s} backup file inside {d}"
  except OSError:  quit &"::ERR Failed to backup {s} to {d}"
proc cpUpd*(s:string,d:string)=
  checkOrMkDir(d)
  try:             exec &"cp -vu {s} {d}"; echo &":: Copied {s} to {d}"
  except OSError:  quit &"::ERR Failed to copy {s} to {d}"
# Moving (mv)
proc mv*(s:string,d:string,t:string)=  #alias mv="mv -v "
  try:
    case t:
    of "dir":  mvDir(s,d);  echo &":: Moved dir {s} to {d}"
    of "file": mvFile(s,d); echo &":: Moved file {s} to {d}"
    else:      quit &"::ERR {t} is not a recognised type"
  except OSError:  quit &"::ERR Failed to move {s} to {d}"
# Removing (rm)
proc rm*(s:string)= rmDir(s,checkDir=true); echo &":: Removed directory {s}"
proc rm*(s:string,t:string)=  #alias rm="rm -rf "
  case t:
  of "dir":  rm(s)
  of "file": rmFile(s); echo &":: Removed file {s}"
  else:      quit &"::ERR {t} is not a recognised type"
# Zipping
proc zip_p(s:string,d:string)= # Zips files literally (absolute or relative, whatever is passed) (internal use only)
  try:             exec &"zip -vr {d} {s}"; echo &":: Created zip file {d} from the contents of {s}"
  except OSError:  quit &"::ERR Failed to create zip file {d} from {s}"
proc zipAbs*(s:string,d:string)= zip_p s, d
proc zip*(s:seq[string],d:string)=  #alias zip="zip -v ", but for Sequences of strings (file lists)
  var tseq=s
  echo &":: Splitting list of files {s}"
  for it in mitems(tseq): it = it.relativePath(getCurrentDir()); echo &": {it}"
  let t = tseq.join(" ")
  zip_p t, d
proc zip*(s:string,d:string)=
  let t = s.split(" "); zip t, d  #alias zip="zip -v "
proc zipd_p(s:string,d:string)= # Removes files from target zip file (internal use only)
  try:             exec &"zip -vd {d} {s}"; echo &":: Deleted {s} file from the contents of {d}"
  except OSError:  quit &"::ERR Failed to delete file {s} from {d}"
proc zipd*(s:string,d:string)= zipd_p s, d  #alias zipd="zip -vd"

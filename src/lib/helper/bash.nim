import os, strformat, strutils, sequtils

# File searching
proc findLatest*(f:string,d:string):string=
  var files:seq[string]
  try:
    for it in walkDirRec(d, checkDir=true):
      if f in it: files.add(it)
  except OSError: quit &"::ERR Tried to find latest version of {f}, but folder {d} doesn't exist"
  result = files[files.len-1] 

# Make Directories (md)
proc md*(d:string)=  #alias md="mkdir -v "
  if dirExists(d): echo &":: Directory {d} already exists. Ignoring its creation."; return
  try:             mkDir(d)#; echo &":: Created directory {d}"
  except OSError:  quit &"::ERR Failed to make directory {d}"
proc md*(d:string,o:bool):string=  md(d); result = if o: d else: ""  # Alias for creation and also assignment to variables
proc checkOrMkDir(f:string)=
  let d=splitFile(f).dir; if not dirExists(d): md d


# Copying
proc cp*(s:string,d:string,t:string)=  #alias cp="cp -v "
  checkOrMkDir(d)
  try:
    case t:
    of "dir":   cpDir(s,d)#;  echo &":: Copied dir {s} to {d}"
    of "file":  cpFile(s,d)#; echo &":: Copied file {s} to {d}"
    #of "ftodir":  copyFileToDir(s,d); echo &":: Copied file {s} to dir {d}"
  except OSError:  quit &"::ERR Failed to copy {s} to {d}"
proc cp*(s:string,d:string)=  # Assume copying file to folder when type is omitted
  let n = s.splitFile().name & s.splitFile().ext # Extract file name+ext
  cp s, d/n, "file" # copy source to dest/name
proc cpBkp*(s:string,d:string)=
  checkOrMkDir(d)
  try:             exec &"cp -vu --backup=t {s} {d}"; echo &":: Created {s} backup file inside {d}"
  except OSError:  quit &"::ERR Failed to backup {s} to {d}"
proc cpUpd*(s:string,d:string)=
  checkOrMkDir(d)
  try:             exec &"cp -vu {s} {d}"; echo &":: Copied {s} to {d}"
  except OSError:  quit &"::ERR Failed to copy {s} to {d}"
proc cpLatest*(d,f, t:string)   = cp findLatest(f,d), t             # Copy latest version of dir/file into targetDir
proc cpLatest*(d,f, td,t:string)= cp findLatest(f,d), td/t, "file"  # Copy latest version of dir/file into targetDir/targetFile

# Moving (mv)
proc mv*(s:string,d:string,t:string)=  #alias mv="mv -v "
  try:
    case t:
    of "dir":  mvDir(s,d)#;  echo &":: Moved dir {s} to {d}"
    of "file": mvFile(s,d)#; echo &":: Moved file {s} to {d}"
    else:      quit &"::ERR {t} is not a recognised type"
  except OSError:  quit &"::ERR Failed to move {s} to {d}"
proc mv*(s:string,d:string)= mv s, d, "file"  # Assume file when type is omitted

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
# Unzipping
proc unzip*(f,d:string; ow:bool)=
  let o = if ow: "-o" else: ""
  try:             exec &"unzip {o} -d {d} {f}"; echo &":: Extracted file {f} to folder {d}"
  except OSError:  quit &"::ERR Failed to extract file {f} to folder {d}"
proc unzip*(f:string,d:string)= unzip(f,d,true) # Assume overwrite when omitted

# Downloading
proc dl*(link:string)=
  try:             exec &"wget {link}"; echo &":: Downloaded file from link: {link}"
  except OSError:  quit &"::ERR Failed to download file from {link}"
proc dl*(link:string, o:string)=
  try:             exec &"wget -O {o} {link}"; echo &":: Downloaded file from link {link}  as {o}"
  except OSError:  quit &"::ERR Failed to download file from {link} as {o}"
proc dl*(link:string, c:bool)=  # Download without clobbing when c=false
  try:
    let nc = if c: "" else: "-nc"
    exec &"wget {nc} {link}"
    echo &":: Downloaded file from link: {link}"
  except OSError:  quit &"::ERR Failed to download file from {link}"



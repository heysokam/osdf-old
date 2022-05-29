import os, parseopt, strutils, strformat
import ./bash as sh
# Command line option parsing
func getBuildType*():string =
  var args = initOptParser(commandLineParams())
  for kind, key, val in args.getOpt():
    if kind in [cmdShortOption, cmdLongOption]:
      if key in ["build", "b"]: result = val
func verbose*():bool =
  result = false # default output is false, unless the opt is found
  var args = initOptParser(commandLineParams())
  for kind, key, val in args.getOpt():
    if kind in [cmdLongOption, cmdShortOption]:
      if key in ["verbose", "v"]: result = true
# Revision Number management
proc setRevNum*(v:int, f:string)=
  if not dirExists(splitFile(f).dir): sh.md splitFile(f).dir
  if not fileExists(f): exec &"touch {f}"; return
  writeFile f, $v
  echo &":: curr Revision is {v}, set in file {f}"
proc getRevNum*(f:string):int=
  if fileExists(f):
    let rev = int(parseInt(readFile(f)))
    result = rev
  else:
    echo &":: File {f} doesn't exist. Creating"
    setRevNum(-1, f)
    result = -1
proc updRevNum*(f:string) =
  var rev = getRevNum(f)
  echo &":: prev Revision is {rev}, stored in file {f}"
  setRevNum(rev+1, f)

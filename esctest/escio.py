import os
import select
import sys
import tty

from esc import ESC, BEL
import escargs
from esclog import LogDebug
import esctypes
import escoding

stdin_fd = None
stdout_fd = None
gSideChannel = None
use8BitControls = False

def Init():
  global stdout_fd
  global stdin_fd

  stdout_fd = os.fdopen(sys.stdout.fileno(), 'wb', 0)
  stdin_fd = os.fdopen(sys.stdin.fileno(), 'rb', 0)
  tty.setraw(stdin_fd)

def Shutdown():
  tty.setcbreak(stdin_fd)

def Write(s, sideChannelOk=True):
  if sideChannelOk and gSideChannel is not None:
    gSideChannel.write(escoding.to_binary(s))
  stdout_fd.write(escoding.to_binary(s))

def SetSideChannel(filename):
  global gSideChannel
  if filename is None:
    if gSideChannel:
      gSideChannel.close()
      gSideChannel = None
  else:
    gSideChannel = open(filename, "wb")

# Tests/conversion of C1 (8-Bit) Control Characters

def Is7BitControl(c):
  if len(c) == 2 and c.startswith(ESC):
    return 1
  return 0

def Is8BitControl(c):
  if len(c) == 1 and ord(c) >= 0x80 and ord(c) <= 0x9f:
    return 1
  return 0

def CmdChar(c):
  if use8BitControls:
    return chr(c)
  return ESC + chr(c - 0x40)

# C1 (8-Bit) Control Characters

def IND():
  return CmdChar(0x84)

def NEL():
  return CmdChar(0x85)

def HTS():
  return CmdChar(0x88)

def RI():
  return CmdChar(0x8d)

def SS2():
  return CmdChar(0x8e)

def SS3():
  return CmdChar(0x8f)

def DCS():
  return CmdChar(0x90)

def SPA():
  return CmdChar(0x96)

def EPA():
  return CmdChar(0x97)

def SOS():
  return CmdChar(0x98)

def DECID():
  return CmdChar(0x9a)

def CSI():
  return CmdChar(0x9b)

def ST():
  return CmdChar(0x9c)

def OSC():
  return CmdChar(0x9d)

def PM():
  return CmdChar(0x9e)

def APC():
  return CmdChar(0x9f)

# I/O functions for C1 (8-Bit) Control Characters

def WriteAPC(params, bel=False, requestsReport=False):
  str_params = list(map(str, params))
  if bel:
    terminator = BEL
  else:
    terminator = ST()
  sequence = APC() + "".join(str_params) + terminator
  LogDebug("Send sequence: " + sequence.replace(ESC, "<ESC>"))
  Write(sequence, sideChannelOk=not requestsReport)

def WriteOSC(params, bel=False, requestsReport=False):
  str_params = list(map(str, params))
  joined_params = ";".join(str_params)
  if bel:
    terminator = BEL
  else:
    terminator = ST()
  sequence = OSC() + joined_params + terminator
  LogDebug("Send sequence: " + sequence.replace(ESC, "<ESC>"))
  Write(sequence, sideChannelOk=not requestsReport)

def WriteDCS(introducer, params):
  Write(DCS() + introducer + params + ST())

def WriteCSI(prefix="", params=[], intermediate="", final="", requestsReport=False):
  if len(final) == 0:
    raise esctypes.InternalError("final must not be empty")
  def StringifyCSIParam(p):
    if p is None:
      return ""
    return str(p)
  str_params = list(map(StringifyCSIParam, params))

  # Remove trailing empty args
  while len(str_params) > 0 and str_params[-1] == "":
    str_params = str_params[:-1]

  joined_params = ";".join(str_params)
  sequence = CSI() + prefix + joined_params + intermediate + final
  LogDebug("Send sequence: " + sequence.replace(ESC, "<ESC>"))
  Write(sequence, sideChannelOk=not requestsReport)

def ReadOrDie(e):
  c = read(1)
  AssertCharsEqual(c, e)

def AssertCharsEqual(c, e):
  if c != e:
    raise esctypes.InternalError("Read %c (0x%02x), expected %c (0x%02x)" % (c, ord(c), e, ord(e)))

def ReadOSC(expected_prefix):
  """Read an OSC code starting with |expected_prefix|."""
  ReadOrDie(ESC)
  ReadOrDie(']')
  for c in expected_prefix:
    ReadOrDie(c)
  s = ""
  while not s.endswith(ST()):
    c = read(1)
    s += c
  return s[:-2]

def ReadCSI(expected_final, expected_prefix=None):
  """Read a CSI code ending with |expected_final| and returns an array of parameters. """

  c = read(1)
  if c == ESC:
    ReadOrDie('[')
  elif ord(c) != 0x9b:
    raise esctypes.InternalError("Read %c (0x%02x), expected CSI" % (c, ord(c)))

  params = []
  current_param = ""

  c = read(1)
  if not c.isdigit() and c != ';':
    if c == expected_prefix:
      c = read(1)
    else:
      raise esctypes.InternalError("Unexpected character 0x%02x" % ord(c))

  while True:
    if c == ";":
      params.append(int(current_param))
      current_param = ""
    elif '0' <= c <= '9':
      current_param += c
    else:
      # Read all the final characters, asserting they match.
      while True:
        AssertCharsEqual(c, expected_final[0])
        expected_final = expected_final[1:]
        if len(expected_final) > 0:
          c = read(1)
        else:
          break

      if current_param == "":
        params.append(None)
      else:
        params.append(int(current_param))
      break
    c = read(1)
  LogDebug("ReadCSI parameters: " + ";".join(map(str,params)))
  return params

def ReadDCS():
  """ Read a DCS code. Returns the characters between DCS and ST. """
  p = read(1)
  if p == ESC:
    ReadOrDie("P")
    p += "P"
  elif ord(p) == 0x90:
    p = "<DCS>"
  else:
    raise esctypes.InternalError("Read %c (0x%02x), expected DCS" % (p, ord(p)))

  result = ""
  while not result.endswith(ST()):
    c = read(1)
    result += c
  LogDebug("Read response: " + (p + result).replace(ESC, "<ESC>"))
  if result.endswith(chr(0x9c)):
    return result[:-1]
  return result[:-2]

def read(n):
  """Try to read n bytes. Times out if it takes more than 1
  second to read any given byte."""
  s = ""
  f = sys.stdin.fileno()
  for _ in range(n):
    r, w, e = select.select([f], [], [], escargs.args.timeout)
    if f not in r:
      raise esctypes.InternalError("Timeout waiting to read.")
    s += escoding.to_string(os.read(f, 1))
  return s

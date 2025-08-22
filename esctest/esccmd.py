from esc import ESC

from escutil import AssertVTLevel
from escutil import GetIndexedColors

import escargs
import escio
import escoding

# DECSET/DECRESET
Allow80To132 = 40  # Allow 80->132 Mode
ALTBUF = 47  # Switch to alt buf
DECAAM = 100
DECANM = 2
DECARM = 8
DECARSM = 98
DECAWM = 7  # Autowrap
DECBKM = 67
DECCANSM = 101
DECCKM = 1
DECCOLM = 3  # 132-column mode
DECCRTSM = 97
DECESKM = 104
DECHCCM = 60
DECHDPXM = 103
DECHEBM = 35
DECHEM = 36
DECKBUM = 68
DECKPM = 81
DECLRMM = 69  # Left/right margin enabled
DECMCM = 99
DECNAKB = 57
DECNCSM = 95
DECNCSM = 95  # Clear screen on enabling column mode
DECNKM = 66
DECNRCM = 42
DECNULM = 102
DECOM = 6  # Origin mode
DECOSCNM = 106
DECPCCM = 64
DECPEX = 19
DECPFF = 18
DECRLCM = 96
DECRLM = 34  # Right-to-left mode
DECSCLM = 4
DECSCNM = 5
DECTCEM = 25
DECVCCM = 61
DECXRLM = 73
MoreFix = 41  # Work around bug in more(1) (see details in test_DECSET_MoreFix)
OPT_ALTBUF = 1047  # Switch to alt buf. DECRESET first clears the alt buf.
OPT_ALTBUF_CURSOR = 1049  # Like 1047 but saves/restores main screen's cursor position.
ReverseWrapExtend = 1045  # Extended Reverse-wraparound mode (only works on conjunction with DECAWM)
ReverseWrapInline = 45    # Reverse-wraparound mode (only works on conjunction with DECAWM)
SaveRestoreCursor = 1048  # Save cursor as in DECSC.

# Xterm Winops (CSI Ps t)
WINOP_DEICONIFY = 1
WINOP_ICONIFY = 2
WINOP_MOVE = 3
WINOP_RESIZE_PIXELS = 4
WINOP_RESIZE_CHARS = 8
WINOP_MAXIMIZE = 9
WINOP_FULLSCREEN = 10
WINOP_REPORT_WINDOW_STATE = 11
WINOP_REPORT_WINDOW_POSITION = 13
WINOP_REPORT_WINDOW_SIZE_PIXELS = 14
WINOP_REPORT_SCREEN_SIZE_PIXELS = 15
WINOP_REPORT_CHAR_SIZE_PIXELS = 16
WINOP_REPORT_TEXT_AREA_CHARS = 18
WINOP_REPORT_SCREEN_SIZE_CHARS = 19
WINOP_REPORT_ICON_LABEL = 20
WINOP_REPORT_WINDOW_TITLE = 21
WINOP_PUSH_TITLE = 22
WINOP_POP_TITLE = 23

# WINOP_MAXIMIZE sub-commands
WINOP_MAXIMIZE_EXIT = 0
WINOP_MAXIMIZE_HV = 1
WINOP_MAXIMIZE_V = 2
WINOP_MAXIMIZE_H = 3

# WINOP_FULLSCREEN sub-commands
WINOP_FULLSCREEN_EXIT = 0
WINOP_FULLSCREEN_ENTER = 1
WINOP_FULLSCREEN_TOGGLE = 2

# WINOP_PUSH_TITLE sub-commands
WINOP_PUSH_TITLE_ICON_AND_WINDOW = 0
WINOP_PUSH_TITLE_ICON = 1
WINOP_PUSH_TITLE_WINDOW = 2

# WINOP_POP_TITLE sub-commands
WINOP_POP_TITLE_ICON_AND_WINDOW = 0
WINOP_POP_TITLE_ICON = 1
WINOP_POP_TITLE_WINDOW = 2

# DECDSR
DECCKSR = 63
DECMSR = 62
DECXCPR = 6
DSRCPR = 6
DSRDECLocatorStatus = 55
DSRIntegrityReport = 75
DSRKeyboard = 26
DSRLocatorId = 56
DSRMultipleSessionStatus = 85
DSRPrinterPort = 15
DSRUDKLocked = 25
DSRXtermLocatorStatus = 55

# SM/RM
EBM = 19
FEAM = 13
FETM = 14
GATM = 1
HEM = 10
IRM = 4
KAM = 2
LNM = 20
MATM = 15
PUM = 11
SATM = 17
SRM = 12
SRTM = 5
TSM = 18
TTM = 16
VEM = 7

# SMTitle
SET_HEX = 0
QUERY_HEX = 1
SET_UTF8 = 2
QUERY_UTF8 = 3

def SCORC():
  """Restore cursor."""
  escio.WriteCSI(final="u")

def SCOSC():
  """Save cursor."""
  escio.WriteCSI(final="s")

def APC():
  """Application Program Command."""
  escio.Write(escio.APC())

def CBT(Pn=None):
  """Move cursor back by Pn tab stops or to left margin. Default is 1."""
  if Pn is None:
    params = []
  else:
    params = [Pn]
  escio.WriteCSI(params=params, final="Z")

def ChangeColor(*args):
  params = [4]
  isQuery = True
  try:
    params.index("?")
  except:
    isQuery = False
  params.extend(args)
  escio.WriteOSC(params, requestsReport=isQuery)

def ChangeDynamicColor(*args):
  params = []
  isQuery = True
  try:
    params.index("?")
  except:
    isQuery = False
  params.extend(args)
  escio.WriteOSC(params, requestsReport=isQuery)

def ChangeSpecialColor(*args):
  if len(args) > 0 and int(args[0]) >= 10:
    params = []
  else:
    params = [4]
  isQuery = True
  try:
    params.index("?")
  except:
    isQuery = False
  params.extend(args)
  for p in range(1, len(params)):
    try:
      q = int(params[p])
      if q < 9:
        params[p] = str(q + GetIndexedColors())
    except:
      pass
  escio.WriteOSC(params, requestsReport=isQuery)

def ChangeSpecialColor2(*args):
  if len(args) > 0 and int(args[0]) >= 10:
    params = []
  else:
    params = [5]
  isQuery = True
  try:
    params.index("?")
  except:
    isQuery = False
  params.extend(args)
  escio.WriteOSC(params, requestsReport=isQuery)

def ChangeWindowTitle(title, bel=False, suppressSideChannel=False):
  """Change the window title."""
  escio.WriteOSC(params=["2", title], bel=bel, requestsReport=suppressSideChannel)

def ChangeIconTitle(title, bel=False, suppressSideChannel=False):
  """Change the icon (tab) title."""
  escio.WriteOSC(params=["1", title], bel=bel, requestsReport=suppressSideChannel)

def ChangeWindowAndIconTitle(title, bel=False, suppressSideChannel=False):
  """Change the window and icon (tab) title."""
  escio.WriteOSC(params=["0", title],
                 bel=bel,
                 requestsReport=suppressSideChannel)
def CHA(Pn=None):
  """Move cursor to Pn column, or first column by default."""
  if Pn is None:
    params = []
  else:
    params = [Pn]
  escio.WriteCSI(params=params, final="G")

def CHT(Ps=None):
  """Move cursor forward by Ps tab stops (default is 1)."""
  if Ps is None:
    params = []
  else:
    params = [Ps]
  escio.WriteCSI(params=params, final="I")

def CNL(Ps=None):
  """Cursor down Ps times and to the left margin."""
  if Ps is None:
    params = []
  else:
    params = [Ps]
  escio.WriteCSI(params=params, final="E")

def CPL(Ps=None):
  """Cursor up Ps times and to the left margin."""
  if Ps is None:
    params = []
  else:
    params = [Ps]
  escio.WriteCSI(params=params, final="F")

def CUB(Ps=None):
  """Cursor left Ps times."""
  if Ps is None:
    params = []
  else:
    params = [Ps]
  escio.WriteCSI(params=params, final="D")

def CUD(Ps=None):
  """Cursor down Ps times."""
  if Ps is None:
    params = []
  else:
    params = [Ps]
  escio.WriteCSI(params=params, final="B")

def CUF(Ps=None):
  """Cursor right Ps times."""
  if Ps is None:
    params = []
  else:
    params = [Ps]
  escio.WriteCSI(params=params, final="C")

def CUP(point=None, row=None, col=None):
  """ Move cursor to |point| """
  if point is None and row is None and col is None:
    escio.WriteCSI(params=[], final="H")
  elif point is None:
    if row is None:
      row = ""
    if col is None:
      escio.WriteCSI(params=[row], final="H")
    else:
      escio.WriteCSI(params=[row, col], final="H")
  else:
    escio.WriteCSI(params=[point.y(), point.x()], final="H")

def CUU(Ps=None):
  """Cursor up Ps times."""
  if Ps is None:
    params = []
  else:
    params = [Ps]
  escio.WriteCSI(params=params, final="A")

def DA(Ps=None):
  """Request primary device attributes."""
  if Ps is None:
    params = []
  else:
    params = [Ps]
  escio.WriteCSI(params=params, final="c")

def DA2(Ps=None):
  """Request secondary device attributes."""
  if Ps is None:
    params = []
  else:
    params = [Ps]
  escio.WriteCSI(params=params, prefix='>', final="c")

def DCH(Ps=None):
  """Delete Ps characters at cursor."""
  if Ps is None:
    params = []
  else:
    params = [Ps]
  escio.WriteCSI(params=params, final="P")

def DCS():
  """Device control string. Prefixes various commands."""
  escio.Write(escio.DCS())

def DECALN():
  """Write test pattern."""
  escio.Write(ESC + "#8")

def DECBI():
  """Index left, scrolling region right if cursor at margin."""
  escio.Write(ESC + "6")

def DECCRA(source_top=None, source_left=None, source_bottom=None,
           source_right=None, source_page=None, dest_top=None,
           dest_left=None, dest_page=None):
  """Copy a region."""
  params = [source_top,
            source_left,
            source_bottom,
            source_right,
            source_page,
            dest_top,
            dest_left,
            dest_page]
  escio.WriteCSI(params=params, intermediate="$", final="v")

def DECDC(Pn=None):
  """Delete column at cursor."""
  if Pn is not None:
    params = [Pn]
  else:
    params = []
  escio.WriteCSI(params=params, intermediate="'", final="~")

def DECDHL(x):
  """Double-width, double-height line.
     x = 3: top half
     x = 4: bottom half"""
  escio.Write(ESC + "#" + str(x))

def DECDSR(Ps, Pid=None, suppressSideChannel=False):
  """Send device status request. Does not read response."""
  if Ps is None:
    params = []
  else:
    if Pid is None:
      params = [Ps]
    else:
      params = [Ps, Pid]
  escio.WriteCSI(params=params, prefix='?', requestsReport=suppressSideChannel, final='n')

def DECELF(Pn=None):
  """Enable local functions."""
  AssertVTLevel(4, "DECELF")
  if Pn is not None:
    params = [Pn]
  else:
    params = []
  escio.WriteCSI(params=params, intermediate="+", final="q")

def DECERA(Pt, Pl, Pb, Pr):
  """Erase rectangle."""
  escio.WriteCSI(params=[Pt, Pl, Pb, Pr], intermediate="$", final="z")

def DECFI():
  """Forward index."""
  escio.Write(ESC + "9")

def DECFRA(Pch, Pt, Pl, Pb, Pr):
  """Fill rectangle with Pch"""
  escio.WriteCSI(params=[Pch, Pt, Pl, Pb, Pr], intermediate="$", final="x")

def DECIC(Pn=None):
  """Insert column at cursor."""
  if Pn is not None:
    params = [Pn]
  else:
    params = []
  escio.WriteCSI(params=params, intermediate="'", final="}")

def DECID():
  """Obsolete form of DA."""
  escio.Write(escio.DECID())

def DECLFKC(Pn=None):
  """Enable local function function key control."""
  AssertVTLevel(4, "DECLFKC")
  if Pn is not None:
    params = [Pn]
  else:
    params = []
  escio.WriteCSI(params=params, intermediate="*", final="}")

def DECRC():
  """Restore the cursor and resets various attributes."""
  escio.Write(ESC + "8")

def DECRQCRA(Pid, Pp=None, rect=None):
  """Compute the checksum (16-bit sum of ordinals) in a rectangle."""
  AssertVTLevel(4, "DECRQCRA")

  params = [Pid]

  if Pp is not None:
    params += [Pp]
  elif Pp is None and rect is not None:
    params += [""]

  if rect is not None:
    params.extend(rect.params())

  escio.WriteCSI(params=params, intermediate='*', final='y', requestsReport=True)

def DECRQM(mode, DEC):
  """Requests if a mode is set or not."""
  AssertVTLevel(3, "DECRQM")
  if DEC:
    escio.WriteCSI(params=[mode], intermediate='$', prefix='?', final='p')
  else:
    escio.WriteCSI(params=[mode], intermediate='$', final='p')

def DECRQSS(Pt):
  AssertVTLevel(3, "DECRQSS")
  escio.WriteDCS("$q", Pt)

def DECRESET(Pm):
  """Reset the parameter |Pm|."""
  escio.WriteCSI(params=[Pm], prefix='?', final='l')

def DECSACE(Ps=None):
  """Set attribute change extent"""
  AssertVTLevel(4, "DECSACE")
  if Ps is None:
    params = []
  else:
    params = [Ps]
  escio.WriteCSI(params=params, intermediate="*", final="x")

def DECSASD(Ps=None):
  """Direct output to status line if Ps is 1, to main display if 0."""
  AssertVTLevel(3, "DECSASD")
  if Ps is None:
    params = []
  else:
    params = [Ps]
  escio.WriteCSI(params=params, intermediate='$', final="}")

def DECSC():
  """Saves the cursor."""
  escio.Write(ESC + "7")

def DECSCA(Ps=None):
  """Turn on character protection if Ps is 1, off if 0."""
  AssertVTLevel(2, "DECSCA")
  if Ps is None:
    params = []
  else:
    params = [Ps]
  escio.WriteCSI(params=params, intermediate='"', final="q")

def DECSCL(level, sevenBit=None):
  """Level should be one of 61, 62, 63, or 64. sevenBit can be 0 or 1, or not
  specified."""
  if sevenBit is None:
    params = [level]
  else:
    params = [level, sevenBit]
  escio.WriteCSI(params=params, intermediate='"', final="p")

def DECSCUSR(Ps=None):
  """Set cursor style 0 through 6, or default of 1."""
  if Ps is None:
    params = []
  else:
    params = [Ps]
  escio.WriteCSI(params=params, intermediate=' ', final="q")

def DECSED(Ps=None):
  """Like ED but respects character protection."""
  if Ps is None:
    params = []
  else:
    params = [Ps]
  escio.WriteCSI(params=params, prefix='?', final="J")

def DECSEL(Ps=None):
  """Like EL but respects character protection."""
  if Ps is None:
    params = []
  else:
    params = [Ps]
  escio.WriteCSI(params=params, prefix='?', final="K")

def DECSERA(Pt, Pl, Pb, Pr):
  """Selective erase rectangle."""
  AssertVTLevel(4, "DECSERA")
  escio.WriteCSI(params=[Pt, Pl, Pb, Pr], intermediate="$", final="{")

def DECSET(Pm):
  """Set the parameter |Pm|."""
  escio.WriteCSI(params=[Pm], prefix='?', final='h')

def DECSLRM(Pl, Pr):
  """Set the left and right margins."""
  AssertVTLevel(4, "DECSLRM")
  escio.WriteCSI(params=[Pl, Pr], final='s')

def DECSMKR(Pn=None):
  """Set modifier key reporting."""
  AssertVTLevel(4, "DECSMKR")
  if Pn is not None:
    params = [Pn]
  else:
    params = []
  escio.WriteCSI(params=params, intermediate="+", final="r")

def DECSNLS(Pn=None):
  """Set number of lines per screen."""
  if Pn is not None:
    params = [Pn]
  else:
    params = []
  escio.WriteCSI(params=params, intermediate="*", final="|")

def DECSSDT(Pn=None):
  """Select status display type."""
  AssertVTLevel(3, "DECSSDT")
  if Pn is None:
    params = []
  else:
    params = [Pn]
  escio.WriteCSI(params=params, intermediate='$', final='~')

def DECSTBM(top=None, bottom=None):
  """Set Scrolling Region [top;bottom] (default = full size of window)."""
  params = []
  if top is not None:
    params.append(top)
  if bottom is not None:
    params.append(bottom)

  escio.WriteCSI(params=params, final="r")

def DECSTR():
  """Soft reset."""
  escio.WriteCSI(prefix='!', final='p')

def DL(Pn=None):
  """Delete |Pn| lines at the cursor. Default value is 1."""
  if Pn is None:
    params = []
  else:
    params = [Pn]
  escio.WriteCSI(params=params, final="M")

def DSR(Ps, suppressSideChannel=False):
  """Send device status request. Does not read response."""
  if Ps is None:
    params = []
  else:
    params = [Ps]
  escio.WriteCSI(params=params, requestsReport=suppressSideChannel, final='n')

def ECH(Pn=None):
  """Erase |Pn| characters starting at the cursor. Default value is 1."""
  if Pn is None:
    params = []
  else:
    params = [Pn]
  escio.WriteCSI(params=params, final="X")

def ED(Ps=None):
  """Erase characters, clearing display attributes. Works in or out of scrolling regions.

  Ps = 0 (default): From the cursor through the end of the display
  Ps = 1: From the beginning of the display through the cursor
  Ps = 2: The complete display
  """
  if Ps is None:
    params = []
  else:
    params = [Ps]
  escio.WriteCSI(params=params, final="J")

def EL(Ps=None):
  """Erase in the active line.

  Ps = 0 (default): Erase to right of cursor
  Ps = 1: Erase to left of cursor
  Ps = 2: Erase whole line
  """
  if Ps is None:
    params = []
  else:
    params = [Ps]
  escio.WriteCSI(params=params, final="K")

def EPA():
  """End protected area."""
  escio.Write(escio.EPA())

def HPA(Pn=None):
  """Position the cursor at the Pn'th column. Default value is 1."""
  if Pn is None:
    params = []
  else:
    params = [Pn]
  escio.WriteCSI(params=params, final="`")

def HPR(Pn=None):
  """Position the cursor at the Pn'th column relative to its current position.
  Default value is 1."""
  if Pn is None:
    params = []
  else:
    params = [Pn]
  escio.WriteCSI(params=params, final="a")

def HTS():
  """Set a horizontal tab stop."""
  escio.Write(escio.HTS())

def HVP(point=None, row=None, col=None):
  """ Move cursor to |point| """
  if point is None and row is None and col is None:
    escio.WriteCSI(params=[], final="H")
  elif point is None:
    if row is None:
      row = ""
    if col is None:
      escio.WriteCSI(params=[row], final="H")
    else:
      escio.WriteCSI(params=[row, col], final="H")
  else:
    escio.WriteCSI(params=[point.y(), point.x()], final="f")

def ICH(Pn=None):
  """ Insert |Pn| blanks at cursor. Cursor does not move. """
  if Pn is None:
    params = []
  else:
    params = [Pn]
  escio.WriteCSI(params=params, final="@")

def IL(Pn=None):
  """Insert |Pn| blank lines after the cursor. Default value is 1."""
  if Pn is None:
    params = []
  else:
    params = [Pn]
  escio.WriteCSI(params=params, final="L")

def IND():
  """Move cursor down one line."""
  escio.Write(escio.IND())

def ManipulateSelectionData(Pc="", Pd=None):
  params = ["52", Pc]
  if Pd is not None:
    params.append(escoding.strip_binary(Pd))
  escio.WriteOSC(params)

def NEL():
  """Index plus carriage return."""
  escio.Write(escio.NEL())

def PM():
  """Privacy message."""
  escio.Write(escio.PM())

def REP(Ps=None):
  """Repeat the preceding character |Ps| times. Undocumented default is 1."""
  if Ps is None:
    params = []
  else:
    params = [Ps]
  escio.WriteCSI(params=params, final="b")

def ResetSpecialColor(*args):
  params = ["105"]
  params.extend(args)
  escio.WriteOSC(params)

def ResetColor(c=""):
  escio.WriteOSC(["104", c])

def ResetDynamicColor(c):
  escio.WriteOSC([str(c)])

def RI():
  """Move cursor up one line."""
  escio.Write(escio.RI())

def RIS():
  """Reset."""
  escio.Write(ESC + "c")

def RM(Pm=None):
  """Reset mode."""
  if Pm is None:
    params = []
  else:
    params = [Pm]
  escio.WriteCSI(params=params, final="l")

def RM_Title(Ps1, Ps2=None):
  """Reset title mode."""
  params = [Ps1]
  if Ps2 is not None:
    params.append(Ps2)
  escio.WriteCSI(params=params, prefix=">", final="T")

def SD(Ps=None):
  """Scroll down by |Ps| lines. Default value is 1."""
  if Ps is None:
    params = []
  else:
    params = [Ps]
  escio.WriteCSI(params=params, final="T")

def SM(Pm=None):
  """Set mode."""
  if Pm is None:
    params = []
  else:
    params = [Pm]
  escio.WriteCSI(params=params, final="h")

def SM_Title(Ps1, Ps2=None):
  """Set title mode."""
  params = [Ps1]
  if Ps2 is not None:
    params.append(Ps2)
  escio.WriteCSI(params=params, prefix=">", final="t")

def SOS():
  """Start of string."""
  escio.Write(escio.SOS())

def SPA():
  """Start protected area."""
  escio.Write(escio.SPA())

def SGR(*args):
  """Select graphic rendition. Params is an array of numbers."""
  escio.WriteCSI(params=args, final="m")

def ST():
  """String terminator."""
  escio.Write(escio.ST())

def SU(Ps=None):
  """Scroll up by |Ps| lines. Default value is 1."""
  if Ps is None:
    params = []
  else:
    params = [Ps]
  escio.WriteCSI(params=params, final="S")

def TBC(Ps=None):
  """Clear tab stop. Default arg is 0 (clear tabstop at cursor)."""
  if Ps is None:
    params = []
  else:
    params = [Ps]
  escio.WriteCSI(params=params, final="g")

def VPA(Ps=None):
  """Move to line |Ps|. Default value is 1."""
  if Ps is None:
    params = []
  else:
    params = [Ps]
  escio.WriteCSI(params=params, final="d")

def VPR(Ps=None):
  """Move down by |Ps| rows. Default value is 1."""
  if Ps is None:
    params = []
  else:
    params = [Ps]
  escio.WriteCSI(params=params, final="e")

def XTERM_RESTORE(Ps=None):
  """Restore given DEC private mode parameters."""
  if Ps is None:
    params = []
  else:
    params = [Ps]
  escio.WriteCSI(params=params, prefix="?", final="r")

def XTERM_SAVE(Ps=None):
  """Save given DEC private mode parameters."""
  if Ps is None:
    params = []
  else:
    params = [Ps]
  escio.WriteCSI(params=params, prefix="?", final="s")

def XTERM_WINOPS(Ps1=None, Ps2=None, Ps3=None):
  if Ps3 is not None:
    params = [Ps1, Ps2, Ps3]
  elif Ps2 is not None:
    params = [Ps1, Ps2]
  elif Ps1 is not None:
    params = [Ps1]
  else:
    params = []
  requestsReport = Ps1 in [WINOP_REPORT_WINDOW_STATE,
                           WINOP_REPORT_WINDOW_POSITION,
                           WINOP_REPORT_WINDOW_SIZE_PIXELS,
                           WINOP_REPORT_TEXT_AREA_CHARS,
                           WINOP_REPORT_SCREEN_SIZE_CHARS,
                           WINOP_REPORT_ICON_LABEL,
                           WINOP_REPORT_WINDOW_TITLE]
  escio.WriteCSI(params=params, final="t", requestsReport=requestsReport)

def ReverseWraparound():
  '''
  Return an appropriate reverse-wrap private mode.  Some tests will fail for
  xterm in patches 381, 392 since the extended mode was added in 383 to help
  with (rare) scripts which require the feature.  See the longer note in
  test_BS_ReverseWrapGoesToBottom.
  '''
  if escargs.args.xterm_reverse_wrap >= 383:
    return ReverseWrapExtend	# since xterm 383
  return ReverseWrapInline	# since xterm 380

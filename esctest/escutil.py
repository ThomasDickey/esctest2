import functools
import traceback
import re

import esc
import escargs
import esccmd
import escio
from esclog import LogInfo, LogDebug
import esctypes
from esctypes import Point, Size, Rect

gNextId = 1
gHaveAsserted = False

gCharSizePixels = Size(0, 0)
gFrameSizePixels = Size(0, 0)
gScreenSizePixels = Size(0, 0)
gCanQueryShellSize = -1

gNumIndexedColors = -1

KNOWN_BUG_TERMINALS = "known_bug_terminals"

def Raise(e):
  if not escargs.args.force:
    raise e

def AssertGE(actual, expected):
  global gHaveAsserted
  gHaveAsserted = True
  if actual < expected:
    Raise(esctypes.TestFailure(actual, expected))

def AssertEQ(actual, expected):
  global gHaveAsserted
  gHaveAsserted = True
  if actual != expected:
    Raise(esctypes.TestFailure(actual, expected))

def AssertTrue(value, details=None):
  if escargs.args.force:
    return
  global gHaveAsserted
  gHaveAsserted = True
  if value is not True:
    Raise(esctypes.TestFailure(value, True, details))

def GetIconTitle():
  esccmd.XTERM_WINOPS(esccmd.WINOP_REPORT_ICON_LABEL)
  return escio.ReadOSC("L")

def GetWindowTitle():
  esccmd.XTERM_WINOPS(esccmd.WINOP_REPORT_WINDOW_TITLE)
  return escio.ReadOSC("l")

def CanQueryShellSize():
  """Determine if the terminal responds to a request for shell-window size vs
  text-window size.

  xterm has two windows of interest:
  a) the text-window
  b) the shell-window (i.e., outer window).

  The shell-window includes the title and other decorations.  Unless those are
  suppressed (an option in some window managers), it will be larger than the
  terminal's character-cell window.  In any case, it also has a border which is
  normally present.

  The window operations report for the window-size in pixels was added to xterm
  to provide an alternate way to measure the text-window (and indirectly, the
  font size).  That is the default operation.  Alternatively, the size of the
  shell window can be returned."""
  global gCanQueryShellSize
  if gCanQueryShellSize < 0:
    gCanQueryShellSize = 0
    # check for the default operation
    esccmd.XTERM_WINOPS(esccmd.WINOP_REPORT_WINDOW_SIZE_PIXELS)
    params = escio.ReadCSI("t")
    if params[0] == 4 and len(params) >= 3:
      # TODO: compare size_1 with result from text-window size
      # If it is larger, then that's a special case.
      size_1 = Size(params[2], params[1])
      gCanQueryShellSize = 1
      # check for the window-shell operation
      esccmd.XTERM_WINOPS(esccmd.WINOP_REPORT_WINDOW_SIZE_PIXELS, 2)
      params = escio.ReadCSI("t")
      if params[0] == 4 and len(params) >= 3:
        size_2 = Size(params[2], params[1])
        if size_2.height() > size_1.height() and \
           size_2.width() > size_1.width():
          gCanQueryShellSize = 2
  return gCanQueryShellSize

def GetWindowSizePixels():
  """Returns a Size giving the window's size in pixels."""
  if CanQueryShellSize() == 2:
    esccmd.XTERM_WINOPS(esccmd.WINOP_REPORT_WINDOW_SIZE_PIXELS, 2)
  else:
    esccmd.XTERM_WINOPS(esccmd.WINOP_REPORT_WINDOW_SIZE_PIXELS)
  params = escio.ReadCSI("t")
  AssertTrue(params[0] == 4)
  AssertTrue(len(params) >= 3)
  return Size(params[2], params[1])

def GetScreenSizePixels():
  """Returns a Size giving the screen's size in pixels.

  The "screen" refers to the X display on which xterm is running.
  Because that does not change as a result of these tests, we
  cache a value to help with performance."""
  global gScreenSizePixels
  if gScreenSizePixels.height() == 0:
    if escargs.args.expected_terminal == "xterm":
      esccmd.XTERM_WINOPS(esccmd.WINOP_REPORT_SCREEN_SIZE_PIXELS)
      params = escio.ReadCSI("t")
      AssertTrue(params[0] == 5)
      AssertTrue(len(params) >= 3)
      gScreenSizePixels = Size(params[2], params[1])
    else:
      # iTerm2 doesn't support esccmd.WINOP_REPORT_SCREEN_SIZE_PIXELS so just fake it.
      gScreenSizePixels = Size(1024, 768)
    LogDebug("size of SCREEN "
             + str(gScreenSizePixels.height()) + "x"
             + str(gScreenSizePixels.width()))
  return gScreenSizePixels

def GetFrameSizePixels():
  """Returns a Size giving the terminal's border/title frame size.

  The frame size is used to adjust the expected error in window-resizing
  tests which modify the shell window's size.
  """
  global gFrameSizePixels
  if gFrameSizePixels.height() == 0:
    GetCharSizePixels()
    outer = GetWindowSizePixels()
    inner = GetScreenSize()
    check = Size(inner.width() * gCharSizePixels.width(),
                 inner.height() * gCharSizePixels.height())
    gFrameSizePixels = Size(outer.width() - check.width(),
                            outer.height() - check.height())
    LogDebug("size of FRAME "
             + str(gFrameSizePixels.height()) + "x"
             + str(gFrameSizePixels.width()))
  return gFrameSizePixels

def GetCharSizePixels():
  """Returns a Size giving the font's character-size in pixels.

  While xterm can be told to change its font, none of these tests exercise
  that feature.  We cache a value to improve performance.
  """
  global gCharSizePixels
  if gCharSizePixels.height() == 0:
    esccmd.XTERM_WINOPS(esccmd.WINOP_REPORT_CHAR_SIZE_PIXELS)
    params = escio.ReadCSI("t")
    AssertTrue(params[0] == 6)
    AssertTrue(len(params) >= 3)
    gCharSizePixels = Size(params[2], params[1])
    LogDebug("size of CHARS " + str(gCharSizePixels.height()) + "x" + str(gCharSizePixels.width()))
  return gCharSizePixels

def GetWindowPosition():
  """Returns a Point giving the window's origin in screen pixels.

  This is the upper-left corner of xterm's shell-window, and is usually
  not the same as the upper-left corner of the terminal's character cell
  grid."""
  esccmd.XTERM_WINOPS(esccmd.WINOP_REPORT_WINDOW_POSITION)
  params = escio.ReadCSI("t")
  AssertTrue(params[0] == 3)
  AssertTrue(len(params) >= 3)
  return Point(params[1], params[2])

def GetIsIconified():
  esccmd.XTERM_WINOPS(esccmd.WINOP_REPORT_WINDOW_STATE)
  params = escio.ReadCSI("t")
  AssertTrue(params[0] in [1, 2], "Params are " + str(params))
  return params[0] == 2

def GetCursorPosition():
  esccmd.DSR(esccmd.DSRCPR, suppressSideChannel=True)
  params = escio.ReadCSI("R")
  return Point(int(params[1]), int(params[0]))

def GetScreenSize():
  """Return the terminal's screen-size in characters.

  The size is reported for the terminal's character-cell window,
  which is smaller than the shell-window."""
  esccmd.XTERM_WINOPS(esccmd.WINOP_REPORT_TEXT_AREA_CHARS)
  params = escio.ReadCSI("t")
  return Size(params[2], params[1])

def GetDisplaySize():
  esccmd.XTERM_WINOPS(esccmd.WINOP_REPORT_SCREEN_SIZE_CHARS)
  params = escio.ReadCSI("t")
  return Size(params[2], params[1])

def GetIndexedColors():
  global gNumIndexedColors
  if gNumIndexedColors <= 0:
    try:
      gNumIndexedColors = 16
      hexname = "436F"      # "Co", in hexadecimal
      escio.WriteDCS("+q", hexname)
      check = escio.ReadDCS()
      myprefix = "1+r" + hexname + "="
      trimmed = check.replace(myprefix, "")
      if trimmed != check:
        hexvalue = trimmed
        strvalue = bytearray.fromhex(hexvalue).decode(encoding="Latin1")
        gNumIndexedColors = int(strvalue)
      if gNumIndexedColors < 8:
        gNumIndexedColors = 8
      elif gNumIndexedColors > 256:
        gNumIndexedColors = 256
    except Exception:
      gNumIndexedColors = 16
  return gNumIndexedColors

def AssertVTLevel(minimum, reason):
  """Checks that the vtLevel is at least minimum.

  This is used to find bugs in tests that are not properly annotated with a vt
  level.
  """
  if esc.vtLevel < minimum:
    if reason is not None:
      LogInfo("BUG: " + reason + " feature is not supported at this level")
    raise esctypes.InsufficientVTLevel(esc.vtLevel, minimum)

def PrintableChar(c):
  return c if ord(' ') <= c <= ord('~') else '?'

def AssertScreenCharsInRectEqual(rect, expected_lines):
  global gHaveAsserted
  gHaveAsserted = True

  AssertVTLevel(4, "checksum")

  if rect.height() != len(expected_lines):
    raise esctypes.InternalError(
        "Height of rect (%d) does not match number of expected lines (%d)" % (
            rect.height(),
            len(expected_lines)))

  # Check each point individually. The dumb checksum algorithm can't distinguish
  # "ab" from "ba", so equivalence of two multiple-character rects means nothing.

  # |actual| and |expected| will form human-readable arrays of lines
  actual = []
  expected = []
  # Additional information about mismatches.
  errorLocations = []
  for point in rect.points():
    y = point.y() - rect.top()
    x = point.x() - rect.left()
    expected_line = expected_lines[y]
    if rect.width() != len(expected_line):
      fmt = ("Width of rect (%d) does not match number of characters in expected line " +
             "index %d, coordinate %d (its length is %d)")
      raise esctypes.InternalError(
          fmt % (rect.width(),
                 y,
                 point.y(),
                 len(expected_lines[y])))

    expected_checksum = ord(expected_line[x])

    actual_checksum = GetChecksumOfRect(Rect(left=point.x(),
                                             top=point.y(),
                                             right=point.x(),
                                             bottom=point.y()))
    # esctest is only asking for one cell at a time, which simplifies things.
    if escargs.args.expected_terminal == "xterm":
      if escargs.args.xterm_checksum < 279:
        actual_checksum = 0x10000 - actual_checksum
        # DEC terminals trim trailing blanks
        if expected_checksum == 0 and actual_checksum == 32:
          actual_checksum = 0

    if len(actual) <= y:
      actual.append("")
    if actual_checksum == 0:
      actual[y] += '.'
    elif actual_checksum < 256:
      actual[y] += chr(actual_checksum)

    if len(expected) <= y:
      expected.append("")
    if expected_checksum == 0:
      expected[y] += '.'
    elif expected_checksum < 256:
      expected[y] += chr(expected_checksum)

    if expected_checksum != actual_checksum:
      errorLocations.append("At %s expected '%c' (0x%02x) but got '%c' (0x%02x)" % (
          str(point),
          PrintableChar(expected_checksum),
          expected_checksum,
          PrintableChar(actual_checksum),
          actual_checksum))

  if len(errorLocations) > 0:
    Raise(esctypes.ChecksumException(errorLocations, actual, expected))

def GetChecksumOfRect(rect):
  global gNextId
  Pid = gNextId
  gNextId += 1
  esccmd.DECRQCRA(Pid, 0, rect)
  params = escio.ReadDCS()

  str_pid = str(Pid)
  if not params.startswith(str_pid):
    if escargs.args.expected_terminal == "iTerm2":
      # workaround for known bug to let screen-scraping tests work...
      str_pid = re.sub(r'[^0-9].*$', "", params)
    else:
      Raise(esctypes.BadResponse(params, "Prefix of " + str_pid))

  i = len(str_pid)

  AssertTrue(params[i:].startswith("!~"))
  i += 2

  hex_checksum = params[i:]
  LogDebug("GetChecksum " + str_pid + " = " + hex_checksum)
  return int(hex_checksum, 16)

def vtLevel(minimum):
  """Defines the minimum VT level the terminal must be capable of to succeed."""
  def decorator(func):
    @functools.wraps(func)
    def func_wrapper(self, *args, **kwargs):
      if esc.vtLevel >= minimum:
        func(self, *args, **kwargs)
      else:
        raise esctypes.InsufficientVTLevel(esc.vtLevel, minimum)
    return func_wrapper
  return decorator

def intentionalDeviationFromSpec(terminal, reason):
  """Decorator for a method indicating that what it tests deviates from the
  sepc and why."""
  def decorator(func):
    @functools.wraps(func)
    def func_wrapper(self, *args, **kwargs):
      func(self, *args, **kwargs)
    return func_wrapper
  return decorator

def optionRejects(terminal, option):
  """Decorator for a method indicating that it will fail if an option is present."""
  reason = "Terminal \"" + terminal + "\" is known to fail this test with option \"" + option + "\" set."
  def decorator(func):
    @functools.wraps(func)
    def func_wrapper(self, *args, **kwargs):
      hasOption = (escargs.args.options is not None and
                   option in escargs.args.options)
      if escargs.args.expected_terminal == terminal:
        try:
          func(self, *args, **kwargs)
        except Exception:
          if not hasOption:
            # Failed despite option being unset. Re-raise.
            raise
          tb = traceback.format_exc()
          lines = tb.split("\n")
          lines = list(map(lambda x: "EXPECTED FAILURE (MISSING OPTION): " + x, lines))
          raise esctypes.KnownBug(reason + "\n\n" + "\n".join(lines))

        # Got here because test passed. If the option is set, that's
        # unexpected so we raise an error.
        if not escargs.args.force and hasOption:
          raise esctypes.InternalError("Should have failed: " + reason)
      else:
        func(self, *args, **kwargs)
    return func_wrapper
  return decorator

def optionRequired(terminal, option, allowPassWithoutOption=False):
  """Decorator for a method indicating that it should fail unless an option is
  present."""
  reason = "Terminal \"" + terminal + "\" requires option \"" + option + "\" for this test to pass."
  def decorator(func):
    @functools.wraps(func)
    def func_wrapper(self, *args, **kwargs):
      hasOption = (escargs.args.options is not None and
                   option in escargs.args.options)
      if escargs.args.expected_terminal == terminal:
        try:
          func(self, *args, **kwargs)
        except Exception:
          if hasOption:
            # Failed despite option being set. Re-raise.
            raise
          tb = traceback.format_exc()
          lines = tb.split("\n")
          lines = list(map(lambda x: "EXPECTED FAILURE (MISSING OPTION): " + x, lines))
          raise esctypes.KnownBug(reason + "\n\n" + "\n".join(lines))

        # This parameter can refer to the command-line options rather than
        # just true/false.
        if isinstance(allowPassWithoutOption, bool):
          ignorePass = allowPassWithoutOption
        else:
          if (escargs.args.options is not None and
            allowPassWithoutOption in escargs.args.options):
            ignorePass = True
          else:
            ignorePass = False

        # Got here because test passed. If the option isn't set, that's
        # unexpected so we raise an error.
        if not escargs.args.force and not hasOption and not ignorePass:
          raise esctypes.InternalError("Should have failed: " + reason)
      else:
        func(self, *args, **kwargs)
    return func_wrapper
  return decorator

def knownBug(terminal, reason, noop=False, shouldTry=True):
  """Decorator for a method indicating that it should fail and explaining why.
  If the method is intended to succeed when nothing happens (that is, the
  sequence being tested is a no-op) then the caller should set noop=True.
  Otherwise, successes will raise an InternalError exception. If shouldTry is
  true then the test will be run to make sure it really does fail."""
  def decorator(func):
    @functools.wraps(func)
    def func_wrapper(self, *args, **kwargs):
      if escargs.args.expected_terminal == terminal:
        if not shouldTry:
          raise esctypes.KnownBug(reason + " (not trying)")
        try:
          func(self, *args, **kwargs)
        except Exception:
          tb = traceback.format_exc()
          lines = tb.split("\n")
          lines = list(map(lambda x: "KNOWN BUG: " + x, lines))
          raise esctypes.KnownBug(reason + "\n" + "\n".join(lines))

        # Shouldn't get here because the test should have failed. If 'force' is on then
        # tests always pass, though.
        if not escargs.args.force and not noop:
          raise esctypes.InternalError("Should have failed")
      else:
        func(self, *args, **kwargs)

    # Add the terminal name to the list of terminals in "func_wrapper"'s
    # func_dict["known_bug_terminals"] so --action=list-known-bugs can work.
    if KNOWN_BUG_TERMINALS in func_wrapper.__dict__:
      kbt = func_wrapper.__dict__.get(KNOWN_BUG_TERMINALS)
    else:
      kbt = {}
      func_wrapper.__dict__[KNOWN_BUG_TERMINALS] = kbt
    kbt[terminal] = reason

    return func_wrapper

  return decorator

def ReasonForKnownBugInMethod(method):
  if KNOWN_BUG_TERMINALS in method.__dict__:
    kbt = method.__dict__.get(KNOWN_BUG_TERMINALS)
    term = escargs.args.expected_terminal
    if term in kbt:
      return kbt[term]
  return None

def AssertAssertionAsserted():
  if escargs.args.force:
    return
  global gHaveAsserted
  ok = gHaveAsserted
  gHaveAsserted = False
  if not ok and not escargs.args.force:
    raise esctypes.BrokenTest("No assertion attempted.")

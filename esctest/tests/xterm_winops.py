import time

import escargs
import esccmd
import esclog

from escutil import AssertEQ, AssertTrue, GetDisplaySize, GetIconTitle
from escutil import GetIsIconified, GetScreenSize, GetWindowPosition
from escutil import GetCharSizePixels, GetFrameSizePixels, GetScreenSizePixels
from escutil import GetWindowSizePixels, GetWindowTitle, knownBug
from escutil import CanQueryShellSize
from esctypes import Point, Size

# No tests for the following operations:
# 5 - Raise in stacking order
# 6 - Lower in stacking order
# 7 - Refresh
# 9;0 - Restore maximized window

class XtermWinopsTests(object):

  @classmethod
  def DelayAfterIcon(cls):
    """Account for time needed by window manager to iconify/deiconify a
    window."""
    need_sleep = escargs.args.expected_terminal in ["xterm"]
    if need_sleep:
      time.sleep(1)

  @classmethod
  def DelayAfterMove(cls):
    """Account for time needed by window manager to move a window."""
    need_sleep = escargs.args.expected_terminal in ["xterm"]
    if need_sleep:
      time.sleep(0.1)

  @classmethod
  def DelayAfterResize(cls):
    """Account for time needed by window manager to resize a window."""
    need_sleep = escargs.args.expected_terminal in ["xterm"]
    if need_sleep:
      time.sleep(1)

  @classmethod
  def GetCharErrorLimit(cls):
    """Returns a Size denoting the expected error limit for character-
    based resizing tests."""
    if escargs.args.expected_terminal == "xterm":
      return Size(2, 2)
    return Size(0, 0)

  @classmethod
  def GetPixelErrorLimit(cls):
    """Returns a Size denoting the expected error limit for pixel-based
    resizing tests.

    For xterm, there are two cases for pixel-based resizing:
    a) WINOP_RESIZE_PIXELS, which requests that the (inner) text-window be
       resize, and
    b) the various "maximize" operations, which operate directly on the (outer)
       shell window.

    They both run into the same constraint: xterm uses window manager
    hints to request that the window manager keep the size of the text
    window an multiple of the character cell-size.  Most window managers
    ignore those hints when asked to maximize a window, and will produce
    a window with cut-off rows/columns.

    While it is "always" true that one can use xwininfo with xterm's
    $WINDOWID to obtain the dimensions of the shell-window, xterm patch 333
    adds a control sequence which returns this information."""
    if escargs.args.expected_terminal in ["xterm"]:
      cells = 3
      if CanQueryShellSize() == 2:
        cells = 1
      frame = GetFrameSizePixels()
      chars = GetCharSizePixels()
      return Size(frame.width() + cells * chars.width(),
                  frame.height() + cells * chars.height())
    return Size(20, 20)

  @classmethod
  def DebugSize(cls, name, value):
    """Log information on a given Size value and its name."""
    esclog.LogDebug(name + str(value.height()) + "x" + str(value.width()))

  def CheckAnySize(self, desired_size, actual_size, limit):
    """After resizing a window, check if its actual size is within the test's
    limits of the desired size."""
    self.DebugSize("actual  size ", actual_size)
    self.DebugSize("desired size ", desired_size)
    error = Size(abs(actual_size.width() - desired_size.width()),
                 abs(actual_size.height() - desired_size.height()))
    self.DebugSize("error limit  ", limit)
    self.DebugSize("actual error ", error)
    AssertTrue(error.width() <= (limit.width()),
               "actual size=%s, desired size=%s, error limit=%s, actual error=%s"
               % (str(actual_size), str(desired_size), str(limit), str(error)))
    AssertTrue(error.height() <= (limit.height()),
               "actual size=%s, desired size=%s, error limit=%s, actual error=%s"
               % (str(actual_size), str(desired_size), str(limit), str(error)))

  def CheckActualSizePixels(self, desired_size):
    """After resizing an xterm window using pixel-units, check if it is close
    enough to pass the test."""
    self.CheckAnySize(desired_size,
                      GetWindowSizePixels(),
                      self.GetPixelErrorLimit())

  def CheckActualSizeChars(self, desired_size, limit):
    """After resizing an xterm window using character-units, check if it is
       close enough to pass the test."""
    self.CheckAnySize(desired_size, GetScreenSize(), limit)

  def CheckForShrinkage(self, original_size, actual_size):
    """After resizing the screen, check if it became smaller.

    The window could become smaller due to a miscomputation,
    since the requested size (perhaps in floating point)
    is truncated to integer values."""
    self.DebugSize("check shrink ", actual_size)
    AssertTrue(actual_size.width() >= original_size.width())
    AssertTrue(actual_size.height() >= original_size.height())

  @classmethod
  def AverageWidth(cls, size_a, size_b):
    """Return the average of the widths from two sizes.

    Some of the xterm resizing-tests use an average of the current
    window size and the X screen-size, since that is fairly likely
    to succeed where a fixed size would fail since it does not take
    into account the actual screen-size."""
    return (size_a.width() + size_b.width()) // 2

  @classmethod
  def AverageHeight(cls, size_a, size_b):
    """Return the average of the heights from two sizes."""
    return (size_a.height() + size_b.height()) // 2

  @knownBug(terminal="iTerm2", reason="Not implemented.")
  @knownBug(terminal="iTerm2beta", reason="Not implemented.")
  def test_XtermWinops_IconifyDeiconfiy(self):
    esccmd.XTERM_WINOPS(esccmd.WINOP_ICONIFY)
    self.DelayAfterIcon()
    AssertEQ(GetIsIconified(), True)

    esccmd.XTERM_WINOPS(esccmd.WINOP_DEICONIFY)
    self.DelayAfterIcon()
    AssertEQ(GetIsIconified(), False)

  @knownBug(terminal="iTerm2beta", reason="Not implemented.")
  def test_XtermWinops_MoveToXY(self):
    '''
    Test window movement to a given position.   The test is indirect, using
    the report after attempting to move to the screen's origins -- which may
    be limited by the window manager if it happens to "own" a panel or bar
    at the top of the screen.  The same can be true of any of the screen's
    boundaries.
    '''
    esccmd.XTERM_WINOPS(esccmd.WINOP_MOVE, 0, 0)
    self.DelayAfterMove()
    origin = GetWindowPosition()
    limit = 10
    # test a diagonal
    for n in range(1, limit):
      esccmd.XTERM_WINOPS(esccmd.WINOP_MOVE, origin.x() + n, origin.y() + n)
      self.DelayAfterMove()
      AssertEQ(GetWindowPosition(), Point(origin.x() + n, origin.y() + n))
    # test a horizontal
    for n in range(limit, 1, -1):
      esccmd.XTERM_WINOPS(esccmd.WINOP_MOVE, origin.x() + n, origin.y() + limit)
      self.DelayAfterMove()
      AssertEQ(GetWindowPosition(), Point(origin.x() + n, origin.y() + limit))
    # test a vertical
    for n in range(limit, 1, -1):
      esccmd.XTERM_WINOPS(esccmd.WINOP_MOVE, origin.x() + limit, origin.y() + n)
      self.DelayAfterMove()
      AssertEQ(GetWindowPosition(), Point(origin.x() + limit, origin.y() + n))

  @knownBug(terminal="iTerm2beta", reason="Not implemented.")
  def test_XtermWinops_MoveToXY_Defaults(self):
    """Default args are interpreted as 0s (see note about window manager)."""
    esccmd.XTERM_WINOPS(esccmd.WINOP_MOVE, 0, 0)
    self.DelayAfterMove()
    origin = GetWindowPosition()
    limit = 10

    esccmd.XTERM_WINOPS(esccmd.WINOP_MOVE, origin.x() + limit, origin.y() + limit)
    self.DelayAfterMove()
    AssertEQ(GetWindowPosition(), Point(origin.x() + limit, origin.y() + limit))

    esccmd.XTERM_WINOPS(esccmd.WINOP_MOVE, origin.x() + limit)
    self.DelayAfterMove()
    AssertEQ(GetWindowPosition(), Point(origin.x() + limit, origin.y()))

    esccmd.XTERM_WINOPS(esccmd.WINOP_MOVE, None, origin.y() + limit)
    self.DelayAfterMove()
    AssertEQ(GetWindowPosition(), Point(origin.x(), origin.y() + limit))

  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_XtermWinops_ResizePixels_BothParameters(self):
    """Resize the window to a pixel size, giving both parameters."""
    maximum_size = GetScreenSizePixels()
    original_size = GetWindowSizePixels()
    if escargs.args.expected_terminal == "xterm":
      desired_size = Size(self.AverageWidth(maximum_size, original_size),
                          self.AverageHeight(maximum_size, original_size))
    else:
      desired_size = Size(400, 200)

    esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                        desired_size.height(),
                        desired_size.width())
    self.DelayAfterResize()
    self.CheckActualSizePixels(desired_size)

    esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                        original_size.height(),
                        original_size.width())
    self.DelayAfterResize()

  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_XtermWinops_ResizePixels_OmittedHeight(self):
    """Resize the window to a pixel size, omitting one parameter. The size
    should not change in the direction of the omitted parameter."""
    maximum_size = GetScreenSizePixels()
    original_size = GetWindowSizePixels()

    if escargs.args.expected_terminal == "xterm":
      desired_size = Size(maximum_size.width(), original_size.height())
    else:
      desired_size = Size(400, original_size.height())

    esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                        None,
                        desired_size.width())
    self.DelayAfterResize()
    self.CheckActualSizePixels(desired_size)

    esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                        original_size.height(),
                        original_size.width())
    self.DelayAfterResize()

  def test_XtermWinops_ResizePixels_OmittedWidth(self):
    """Resize the window to a pixel size, omitting one parameter. The size
    should not change in the direction of the omitted parameter."""
    maximum_size = GetScreenSizePixels()
    original_size = GetWindowSizePixels()

    if escargs.args.expected_terminal == "xterm":
      desired_size = Size(original_size.width(),
                          self.AverageHeight(maximum_size, original_size))
    else:
      desired_size = Size(original_size.width(), 200)

    esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                        desired_size.height())
    self.DelayAfterResize()
    self.CheckActualSizePixels(desired_size)

    esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                        original_size.height(),
                        original_size.width())
    self.DelayAfterResize()

  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_XtermWinops_ResizePixels_ZeroWidth(self):
    """Resize the window to a pixel size, setting one parameter to 0. The
    window should maximize in the direction of the 0 parameter."""
    if escargs.args.expected_terminal == "xterm":
      maximum_size = GetScreenSizePixels()
      original_size = GetWindowSizePixels()

      # Set height and maximize width.
      desired_size = Size(maximum_size.width(),
                          self.AverageHeight(maximum_size, original_size))
      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                          desired_size.height(),
                          0)
      self.DelayAfterResize()
      self.CheckActualSizePixels(desired_size)

      # See if the width is about as big as the display (only measurable in
      # characters, not pixels).
      display_size = GetDisplaySize()  # In characters
      screen_size = GetScreenSize()  # In characters
      max_error = 5
      AssertTrue(abs(display_size.width() - screen_size.width()) < max_error)

      # Restore to original size.
      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                          original_size.height(),
                          original_size.width())
      self.DelayAfterResize()
    else:
      original_size = GetWindowSizePixels()

      # Set height and maximize width.
      desired_height = 200
      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                          desired_height,
                          0)

      # Make sure the height changed as requested.
      max_error = 20
      actual_size = GetWindowSizePixels()
      AssertTrue(abs(actual_size.height() - desired_height) < max_error)

      # See if the width is about as big as the display (only measurable in
      # characters, not pixels).
      display_size = GetDisplaySize()  # In characters
      screen_size = GetScreenSize()  # In characters
      max_error = 5
      AssertTrue(abs(display_size.width() - screen_size.width()) < max_error)

      # Restore to original size.
      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                          original_size.height(),
                          original_size.width())

  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_XtermWinops_ResizePixels_ZeroHeight(self):
    """Resize the window to a pixel size, setting one parameter to 0. The
    window should maximize in the direction of the 0 parameter."""
    if escargs.args.expected_terminal == "xterm":
      maximum_size = GetScreenSizePixels()
      original_size = GetWindowSizePixels()

      # Set height and maximize width.
      desired_size = Size(self.AverageWidth(maximum_size, original_size),
                          maximum_size.height())
      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                          0,
                          desired_size.width())
      self.DelayAfterResize()
      self.CheckActualSizePixels(desired_size)

      # See if the height is about as big as the display (only measurable in
      # characters, not pixels).
      display_size = GetDisplaySize()  # In characters
      screen_size = GetScreenSize()  # In characters
      max_error = 5
      AssertTrue(abs(display_size.height() - screen_size.height()) < max_error)

      # Restore to original size.
      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                          original_size.height(),
                          original_size.width())
      self.DelayAfterResize()
    else:
      original_size = GetWindowSizePixels()

      # Set height and maximize width.
      desired_width = 400
      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                          0,
                          desired_width)

      # Make sure the height changed as requested.
      max_error = 20
      actual_size = GetWindowSizePixels()
      AssertTrue(abs(actual_size.width() - desired_width) < max_error)

      # See if the height is about as big as the display (only measurable in
      # characters, not pixels).
      display_size = GetDisplaySize()  # In characters
      screen_size = GetScreenSize()  # In characters
      max_error = 5
      AssertTrue(abs(display_size.height() - screen_size.height()) < max_error)

      # Restore to original size.
      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                          original_size.height(),
                          original_size.width())

  def test_XtermWinops_ResizeChars_BothParameters(self):
    """Resize the window to a character size, giving both parameters."""
    maximum_size = GetDisplaySize()  # In characters
    original_size = GetScreenSize()  # In characters
    if escargs.args.expected_terminal == "xterm":
      desired_size = Size(self.AverageWidth(maximum_size, original_size),
                          self.AverageHeight(maximum_size, original_size))
    else:
      desired_size = Size(20, 21)

    esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_CHARS,
                        desired_size.height(),
                        desired_size.width())
    self.DelayAfterResize()

    self.CheckActualSizeChars(desired_size, self.GetCharErrorLimit())

  def test_XtermWinops_ResizeChars_ZeroWidth(self):
    """Resize the window to a character size, setting one param to 0 (max size
    in that direction)."""
    maximum_size = GetDisplaySize()
    original_size = GetScreenSize()
    if escargs.args.expected_terminal == "xterm":
      desired_size = Size(maximum_size.width(), original_size.height())
    else:
      desired_size = Size(maximum_size.width(), 21)

    esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_CHARS,
                        desired_size.height(),
                        0)
    self.DelayAfterResize()

    limit = self.GetCharErrorLimit()
    limit = Size(limit.width(), 0)
    self.CheckActualSizeChars(desired_size, limit)

  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_XtermWinops_ResizeChars_ZeroHeight(self):
    """Resize the window to a character size, setting one param to 0 (max size
    in that direction)."""
    maximum_size = GetDisplaySize()
    original_size = GetScreenSize()
    if escargs.args.expected_terminal == "xterm":
      desired_size = Size(original_size.width(), maximum_size.height())
    else:
      desired_size = Size(20, maximum_size.height())

    esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_CHARS,
                        0,
                        desired_size.width())
    self.DelayAfterResize()

    limit = self.GetCharErrorLimit()
    limit = Size(0, limit.height())
    self.CheckActualSizeChars(desired_size, limit)

  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_XtermWinops_ResizeChars_DefaultWidth(self):
    original_size = GetScreenSize()
    display_size = GetDisplaySize()
    if escargs.args.expected_terminal == "xterm":
      desired_size = Size(original_size.width(),
                          self.AverageHeight(original_size, display_size))
    else:
      desired_size = Size(original_size.width(), 21)

    esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_CHARS,
                        desired_size.height())
    self.DelayAfterResize()

    self.CheckActualSizeChars(desired_size, Size(0, 0))

  def test_XtermWinops_ResizeChars_DefaultHeight(self):
    original_size = GetScreenSize()
    display_size = GetDisplaySize()
    if escargs.args.expected_terminal == "xterm":
      desired_size = Size(self.AverageWidth(original_size, display_size),
                          original_size.height())
    else:
      desired_size = Size(20, original_size.height())

    esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_CHARS,
                        None,
                        desired_size.width())
    self.DelayAfterResize()

    self.CheckActualSizeChars(desired_size, Size(0, 0))

  @knownBug(terminal="iTerm2", reason="Not implemented")
  @knownBug(terminal="iTerm2beta", reason="Not implemented")
  def test_XtermWinops_MaximizeWindow_HorizontallyAndVertically(self):
    esccmd.XTERM_WINOPS(esccmd.WINOP_MAXIMIZE, esccmd.WINOP_MAXIMIZE_HV)
    self.DelayAfterResize()
    actual_size = GetScreenSize()
    desired_size = GetDisplaySize()

    esccmd.XTERM_WINOPS(esccmd.WINOP_MAXIMIZE, esccmd.WINOP_MAXIMIZE_EXIT)
    self.DelayAfterResize()
    if escargs.args.expected_terminal == "xterm":
      error_limit = Size(3, 3)
    else:
      error_limit = Size(0, 0)
    self.CheckAnySize(desired_size, actual_size, error_limit)

  @knownBug(terminal="iTerm2", reason="Not implemented")
  @knownBug(terminal="iTerm2beta", reason="Not implemented")
  def test_XtermWinops_MaximizeWindow_Horizontally(self):
    desired_size = Size(GetDisplaySize().width(),
                        GetScreenSize().height())
    esccmd.XTERM_WINOPS(esccmd.WINOP_MAXIMIZE, esccmd.WINOP_MAXIMIZE_H)
    self.DelayAfterResize()
    actual_size = GetScreenSize()

    esccmd.XTERM_WINOPS(esccmd.WINOP_MAXIMIZE, esccmd.WINOP_MAXIMIZE_EXIT)
    self.DelayAfterResize()
    if escargs.args.expected_terminal == "xterm":
      error_limit = Size(3, 0)
    else:
      error_limit = Size(0, 0)

    self.CheckAnySize(desired_size, actual_size, error_limit)

  @knownBug(terminal="iTerm2", reason="Not implemented")
  @knownBug(terminal="iTerm2beta", reason="Not implemented")
  def test_XtermWinops_MaximizeWindow_Vertically(self):
    desired_size = Size(GetScreenSize().width(),
                        GetDisplaySize().height())
    esccmd.XTERM_WINOPS(esccmd.WINOP_MAXIMIZE, esccmd.WINOP_MAXIMIZE_V)
    self.DelayAfterResize()
    actual_size = GetScreenSize()

    esccmd.XTERM_WINOPS(esccmd.WINOP_MAXIMIZE, esccmd.WINOP_MAXIMIZE_EXIT)
    self.DelayAfterResize()
    if escargs.args.expected_terminal == "xterm":
      error_limit = Size(0, 5)
    else:
      error_limit = Size(0, 0)
    self.CheckAnySize(desired_size, actual_size, error_limit)

  @knownBug(terminal="iTerm2", reason="Not implemented")
  @knownBug(terminal="iTerm2beta", reason="Not implemented")
  def test_XtermWinops_Fullscreen(self):
    original_size = GetScreenSize()
    display_size = GetDisplaySize()

    # Enter fullscreen
    esccmd.XTERM_WINOPS(esccmd.WINOP_FULLSCREEN,
                        esccmd.WINOP_FULLSCREEN_ENTER)
    self.DelayAfterResize()

    actual_size = GetScreenSize()
    self.CheckAnySize(display_size, actual_size, Size(3, 3))
    self.CheckForShrinkage(original_size, actual_size)

    # Exit fullscreen
    esccmd.XTERM_WINOPS(esccmd.WINOP_FULLSCREEN,
                        esccmd.WINOP_FULLSCREEN_EXIT)
    self.DelayAfterResize()

    self.CheckForShrinkage(original_size, GetScreenSize())

    # Toggle in
    esccmd.XTERM_WINOPS(esccmd.WINOP_FULLSCREEN,
                        esccmd.WINOP_FULLSCREEN_TOGGLE)
    self.DelayAfterResize()

    self.CheckForShrinkage(original_size, GetScreenSize())

    # Toggle out
    esccmd.XTERM_WINOPS(esccmd.WINOP_FULLSCREEN,
                        esccmd.WINOP_FULLSCREEN_TOGGLE)
    self.DelayAfterResize()

    self.CheckForShrinkage(original_size, GetScreenSize())

  @classmethod
  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_XtermWinops_ReportIconLabel(cls):
    string = "test " + str(time.time())
    esccmd.ChangeIconTitle(string)
    AssertEQ(GetIconTitle(), string)

  @classmethod
  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_XtermWinops_ReportWindowLabel(cls):
    string = "test " + str(time.time())
    esccmd.ChangeWindowTitle(string)
    AssertEQ(GetWindowTitle(), string)

  @classmethod
  def test_XtermWinops_PushIconAndWindow_PopIconAndWindow(cls):
    """Basic test: Push an icon & window title and restore it."""
    # Generate a uniqueish string
    string = str(time.time())

    # Set the window and icon title, then push both.
    esccmd.ChangeWindowAndIconTitle(string)
    AssertEQ(GetWindowTitle(), string)
    AssertEQ(GetIconTitle(), string)
    esccmd.XTERM_WINOPS(esccmd.WINOP_PUSH_TITLE,
                        esccmd.WINOP_PUSH_TITLE_ICON_AND_WINDOW)

    # Change to x, make sure it took.
    esccmd.ChangeWindowTitle("x")
    esccmd.ChangeIconTitle("x")
    AssertEQ(GetWindowTitle(), "x")
    AssertEQ(GetIconTitle(), "x")

    # Pop both window and icon titles, ensure correct.
    esccmd.XTERM_WINOPS(esccmd.WINOP_POP_TITLE,
                        esccmd.WINOP_POP_TITLE_ICON_AND_WINDOW)
    AssertEQ(GetWindowTitle(), string)
    AssertEQ(GetIconTitle(), string)

  @classmethod
  @knownBug(terminal="iTerm2",
            reason="The window title incorrectly changes"
            + " when popping the icon title.")
  @knownBug(terminal="iTerm2beta",
            reason="The window title incorrectly changes"
            + " when popping the icon title.")
  def test_XtermWinops_PushIconAndWindow_PopIcon(cls):
    """Push an icon & window title and pop just the icon title."""
    # Generate a uniqueish string
    string = str(time.time())

    # Set the window and icon title, then push both.
    esccmd.ChangeWindowAndIconTitle(string)
    AssertEQ(GetWindowTitle(), string)
    AssertEQ(GetIconTitle(), string)
    esccmd.XTERM_WINOPS(esccmd.WINOP_PUSH_TITLE,
                        esccmd.WINOP_PUSH_TITLE_ICON_AND_WINDOW)

    # Change to x, make sure it took.
    esccmd.ChangeWindowTitle("x")
    esccmd.ChangeIconTitle("x")
    AssertEQ(GetWindowTitle(), "x")
    AssertEQ(GetIconTitle(), "x")

    # Pop icon title, ensure correct.
    esccmd.XTERM_WINOPS(esccmd.WINOP_POP_TITLE,
                        esccmd.WINOP_POP_TITLE_ICON)
    AssertEQ(GetWindowTitle(), "x")
    AssertEQ(GetIconTitle(), string)

    # Try to pop the window title; should do nothing.
    esccmd.XTERM_WINOPS(esccmd.WINOP_POP_TITLE,
                        esccmd.WINOP_POP_TITLE_WINDOW)
    AssertEQ(GetWindowTitle(), "x")
    AssertEQ(GetIconTitle(), string)

  @classmethod
  @knownBug(terminal="iTerm2",
            reason="The window title incorrectly changes"
            + " when popping the icon title.")
  @knownBug(terminal="iTerm2beta",
            reason="The window title incorrectly changes"
            + " when popping the icon title.")
  def test_XtermWinops_PushIconAndWindow_PopWindow(cls):
    """Push an icon & window title and pop just the window title."""
    # Generate a uniqueish string
    string = str(time.time())

    # Set the window and icon title, then push both.
    esccmd.ChangeWindowAndIconTitle(string)
    AssertEQ(GetWindowTitle(), string)
    AssertEQ(GetIconTitle(), string)
    esccmd.XTERM_WINOPS(esccmd.WINOP_PUSH_TITLE,
                        esccmd.WINOP_PUSH_TITLE_ICON_AND_WINDOW)

    # Change to x, make sure it took.
    esccmd.ChangeWindowTitle("x")
    esccmd.ChangeIconTitle("x")
    AssertEQ(GetWindowTitle(), "x")
    AssertEQ(GetIconTitle(), "x")

    # Pop icon title, ensure correct.
    esccmd.XTERM_WINOPS(esccmd.WINOP_POP_TITLE,
                        esccmd.WINOP_POP_TITLE_WINDOW)
    AssertEQ(GetWindowTitle(), string)
    AssertEQ(GetIconTitle(), "x")

    # Try to pop the icon title; should do nothing.
    esccmd.XTERM_WINOPS(esccmd.WINOP_POP_TITLE,
                        esccmd.WINOP_POP_TITLE_ICON)
    AssertEQ(GetWindowTitle(), string)
    AssertEQ(GetIconTitle(), "x")

  @classmethod
  def test_XtermWinops_PushIcon_PopIcon(cls):
    """Push icon title and then pop it."""
    # Generate a uniqueish string
    string = str(time.time())

    # Set the window and icon title, then push both.
    esccmd.ChangeWindowTitle("x")
    esccmd.ChangeIconTitle(string)
    esccmd.XTERM_WINOPS(esccmd.WINOP_PUSH_TITLE,
                        esccmd.WINOP_PUSH_TITLE_ICON)

    # Change to x.
    esccmd.ChangeIconTitle("y")

    # Pop icon title, ensure correct.
    esccmd.XTERM_WINOPS(esccmd.WINOP_POP_TITLE,
                        esccmd.WINOP_POP_TITLE_ICON)
    AssertEQ(GetWindowTitle(), "x")
    AssertEQ(GetIconTitle(), string)

  @classmethod
  def test_XtermWinops_PushWindow_PopWindow(cls):
    """Push window title and then pop it."""
    # Generate a uniqueish string
    string = str(time.time())

    # Set the window and icon title, then push both.
    esccmd.ChangeIconTitle("x")
    esccmd.ChangeWindowTitle(string)
    esccmd.XTERM_WINOPS(esccmd.WINOP_PUSH_TITLE,
                        esccmd.WINOP_PUSH_TITLE_WINDOW)

    # Change to x.
    esccmd.ChangeWindowTitle("y")

    # Pop window title, ensure correct.
    esccmd.XTERM_WINOPS(esccmd.WINOP_POP_TITLE,
                        esccmd.WINOP_POP_TITLE_WINDOW)
    AssertEQ(GetIconTitle(), "x")
    AssertEQ(GetWindowTitle(), string)

  @classmethod
  def test_XtermWinops_PushIconThenWindowThenPopBoth(cls):
    """Push icon, then push window, then pop both."""
    # Generate a uniqueish string
    string1 = "a" + str(time.time())
    string2 = "b" + str(time.time())

    # Set titles
    esccmd.ChangeWindowTitle(string1)
    esccmd.ChangeIconTitle(string2)

    # Push icon then window
    esccmd.XTERM_WINOPS(esccmd.WINOP_PUSH_TITLE,
                        esccmd.WINOP_PUSH_TITLE_ICON)
    esccmd.XTERM_WINOPS(esccmd.WINOP_PUSH_TITLE,
                        esccmd.WINOP_PUSH_TITLE_WINDOW)

    # Change both to known values.
    esccmd.ChangeWindowTitle("y")
    esccmd.ChangeIconTitle("z")

    # Pop both titles.
    esccmd.XTERM_WINOPS(esccmd.WINOP_POP_TITLE,
                        esccmd.WINOP_POP_TITLE_ICON_AND_WINDOW)
    AssertEQ(GetWindowTitle(), string1)
    AssertEQ(GetIconTitle(), string2)

  @classmethod
  def test_XtermWinops_PushMultiplePopMultiple_Icon(cls):
    """Push two titles and pop twice."""
    # Generate a uniqueish string
    string1 = "a" + str(time.time())
    string2 = "b" + str(time.time())

    for title in [string1, string2]:
      # Set title
      esccmd.ChangeIconTitle(title)

      # Push
      esccmd.XTERM_WINOPS(esccmd.WINOP_PUSH_TITLE,
                          esccmd.WINOP_PUSH_TITLE_ICON)

    # Change to known values.
    esccmd.ChangeIconTitle("z")

    # Pop
    esccmd.XTERM_WINOPS(esccmd.WINOP_POP_TITLE,
                        esccmd.WINOP_POP_TITLE_ICON)
    AssertEQ(GetIconTitle(), string2)

    # Pop
    esccmd.XTERM_WINOPS(esccmd.WINOP_POP_TITLE,
                        esccmd.WINOP_POP_TITLE_ICON)
    AssertEQ(GetIconTitle(), string1)

  @classmethod
  def test_XtermWinops_PushMultiplePopMultiple_Window(cls):
    """Push two titles and pop twice."""
    # Generate a uniqueish string
    string1 = "a" + str(time.time())
    string2 = "b" + str(time.time())

    for title in [string1, string2]:
      # Set title
      esccmd.ChangeWindowTitle(title)

      # Push
      esccmd.XTERM_WINOPS(esccmd.WINOP_PUSH_TITLE,
                          esccmd.WINOP_PUSH_TITLE_WINDOW)

    # Change to known values.
    esccmd.ChangeWindowTitle("z")

    # Pop
    esccmd.XTERM_WINOPS(esccmd.WINOP_POP_TITLE,
                        esccmd.WINOP_POP_TITLE_WINDOW)
    AssertEQ(GetWindowTitle(), string2)

    # Pop
    esccmd.XTERM_WINOPS(esccmd.WINOP_POP_TITLE,
                        esccmd.WINOP_POP_TITLE_WINDOW)
    AssertEQ(GetWindowTitle(), string1)

  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_XtermWinops_DECSLPP(self):
    """Resize to n lines of height."""
    esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_CHARS,
                        10,
                        90)
    self.DelayAfterResize()

    AssertEQ(GetScreenSize(), Size(90, 10))

    esccmd.XTERM_WINOPS(24)
    AssertEQ(GetScreenSize(), Size(90, 24))

    esccmd.XTERM_WINOPS(30)
    AssertEQ(GetScreenSize(), Size(90, 30))

import escargs
import esccmd
import esclog
from escutil import AssertEQ, AssertTrue, GetDisplaySize, GetIconTitle
from escutil import GetIsIconified, GetScreenSize, GetWindowPosition
from escutil import GetCharSizePixels, GetFrameSizePixels, GetScreenSizePixels
from escutil import GetWindowSizePixels, GetWindowTitle, knownBug
from esctypes import Point, Size
import time

# No tests for the following operations:
# 5 - Raise in stacking order
# 6 - Lower in stacking order
# 7 - Refresh
# 9;0 - Restore maximized window

class XtermWinopsTests(object):
  def delay_after_icon(self):
    need_sleep = escargs.args.expected_terminal in ["xterm"]
    if need_sleep:
      time.sleep(0.5)

  def delay_after_move(self):
    need_sleep = escargs.args.expected_terminal in ["xterm"]
    if need_sleep:
      time.sleep(0.1)

  def delay_after_resize(self):
    need_sleep = escargs.args.expected_terminal in ["xterm"]
    if need_sleep:
      time.sleep(1)

  def get_pixel_error_limit(self, characterCells):
    frame = GetFrameSizePixels()
    chars = GetCharSizePixels()
    return Size(frame.width() + characterCells * chars.width(),
                frame.height() + characterCells * chars.height())

  def check_any_size(self, desired_size, actual_size, limit):
    esclog.LogInfo("actual  size " + str(actual_size.height()) + "x" + str(actual_size.width()))
    esclog.LogInfo("desired size " + str(desired_size.height()) + "x" + str(desired_size.width()))
    error = Size(abs(actual_size.width() - desired_size.width()),
                 abs(actual_size.height() - desired_size.height()))
    esclog.LogInfo("error limit  " + str(limit.height()) + "x" + str(limit.width()))
    esclog.LogInfo("actual error " + str(error.height()) + "x" + str(error.width()))
    AssertTrue(error.width() <= (limit.width()))
    AssertTrue(error.height() <= (limit.height()))

  def check_actual_size_pixels(self, desired_size):
    self.check_any_size(desired_size, GetWindowSizePixels(), self.get_pixel_error_limit(3))

  def check_actual_size_chars(self, desired_size, limit):
    self.check_any_size(desired_size, GetScreenSize(), limit)

  def check_for_shrinkage(self, original_size, actual_size):
    esclog.LogInfo("actual size  " + str(actual_size.height()) + "x" + str(actual_size.width()))
    AssertTrue(actual_size.width() >= original_size.width())
    AssertTrue(actual_size.height() >= original_size.height())

  def average_width(self, a, b):
    return (a.width() + b.width()) / 2

  def average_height(self, a, b):
    return (a.height() + b.height()) / 2

  def test_XtermWinops_IconifyDeiconfiy(self):
    esccmd.XTERM_WINOPS(esccmd.WINOP_ICONIFY)
    self.delay_after_icon()
    AssertEQ(GetIsIconified(), True)

    esccmd.XTERM_WINOPS(esccmd.WINOP_DEICONIFY)
    self.delay_after_icon()
    AssertEQ(GetIsIconified(), False)

  def test_XtermWinops_MoveToXY(self):
    esccmd.XTERM_WINOPS(esccmd.WINOP_MOVE, 0, 0)
    self.delay_after_move()
    AssertEQ(GetWindowPosition(), Point(0, 0))
    esccmd.XTERM_WINOPS(esccmd.WINOP_MOVE, 1, 1)
    self.delay_after_move()
    AssertEQ(GetWindowPosition(), Point(1, 1))

  def test_XtermWinops_MoveToXY_Defaults(self):
    """Default args are interpreted as 0s."""
    esccmd.XTERM_WINOPS(esccmd.WINOP_MOVE, 1, 1)
    self.delay_after_move()
    AssertEQ(GetWindowPosition(), Point(1, 1))

    esccmd.XTERM_WINOPS(esccmd.WINOP_MOVE, 1)
    self.delay_after_move()
    AssertEQ(GetWindowPosition(), Point(1, 0))

    esccmd.XTERM_WINOPS(esccmd.WINOP_MOVE, None, 1)
    self.delay_after_move()
    AssertEQ(GetWindowPosition(), Point(0, 1))

  def test_XtermWinops_ResizePixels_BothParameters(self):
    """Resize the window to a pixel size, giving both parameters."""
    if escargs.args.expected_terminal == "xterm":
      maximum_size = GetScreenSizePixels()
      original_size = GetWindowSizePixels()
      desired_size = Size(self.average_width(maximum_size, original_size),
                          self.average_height(maximum_size, original_size))

      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                          desired_size.height(),
                          desired_size.width())
      self.delay_after_resize()
      self.check_actual_size_pixels(desired_size)

      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                          original_size.height(),
                          original_size.width())
      self.delay_after_resize()
    else:
      original_size = GetWindowSizePixels()
      desired_size = Size(400, 200)

      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                          desired_size.height(),
                          desired_size.width())
      # See if we're within 20px of the desired size on each dimension. It won't
      # be exact because most terminals snap to grid.
      actual_size = GetWindowSizePixels()
      error = Size(abs(actual_size.width() - desired_size.width()),
                   abs(actual_size.height() - desired_size.height()))
      max_error = 20
      AssertTrue(error.width() <= max_error)
      AssertTrue(error.height() <= max_error)

      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                          original_size.height(),
                          original_size.width())

  def test_XtermWinops_ResizePixels_OmittedHeight(self):
    """Resize the window to a pixel size, omitting one parameter. The size
    should not change in the direction of the omitted parameter."""
    if escargs.args.expected_terminal == "xterm":
      maximum_size = GetScreenSizePixels()
      original_size = GetWindowSizePixels()

      desired_size = Size(maximum_size.width(), original_size.height())

      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                          None,
                          desired_size.width())
      self.delay_after_resize()
      self.check_actual_size_pixels(desired_size)

      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                          original_size.height(),
                          original_size.width())
      self.delay_after_resize()
    else:
      original_size = GetWindowSizePixels()
      desired_size = Size(400, original_size.height())

      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                          None,
                          desired_size.width())
      # See if we're within 20px of the desired size. It won't be exact because
      # most terminals snap to grid.
      actual_size = GetWindowSizePixels()
      error = Size(abs(actual_size.width() - desired_size.width()),
                   abs(actual_size.height() - desired_size.height()))
      max_error = 20
      AssertTrue(error.width() <= max_error)
      AssertTrue(error.height() <= max_error)

      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                          original_size.height(),
                          original_size.width())

  def test_XtermWinops_ResizePixels_OmittedWidth(self):
    """Resize the window to a pixel size, omitting one parameter. The size
    should not change in the direction of the omitted parameter."""
    if escargs.args.expected_terminal == "xterm":
      maximum_size = GetScreenSizePixels()
      original_size = GetWindowSizePixels()

      desired_size = Size(original_size.width(),
                          self.average_height(maximum_size, original_size))

      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                          desired_size.height())
      self.delay_after_resize()
      self.check_actual_size_pixels(desired_size)

      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                          original_size.height(),
                          original_size.width())
      self.delay_after_resize()
    else:
      original_size = GetWindowSizePixels()
      desired_size = Size(original_size.width(), 200)

      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                          desired_size.height())
      # See if we're within 20px of the desired size. It won't be exact because
      # most terminals snap to grid.
      actual_size = GetWindowSizePixels()
      error = Size(abs(actual_size.width() - desired_size.width()),
                   abs(actual_size.height() - desired_size.height()))
      max_error = 20
      AssertTrue(error.width() <= max_error)
      AssertTrue(error.height() <= max_error)

      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                          original_size.height(),
                          original_size.width())

  def test_XtermWinops_ResizePixels_ZeroWidth(self):
    """Resize the window to a pixel size, setting one parameter to 0. The
    window should maximize in the direction of the 0 parameter."""
    if escargs.args.expected_terminal == "xterm":
      maximum_size = GetScreenSizePixels()
      original_size = GetWindowSizePixels()

      # Set height and maximize width.
      desired_size = Size(maximum_size.width(),
                          self.average_height(maximum_size, original_size))
      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                          desired_size.height(),
                          0)
      self.delay_after_resize()
      self.check_actual_size_pixels(desired_size)

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
      self.delay_after_resize()
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

  def test_XtermWinops_ResizePixels_ZeroHeight(self):
    """Resize the window to a pixel size, setting one parameter to 0. The
    window should maximize in the direction of the 0 parameter."""
    if escargs.args.expected_terminal == "xterm":
      maximum_size = GetScreenSizePixels()
      original_size = GetWindowSizePixels()

      # Set height and maximize width.
      desired_size = Size(self.average_width(maximum_size, original_size),
                          maximum_size.height())
      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_PIXELS,
                          0,
                          desired_size.width())
      self.delay_after_resize()
      self.check_actual_size_pixels(desired_size)

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
      self.delay_after_resize()
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
    if escargs.args.expected_terminal == "xterm":
      maximum_size = GetDisplaySize()  # In characters
      original_size = GetScreenSize()  # In characters
      desired_size = Size(self.average_width(maximum_size, original_size),
                          self.average_height(maximum_size, original_size))

      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_CHARS,
                          desired_size.height(),
                          desired_size.width())
      self.delay_after_resize()

      self.check_actual_size_chars(desired_size, Size(3, 3))
    else:
      desired_size = Size(20, 21)

      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_CHARS,
                          desired_size.height(),
                          desired_size.width())
      AssertEQ(GetScreenSize(), desired_size)

  def test_XtermWinops_ResizeChars_ZeroWidth(self):
    """Resize the window to a character size, setting one param to 0 (max size
    in that direction)."""
    if escargs.args.expected_terminal == "xterm":
      maximum_size = GetDisplaySize()
      original_size = GetScreenSize()
      desired_size = Size(maximum_size.width(), original_size.height())

      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_CHARS,
                          desired_size.height(),
                          0)
      self.delay_after_resize()

      self.check_actual_size_chars(desired_size, Size(3, 0))
    else:
      max_size = GetDisplaySize()
      desired_size = Size(max_size.width(), 21)

      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_CHARS,
                          desired_size.height(),
                          0)
      self.delay_after_resize()
      AssertEQ(GetScreenSize(), desired_size)

  def test_XtermWinops_ResizeChars_ZeroHeight(self):
    """Resize the window to a character size, setting one param to 0 (max size
    in that direction)."""
    if escargs.args.expected_terminal == "xterm":
      maximum_size = GetDisplaySize()
      original_size = GetScreenSize()
      desired_size = Size(original_size.width(), maximum_size.height())

      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_CHARS,
                          0,
                          desired_size.width())
      self.delay_after_resize()

      self.check_actual_size_chars(desired_size, Size(0, 3))
    else:
      max_size = GetDisplaySize()
      desired_size = Size(20, max_size.height())

      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_CHARS,
                          0,
                          desired_size.width())
      self.delay_after_resize()
      AssertEQ(GetScreenSize(), desired_size)

  def test_XtermWinops_ResizeChars_DefaultWidth(self):
    if escargs.args.expected_terminal == "xterm":
      original_size = GetScreenSize()
      display_size = GetDisplaySize()
      desired_size = Size(original_size.width(),
                          self.average_height(original_size, display_size))

      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_CHARS,
                          desired_size.height())
      self.delay_after_resize()

      self.check_actual_size_chars(desired_size, Size(0, 0))
    else:
      original_size = GetScreenSize()
      desired_size = Size(original_size.width(), 21)

      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_CHARS,
                          desired_size.height())
      AssertEQ(GetScreenSize(), desired_size)

  def test_XtermWinops_ResizeChars_DefaultHeight(self):
    if escargs.args.expected_terminal == "xterm":
      original_size = GetScreenSize()
      display_size = GetDisplaySize()
      desired_size = Size(self.average_width(original_size, display_size),
                          original_size.height())

      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_CHARS,
                          None,
                          desired_size.width())
      self.delay_after_resize()

      self.check_actual_size_chars(desired_size, Size(0, 0))
    else:
      original_size = GetScreenSize()
      desired_size = Size(20, original_size.height())

      esccmd.XTERM_WINOPS(esccmd.WINOP_RESIZE_CHARS,
                          None,
                          desired_size.width())
      AssertEQ(GetScreenSize(), desired_size)

  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_XtermWinops_MaximizeWindow_HorizontallyAndVertically(self):
    if escargs.args.expected_terminal == "xterm":
      esccmd.XTERM_WINOPS(esccmd.WINOP_MAXIMIZE, esccmd.WINOP_MAXIMIZE_HV)
      self.delay_after_resize()

      actual_size = GetScreenSize()
      desired_size = GetDisplaySize()

      esccmd.XTERM_WINOPS(esccmd.WINOP_MAXIMIZE, esccmd.WINOP_MAXIMIZE_EXIT)
      self.delay_after_resize()

      self.check_any_size(desired_size, actual_size, Size(3, 3))
    else:
      esccmd.XTERM_WINOPS(esccmd.WINOP_MAXIMIZE, esccmd.WINOP_MAXIMIZE_HV)
      AssertEQ(GetScreenSize(), GetDisplaySize())

  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_XtermWinops_MaximizeWindow_Horizontally(self):
    if escargs.args.expected_terminal == "xterm":
      desired_size = Size(GetDisplaySize().width(),
                          GetScreenSize().height())

      esccmd.XTERM_WINOPS(esccmd.WINOP_MAXIMIZE, esccmd.WINOP_MAXIMIZE_H)
      self.delay_after_resize()

      actual_size = GetScreenSize()

      esccmd.XTERM_WINOPS(esccmd.WINOP_MAXIMIZE, esccmd.WINOP_MAXIMIZE_EXIT)
      self.delay_after_resize()

      self.check_any_size(desired_size, actual_size, Size(3, 0))
    else:
      display_size = GetDisplaySize()
      original_size = GetScreenSize()
      expected_size = Size(width=display_size.width(),
                           height=original_size.height())
      esccmd.XTERM_WINOPS(esccmd.WINOP_MAXIMIZE, esccmd.WINOP_MAXIMIZE_H)
      AssertEQ(GetScreenSize(), expected_size)

  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_XtermWinops_MaximizeWindow_Vertically(self):
    if escargs.args.expected_terminal == "xterm":
      desired_size = Size(GetScreenSize().width(),
                          GetDisplaySize().height())

      esccmd.XTERM_WINOPS(esccmd.WINOP_MAXIMIZE, esccmd.WINOP_MAXIMIZE_V)
      self.delay_after_resize()

      actual_size = GetScreenSize()

      esccmd.XTERM_WINOPS(esccmd.WINOP_MAXIMIZE, esccmd.WINOP_MAXIMIZE_EXIT)
      self.delay_after_resize()

      self.check_any_size(desired_size, actual_size, Size(0, 5))
    else:
      display_size = GetDisplaySize()
      original_size = GetScreenSize()
      expected_size = Size(width=original_size.width(),
                           height=display_size.height())
      esccmd.XTERM_WINOPS(esccmd.WINOP_MAXIMIZE, esccmd.WINOP_MAXIMIZE_V)
      AssertEQ(GetScreenSize(), expected_size)

  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_XtermWinops_Fullscreen(self):
    if escargs.args.expected_terminal == "xterm":
      original_size = GetScreenSize()
      display_size = GetDisplaySize()

      # Enter fullscreen
      esccmd.XTERM_WINOPS(esccmd.WINOP_FULLSCREEN,
                          esccmd.WINOP_FULLSCREEN_ENTER)
      self.delay_after_resize()

      actual_size = GetScreenSize()
      self.check_any_size(display_size, actual_size, Size(3, 3))
      self.check_for_shrinkage(original_size, actual_size)

      # Exit fullscreen
      esccmd.XTERM_WINOPS(esccmd.WINOP_FULLSCREEN,
                          esccmd.WINOP_FULLSCREEN_EXIT)
      self.delay_after_resize()

      self.check_for_shrinkage(original_size, GetScreenSize())

      # Toggle in
      esccmd.XTERM_WINOPS(esccmd.WINOP_FULLSCREEN,
                          esccmd.WINOP_FULLSCREEN_TOGGLE)
      self.delay_after_resize()

      self.check_for_shrinkage(original_size, GetScreenSize())

      # Toggle out
      esccmd.XTERM_WINOPS(esccmd.WINOP_FULLSCREEN,
                          esccmd.WINOP_FULLSCREEN_TOGGLE)
      self.delay_after_resize()

      self.check_for_shrinkage(original_size, GetScreenSize())
    else:
      original_size = GetScreenSize()
      display_size = GetDisplaySize()

      # Enter fullscreen
      esccmd.XTERM_WINOPS(esccmd.WINOP_FULLSCREEN,
                          esccmd.WINOP_FULLSCREEN_ENTER)
      time.sleep(1)
      actual_size = GetScreenSize()
      AssertTrue(actual_size.width() >= display_size.width())
      AssertTrue(actual_size.height() >= display_size.height())

      AssertTrue(actual_size.width() >= original_size.width())
      AssertTrue(actual_size.height() >= original_size.height())

      # Exit fullscreen
      esccmd.XTERM_WINOPS(esccmd.WINOP_FULLSCREEN,
                          esccmd.WINOP_FULLSCREEN_EXIT)
      AssertEQ(GetScreenSize(), original_size)

      # Toggle in
      esccmd.XTERM_WINOPS(esccmd.WINOP_FULLSCREEN,
                          esccmd.WINOP_FULLSCREEN_TOGGLE)
      AssertTrue(actual_size.width() >= display_size.width())
      AssertTrue(actual_size.height() >= display_size.height())

      AssertTrue(actual_size.width() >= original_size.width())
      AssertTrue(actual_size.height() >= original_size.height())

      # Toggle out
      esccmd.XTERM_WINOPS(esccmd.WINOP_FULLSCREEN,
                          esccmd.WINOP_FULLSCREEN_TOGGLE)
      AssertEQ(GetScreenSize(), original_size)

  @knownBug(terminal="iTerm2",
            reason="iTerm2 seems to report the window label instead of the icon label")
  def test_XtermWinops_ReportIconLabel(self):
    string = "test " + str(time.time())
    esccmd.ChangeIconTitle(string)
    AssertEQ(GetIconTitle(), string)

  def test_XtermWinops_ReportWindowLabel(self):
    string = "test " + str(time.time())
    esccmd.ChangeWindowTitle(string)
    AssertEQ(GetWindowTitle(), string)

  def test_XtermWinops_PushIconAndWindow_PopIconAndWindow(self):
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

  @knownBug(terminal="iTerm2", reason="The window title incorrectly changes when popping the icon title.")
  def test_XtermWinops_PushIconAndWindow_PopIcon(self):
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

  @knownBug(terminal="iTerm2", reason="The window title incorrectly changes when popping the icon title.")
  def test_XtermWinops_PushIconAndWindow_PopWindow(self):
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

  @knownBug(terminal="iTerm2",
            reason="iTerm2 pops twice while xterm pops only once for POP_TITLE_ICON_AND_WINDOW")
  def test_XtermWinops_PushIcon_PopIcon(self):
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

  @knownBug(terminal="iTerm2",
            reason="POP_TITLE_WINDOW incorrectly changes the icon title.")
  def test_XtermWinops_PushWindow_PopWindow(self):
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

  @knownBug(terminal="iTerm2",
            reason="iTerm2 pops twice while xterm pops only once for POP_TITLE_ICON_AND_WINDOW")
  def test_XtermWinops_PushIconThenWindowThenPopBoth(self):
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

  @knownBug(terminal="iTerm2",
            reason="iTerm2 incorrectly reports the window's title when the icon's title is requested.")
  def test_XtermWinops_PushMultiplePopMultiple_Icon(self):
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

  def test_XtermWinops_PushMultiplePopMultiple_Window(self):
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
    self.delay_after_resize()

    AssertEQ(GetScreenSize(), Size(90, 10))

    esccmd.XTERM_WINOPS(24)
    AssertEQ(GetScreenSize(), Size(90, 24))

    esccmd.XTERM_WINOPS(30)
    AssertEQ(GetScreenSize(), Size(90, 30))

from esc import empty, S7C1T, S8C1T
import escargs
import esccmd
import escio
from escutil import AssertEQ
from escutil import AssertScreenCharsInRectEqual
from escutil import GetCursorPosition
from escutil import GetScreenSize
from escutil import optionRequired
from escutil import vtLevel
from esctypes import Point, Rect

class NELTests(object):

  @classmethod
  def test_NEL_Basic(cls):
    """Next Line moves the cursor down one line and to the start of the next line."""
    esccmd.CUP(Point(5, 3))
    esccmd.NEL()
    position = GetCursorPosition()
    AssertEQ(position.x(), 1)
    AssertEQ(position.y(), 4)

  @classmethod
  @vtLevel(4)
  def test_NEL_Scrolls(cls):
    """Next Line scrolls when it hits the bottom."""
    height = GetScreenSize().height()

    # Put a and b on the last two lines.
    esccmd.CUP(Point(2, height - 1))
    escio.Write("a")
    esccmd.CUP(Point(2, height))
    escio.Write("b")

    # Move to penultimate line.
    esccmd.CUP(Point(2, height - 1))

    # Move down, ensure no scroll yet.
    esccmd.NEL()
    AssertEQ(GetCursorPosition(), Point(1, height))
    AssertScreenCharsInRectEqual(Rect(2, height - 2, 2, height), [empty(), "a", "b"])

    # Move down, ensure scroll.
    esccmd.NEL()
    AssertEQ(GetCursorPosition(), Point(1, height))
    AssertScreenCharsInRectEqual(Rect(2, height - 2, 2, height), ["a", "b", empty()])

  @classmethod
  @vtLevel(4)
  def test_NEL_ScrollsInTopBottomRegionStartingAbove(cls):
    """Next Line scrolls when it hits the bottom region (starting above top)."""
    esccmd.DECSTBM(4, 5)
    esccmd.CUP(Point(2, 5))
    escio.Write("x")

    esccmd.CUP(Point(2, 3))
    esccmd.NEL()  # To 4
    esccmd.NEL()  # To 5
    esccmd.NEL()  # Stay at 5 and scroll x up one line
    AssertEQ(GetCursorPosition(), Point(1, 5))
    AssertScreenCharsInRectEqual(Rect(2, 4, 2, 5), ["x", empty()])

  @classmethod
  @vtLevel(4)
  def test_NEL_ScrollsInTopBottomRegionStartingWithin(cls):
    """Next Line scrolls when it hits the bottom region (starting within region)."""
    esccmd.DECSTBM(4, 5)
    esccmd.CUP(Point(2, 5))
    escio.Write("x")

    esccmd.CUP(Point(2, 4))
    esccmd.NEL()  # To 5
    esccmd.NEL()  # Stay at 5 and scroll x up one line
    AssertEQ(GetCursorPosition(), Point(1, 5))
    AssertScreenCharsInRectEqual(Rect(2, 4, 2, 5), ["x", empty()])

  @classmethod
  @vtLevel(4)
  def test_NEL_MovesDoesNotScrollOutsideLeftRight(cls):
    """Cursor moves down but won't scroll when outside left-right region."""
    esccmd.DECSTBM(2, 5)
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(2, 5)
    esccmd.CUP(Point(3, 5))
    escio.Write("x")

    # Move past bottom margin but to the right of the left-right region
    esccmd.CUP(Point(6, 5))
    esccmd.NEL()
    # Cursor won't pass bottom or scroll.
    AssertEQ(GetCursorPosition(), Point(2, 5))
    AssertScreenCharsInRectEqual(Rect(3, 5, 3, 5), ["x"])

    # Cursor can move down a line without scrolling.
    esccmd.CUP(Point(6, 4))
    esccmd.NEL()
    AssertEQ(GetCursorPosition(), Point(2, 5))

    # Try to move past the bottom of the screen but to the right of the left-right region
    height = GetScreenSize().height()
    esccmd.CUP(Point(6, height))
    esccmd.NEL()
    AssertEQ(GetCursorPosition(), Point(2, height))
    AssertScreenCharsInRectEqual(Rect(3, 5, 3, 5), ["x"])

    # Move past bottom margin but to the left of the left-right region
    esccmd.CUP(Point(1, 5))
    esccmd.NEL()
    AssertEQ(GetCursorPosition(), Point(1, 5))
    AssertScreenCharsInRectEqual(Rect(3, 5, 3, 5), ["x"])

    # Try to move past the bottom of the screen but to the left of the left-right region
    height = GetScreenSize().height()
    esccmd.CUP(Point(1, height))
    esccmd.NEL()
    AssertEQ(GetCursorPosition(), Point(1, height))
    AssertScreenCharsInRectEqual(Rect(3, 5, 3, 5), ["x"])

  @classmethod
  @vtLevel(4)
  def test_NEL_StopsAtBottomLineWhenBegunBelowScrollRegion(cls):
    """When the cursor starts below the scroll region, Next Line moves it down to the
    bottom of the screen but won't scroll."""
    # Set a scroll region. This must be done first because DECSTBM moves the cursor to the origin.
    esccmd.DECSTBM(4, 5)

    # Position the cursor below the scroll region
    esccmd.CUP(Point(1, 6))
    escio.Write("x")

    # Move it down by a lot
    height = GetScreenSize().height()
    for _ in range(height):
      esccmd.NEL()

    # Ensure it stopped at the bottom of the screen
    AssertEQ(GetCursorPosition(), Point(1, height))

    # Ensure no scroll
    AssertScreenCharsInRectEqual(Rect(1, 6, 1, 6), ["x"])

  @classmethod
  @optionRequired(terminal="xterm", option=escargs.DISABLE_WIDE_CHARS, allowPassWithoutOption=escargs.ALLOW_C1_PRINTABLE)
  @optionRequired(terminal="iTerm2", option=escargs.DISABLE_WIDE_CHARS)
  @optionRequired(terminal="iTerm2beta", option=escargs.DISABLE_WIDE_CHARS)
  def test_NEL_8bit(cls):
    esccmd.CUP(Point(5, 3))

    escio.use8BitControls = True
    escio.Write(S8C1T)
    esccmd.NEL()
    escio.Write(S7C1T)
    escio.use8BitControls = False

    position = GetCursorPosition()
    AssertEQ(position.x(), 1)
    AssertEQ(position.y(), 4)

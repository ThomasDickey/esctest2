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

class RITests(object):

  @classmethod
  def test_RI_Basic(cls):
    """Reverse index moves the cursor up one line."""
    esccmd.CUP(Point(5, 3))
    esccmd.RI()
    position = GetCursorPosition()
    AssertEQ(position.x(), 5)
    AssertEQ(position.y(), 2)

  @classmethod
  @vtLevel(4)
  def test_RI_Scrolls(cls):
    """Reverse index scrolls when it hits the top."""
    # Put a and b on the last two lines.
    esccmd.CUP(Point(2, 1))
    escio.Write("a")
    esccmd.CUP(Point(2, 2))
    escio.Write("b")

    # Move to second line.
    esccmd.CUP(Point(2, 2))

    # Move up, ensure no scroll yet.
    esccmd.RI()
    AssertEQ(GetCursorPosition().y(), 1)
    AssertScreenCharsInRectEqual(Rect(2, 1, 2, 3), ["a", "b", empty()])

    # Move up, ensure scroll.
    esccmd.RI()
    AssertEQ(GetCursorPosition().y(), 1)
    AssertScreenCharsInRectEqual(Rect(2, 1, 2, 3), [empty(), "a", "b"])

  @classmethod
  @vtLevel(4)
  def test_RI_ScrollsInTopBottomRegionStartingBelow(cls):
    """Reverse index scrolls when it hits the top region (starting below bottom)."""
    esccmd.DECSTBM(4, 5)
    esccmd.CUP(Point(2, 4))
    escio.Write("x")

    esccmd.CUP(Point(2, 6))
    esccmd.RI()  # To 5
    esccmd.RI()  # To 4
    esccmd.RI()  # Stay at 4 and scroll x down one line
    AssertEQ(GetCursorPosition(), Point(2, 4))
    AssertScreenCharsInRectEqual(Rect(2, 4, 2, 5), [empty(), "x"])

  @classmethod
  @vtLevel(4)
  def test_RI_ScrollsInTopBottomRegionStartingWithin(cls):
    """Reverse index scrolls when it hits the top (starting within region)."""
    esccmd.DECSTBM(4, 5)
    esccmd.CUP(Point(2, 4))
    escio.Write("x")

    esccmd.CUP(Point(2, 5))
    esccmd.RI()  # To 4
    esccmd.RI()  # Stay at 4 and scroll x down one line
    AssertEQ(GetCursorPosition(), Point(2, 4))
    AssertScreenCharsInRectEqual(Rect(2, 4, 2, 5), [empty(), "x"])

  @classmethod
  @vtLevel(4)
  def test_RI_MovesDoesNotScrollOutsideLeftRight(cls):
    """Cursor moves down but won't scroll when outside left-right region."""
    esccmd.DECSTBM(2, 5)
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(2, 5)
    esccmd.CUP(Point(3, 5))
    escio.Write("x")

    # Move past bottom margin but to the right of the left-right region
    esccmd.CUP(Point(6, 2))
    esccmd.RI()
    # Cursor won't pass bottom or scroll.
    AssertEQ(GetCursorPosition(), Point(6, 2))
    AssertScreenCharsInRectEqual(Rect(3, 5, 3, 5), ["x"])

    # Try to move past the top of the screen but to the right of the left-right region
    esccmd.CUP(Point(6, 1))
    esccmd.RI()
    AssertEQ(GetCursorPosition(), Point(6, 1))
    AssertScreenCharsInRectEqual(Rect(3, 5, 3, 5), ["x"])

    # Move past top margin but to the left of the left-right region
    esccmd.CUP(Point(1, 2))
    esccmd.RI()
    AssertEQ(GetCursorPosition(), Point(1, 2))
    AssertScreenCharsInRectEqual(Rect(3, 5, 3, 5), ["x"])

    # Try to move past the top of the screen but to the left of the left-right region
    esccmd.CUP(Point(1, 1))
    esccmd.RI()
    AssertEQ(GetCursorPosition(), Point(1, 1))
    AssertScreenCharsInRectEqual(Rect(3, 5, 3, 5), ["x"])

  @classmethod
  @vtLevel(4)
  def test_RI_StopsAtTopLineWhenBegunAboveScrollRegion(cls):
    """When the cursor starts above the scroll region, reverse index moves it
    up to the top of the screen but won't scroll."""
    # Set a scroll region. This must be done first because DECSTBM moves the
    # cursor to the origin.
    esccmd.DECSTBM(4, 5)

    # Position the cursor above the scroll region
    esccmd.CUP(Point(1, 3))
    escio.Write("x")

    # Move it up by a lot
    height = GetScreenSize().height()
    for _ in range(height):
      esccmd.RI()

    # Ensure it stopped at the top of the screen
    AssertEQ(GetCursorPosition().y(), 1)

    # Ensure no scroll
    AssertScreenCharsInRectEqual(Rect(1, 3, 1, 3), ["x"])

  @classmethod
  @optionRequired(terminal="xterm", option=escargs.DISABLE_WIDE_CHARS, allowPassWithoutOption=escargs.ALLOW_C1_PRINTABLE)
  @optionRequired(terminal="iTerm2", option=escargs.DISABLE_WIDE_CHARS)
  @optionRequired(terminal="iTerm2beta", option=escargs.DISABLE_WIDE_CHARS)
  def test_RI_8bit(cls):
    esccmd.CUP(Point(5, 3))

    escio.use8BitControls = True
    escio.Write(S8C1T)
    esccmd.RI()
    escio.Write(S7C1T)
    escio.use8BitControls = False

    position = GetCursorPosition()
    AssertEQ(position.x(), 5)
    AssertEQ(position.y(), 2)

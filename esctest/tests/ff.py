from esc import FF, empty

import esccmd
import escio

from escutil import AssertEQ
from escutil import AssertScreenCharsInRectEqual
from escutil import GetCursorPosition
from escutil import GetScreenSize
from escutil import knownBug
from escutil import vtLevel
from esctypes import Point, Rect

class FFTests(object):
  """LNM is tested in the SM tests, and not duplicated here. These tests are
  the same as those for IND."""

  @classmethod
  def test_FF_Basic(cls):
    """FF moves the cursor down one line."""
    esccmd.CUP(Point(5, 3))
    escio.Write(FF)
    position = GetCursorPosition()
    AssertEQ(position.x(), 5)
    AssertEQ(position.y(), 4)

  @classmethod
  @vtLevel(4)
  def test_FF_Scrolls(cls):
    """FF scrolls when it hits the bottom."""
    height = GetScreenSize().height()

    # Put a and b on the last two lines.
    esccmd.CUP(Point(2, height - 1))
    escio.Write("a")
    esccmd.CUP(Point(2, height))
    escio.Write("b")

    # Move to penultimate line.
    esccmd.CUP(Point(2, height - 1))

    # Move down, ensure no scroll yet.
    escio.Write(FF)
    AssertEQ(GetCursorPosition().y(), height)
    AssertScreenCharsInRectEqual(Rect(2, height - 2, 2, height), [empty(), "a", "b"])

    # Move down, ensure scroll.
    escio.Write(FF)
    AssertEQ(GetCursorPosition().y(), height)
    AssertScreenCharsInRectEqual(Rect(2, height - 2, 2, height), ["a", "b", empty()])

  @classmethod
  @vtLevel(4)
  def test_FF_ScrollsInTopBottomRegionStartingAbove(cls):
    """FF scrolls when it hits the bottom region (starting above top)."""
    esccmd.DECSTBM(4, 5)
    esccmd.CUP(Point(2, 5))
    escio.Write("x")

    esccmd.CUP(Point(2, 3))
    escio.Write(FF)
    escio.Write(FF)
    escio.Write(FF)
    AssertEQ(GetCursorPosition(), Point(2, 5))
    AssertScreenCharsInRectEqual(Rect(2, 4, 2, 5), ["x", empty()])

  @classmethod
  @vtLevel(4)
  def test_FF_ScrollsInTopBottomRegionStartingWithin(cls):
    """FF scrolls when it hits the bottom region (starting within region)."""
    esccmd.DECSTBM(4, 5)
    esccmd.CUP(Point(2, 5))
    escio.Write("x")

    esccmd.CUP(Point(2, 4))
    escio.Write(FF)
    escio.Write(FF)
    AssertEQ(GetCursorPosition(), Point(2, 5))
    AssertScreenCharsInRectEqual(Rect(2, 4, 2, 5), ["x", empty()])

  @classmethod
  @vtLevel(4)
  def test_FF_MovesDoesNotScrollOutsideLeftRight(cls):
    """Cursor moves down but won't scroll when outside left-right region."""
    esccmd.DECSTBM(2, 5)
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(2, 5)
    esccmd.CUP(Point(3, 5))
    escio.Write("x")

    # Move past bottom margin but to the right of the left-right region
    esccmd.CUP(Point(6, 5))
    escio.Write(FF)
    # Cursor won't pass bottom or scroll.
    AssertEQ(GetCursorPosition(), Point(6, 5))
    AssertScreenCharsInRectEqual(Rect(3, 5, 3, 5), ["x"])

    # Cursor can move down
    esccmd.CUP(Point(6, 4))
    escio.Write(FF)
    AssertEQ(GetCursorPosition(), Point(6, 5))

    # Try to move past the bottom of the screen but to the right of the left-right region
    height = GetScreenSize().height()
    esccmd.CUP(Point(6, height))
    escio.Write(FF)
    AssertEQ(GetCursorPosition(), Point(6, height))
    AssertScreenCharsInRectEqual(Rect(3, 5, 3, 5), ["x"])

    # Move past bottom margin but to the left of the left-right region
    esccmd.CUP(Point(1, 5))
    escio.Write(FF)
    AssertEQ(GetCursorPosition(), Point(1, 5))
    AssertScreenCharsInRectEqual(Rect(3, 5, 3, 5), ["x"])

    # Try to move past the bottom of the screen but to the left of the left-right region
    height = GetScreenSize().height()
    esccmd.CUP(Point(1, height))
    escio.Write(FF)
    AssertEQ(GetCursorPosition(), Point(1, height))
    AssertScreenCharsInRectEqual(Rect(3, 5, 3, 5), ["x"])

  @classmethod
  @vtLevel(4)
  def test_FF_StopsAtBottomLineWhenBegunBelowScrollRegion(cls):
    """When the cursor starts below the scroll region, index moves it down to the
    bottom of the screen but won't scroll."""
    # Set a scroll region. This must be done first because DECSTBM moves the cursor to the origin.
    esccmd.DECSTBM(4, 5)

    # Position the cursor below the scroll region
    esccmd.CUP(Point(1, 6))
    escio.Write("x")

    # Move it down by a lot
    height = GetScreenSize().height()
    for _ in range(height):
      escio.Write(FF)

    # Ensure it stopped at the bottom of the screen
    AssertEQ(GetCursorPosition().y(), height)

    # Ensure no scroll
    AssertScreenCharsInRectEqual(Rect(1, 6, 1, 6), ["x"])

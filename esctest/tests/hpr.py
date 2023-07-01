from esc import empty
import esccmd
import escio
from escutil import AssertEQ
from escutil import AssertScreenCharsInRectEqual
from escutil import GetCursorPosition
from escutil import GetScreenSize
from escutil import knownBug
from escutil import vtLevel
from esctypes import Point, Rect

class HPRTests(object):

  @classmethod
  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_HPR_DefaultParams(cls):
    """With no params, HPR moves right by 1."""
    esccmd.CUP(Point(6, 1))
    esccmd.HPR()

    position = GetCursorPosition()
    AssertEQ(position.x(), 7)

  @classmethod
  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_HPR_StopsAtRightEdge(cls):
    """HPR won't go past the right edge."""
    # Position on 6th row
    esccmd.CUP(Point(5, 6))

    # Try to move 10 past the right edge
    size = GetScreenSize()
    esccmd.HPR(size.width() + 10)

    # Ensure at the right edge on same row
    position = GetCursorPosition()
    AssertEQ(position.x(), size.width())
    AssertEQ(position.y(), 6)

  @classmethod
  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_HPR_DoesNotChangeRow(cls):
    """HPR moves the specified column and does not change the row."""
    esccmd.CUP(Point(5, 6))
    esccmd.HPR(2)

    position = GetCursorPosition()
    AssertEQ(position.x(), 7)
    AssertEQ(position.y(), 6)

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  @knownBug(terminal="iTerm2beta", reason="Erase fills rather than clears.")
  def test_HPR_IgnoresOriginMode(cls):
    """HPR continues to work in origin mode."""
    # Set a scroll region.
    esccmd.DECSTBM(6, 11)
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(5, 10)

    # Enter origin mode
    esccmd.DECSET(esccmd.DECOM)

    # Move to center of region
    esccmd.CUP(Point(2, 2))
    escio.Write('X')

    # Move right by 2
    esccmd.HPR(2)
    escio.Write('Y')

    # Exit origin mode
    esccmd.DECRESET(esccmd.DECOM)

    # Reset margins
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSTBM()

    # See what happened
    AssertScreenCharsInRectEqual(Rect(5, 7, 9, 7), [empty() + "X" + empty() * 2 + "Y"])

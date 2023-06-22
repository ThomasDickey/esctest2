from esc import empty
import esccmd
import escio
from escutil import AssertEQ
from escutil import AssertScreenCharsInRectEqual
from escutil import GetCursorPosition
from escutil import GetScreenSize
from escutil import vtLevel
from esctypes import Point, Rect

class VPRTests(object):

  @classmethod
  def test_VPR_DefaultParams(cls):
    """With no params, VPR moves right by 1."""
    esccmd.CUP(Point(1, 6))
    esccmd.VPR()

    position = GetCursorPosition()
    AssertEQ(position.y(), 7)

  @classmethod
  def test_VPR_StopsAtBottomEdge(cls):
    """VPR won't go past the bottom edge."""
    # Position on 5th column
    esccmd.CUP(Point(5, 6))

    # Try to move 10 past the bottom edge
    size = GetScreenSize()
    esccmd.VPR(size.height() + 10)

    # Ensure at the bottom edge on same column
    position = GetCursorPosition()
    AssertEQ(position.x(), 5)
    AssertEQ(position.y(), size.height())

  @classmethod
  def test_VPR_DoesNotChangeColumn(cls):
    """VPR moves the specified row and does not change the column."""
    esccmd.CUP(Point(5, 6))
    esccmd.VPR(2)

    position = GetCursorPosition()
    AssertEQ(position.x(), 5)
    AssertEQ(position.y(), 8)

  @classmethod
  @vtLevel(4)
  def test_VPR_IgnoresOriginMode(cls):
    """VPR continues to work in origin mode."""
    # Set a scroll region.
    esccmd.DECSTBM(6, 11)
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(5, 10)

    # Enter origin mode
    esccmd.DECSET(esccmd.DECOM)

    # Move to center of region
    esccmd.CUP(Point(2, 2))
    escio.Write('X')

    # Move down by 2
    esccmd.VPR(2)
    escio.Write('Y')

    # Exit origin mode
    esccmd.DECRESET(esccmd.DECOM)

    # Reset margins
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSTBM()

    # See what happened
    AssertScreenCharsInRectEqual(Rect(6, 7, 7, 9), ['X' + empty(),
                                                    empty() * 2,
                                                    empty() + 'Y'])

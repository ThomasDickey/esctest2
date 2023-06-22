import esccmd
import escio
from escutil import AssertEQ
from escutil import AssertScreenCharsInRectEqual
from escutil import GetCursorPosition
from escutil import GetScreenSize
from escutil import vtLevel
from esctypes import Point, Rect

class CUPTests(object):

  @classmethod
  def test_CUP_DefaultParams(cls):
    """With no params, CUP moves to 1,1."""
    esccmd.CUP(Point(6, 3))

    position = GetCursorPosition()
    AssertEQ(position.x(), 6)
    AssertEQ(position.y(), 3)

    esccmd.CUP()

    position = GetCursorPosition()
    AssertEQ(position.x(), 1)
    AssertEQ(position.y(), 1)

  @classmethod
  def test_CUP_RowOnly(cls):
    """Default column is 1."""
    esccmd.CUP(Point(6, 3))

    position = GetCursorPosition()
    AssertEQ(position.x(), 6)
    AssertEQ(position.y(), 3)

    esccmd.CUP(row=2)

    position = GetCursorPosition()
    AssertEQ(position.x(), 1)
    AssertEQ(position.y(), 2)

  @classmethod
  def test_CUP_ColumnOnly(cls):
    """Default row is 1."""
    esccmd.CUP(Point(6, 3))

    position = GetCursorPosition()
    AssertEQ(position.x(), 6)
    AssertEQ(position.y(), 3)

    esccmd.CUP(col=2)

    position = GetCursorPosition()
    AssertEQ(position.x(), 2)
    AssertEQ(position.y(), 1)

  @classmethod
  def test_CUP_ZeroIsTreatedAsOne(cls):
    """Zero args are treated as 1."""
    esccmd.CUP(Point(6, 3))
    esccmd.CUP(col=0, row=0)
    position = GetCursorPosition()
    AssertEQ(position.x(), 1)
    AssertEQ(position.y(), 1)

  @classmethod
  def test_CUP_OutOfBoundsParams(cls):
    """With overly large parameters, CUP moves as far as possible down and right."""
    size = GetScreenSize()
    esccmd.CUP(Point(size.width() + 10, size.height() + 10))

    position = GetCursorPosition()
    AssertEQ(position.x(), size.width())
    AssertEQ(position.y(), size.height())

  @classmethod
  @vtLevel(4)
  def test_CUP_RespectsOriginMode(cls):
    """CUP is relative to margins in origin mode."""
    # Set a scroll region.
    esccmd.DECSTBM(6, 11)
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(5, 10)

    # Move to center of region
    esccmd.CUP(Point(7, 9))
    position = GetCursorPosition()
    AssertEQ(position.x(), 7)
    AssertEQ(position.y(), 9)

    # Turn on origin mode.
    esccmd.DECSET(esccmd.DECOM)

    # Move to top-left
    esccmd.CUP(Point(1, 1))

    # Check relative position while still in origin mode.
    position = GetCursorPosition()
    AssertEQ(position.x(), 1)
    AssertEQ(position.y(), 1)

    escio.Write("X")

    # Turn off origin mode. This moves the cursor.
    esccmd.DECRESET(esccmd.DECOM)

    # Turn off scroll regions so checksum can work.
    esccmd.DECSTBM()
    esccmd.DECRESET(esccmd.DECLRMM)

    # Make sure there's an X at 5,6
    AssertScreenCharsInRectEqual(Rect(5, 6, 5, 6),
                                 ["X"])

from esc import TAB
import esccmd
import escio
from escutil import AssertEQ, GetCursorPosition, vtLevel
from esctypes import Point

class TBCTests(object):

  @classmethod
  @vtLevel(1)
  def test_TBC_Default(cls):
    """No param clears the tab stop at the cursor."""
    escio.Write(TAB)
    AssertEQ(GetCursorPosition().x(), 9)
    esccmd.TBC()
    esccmd.CUP(Point(1, 1))
    escio.Write(TAB)
    AssertEQ(GetCursorPosition().x(), 17)

  @classmethod
  @vtLevel(1)
  def test_TBC_0(cls):
    """0 param clears the tab stop at the cursor."""
    escio.Write(TAB)
    AssertEQ(GetCursorPosition().x(), 9)
    esccmd.TBC(0)
    esccmd.CUP(Point(1, 1))
    escio.Write(TAB)
    AssertEQ(GetCursorPosition().x(), 17)

  @classmethod
  @vtLevel(1)
  def test_TBC_3(cls):
    """3 param clears all tab stops."""
    # Remove all tab stops
    esccmd.TBC(3)

    # Set a tab stop at 30
    esccmd.CUP(Point(30, 1))
    esccmd.HTS()

    # Move back to the start and then tab. Should go to 30.
    esccmd.CUP(Point(1, 1))
    escio.Write(TAB)
    AssertEQ(GetCursorPosition().x(), 30)

  @classmethod
  @vtLevel(1)
  def test_TBC_NoOp(cls):
    """Clearing a nonexistent tab stop should do nothing."""
    # Move to 10 and clear the tab stop
    esccmd.CUP(Point(10, 1))
    esccmd.TBC(0)

    # Move to 1 and tab twice, ensuring the stops at 9 and 17 are still there.
    esccmd.CUP(Point(1, 1))
    escio.Write(TAB)
    AssertEQ(GetCursorPosition().x(), 9)
    escio.Write(TAB)
    AssertEQ(GetCursorPosition().x(), 17)

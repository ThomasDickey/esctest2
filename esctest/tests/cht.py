import esccmd
from esctypes import Point
from escutil import AssertEQ, GetCursorPosition, vtLevel

class CHTTests(object):

  @classmethod
  def test_CHT_OneTabStopByDefault(cls):
    esccmd.CHT()
    position = GetCursorPosition()
    AssertEQ(position.x(), 9)

  @classmethod
  def test_CHT_ExplicitParameter(cls):
    esccmd.CHT(2)
    position = GetCursorPosition()
    AssertEQ(position.x(), 17)

  @classmethod
  @vtLevel(4)
  def test_CHT_IgnoresScrollingRegion(cls):
    """Test cursor forward tab (ECMA-48).

    CHT is just a parameterized tab.
    In DEC terminals (and compatible such as xterm),
    tabs stop at the right margin.
    ECMA-48 does not specify margins, so the behavior follows DEC.
    """
    # Set a scroll region.
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(5, 30)

    # Move to center of region
    esccmd.CUP(Point(7, 9))

    # Ensure we can tab within the region
    esccmd.CHT(2)
    position = GetCursorPosition()
    AssertEQ(position.x(), 17)

    # Ensure that we can't tab out of the region
    esccmd.CHT(2)
    position = GetCursorPosition()
    AssertEQ(position.x(), 30)

    # Try again, starting before the region.
    esccmd.CUP(Point(1, 9))
    esccmd.CHT(9)
    position = GetCursorPosition()
    AssertEQ(position.x(), 30)

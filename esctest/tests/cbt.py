import esccmd
from esctypes import Point
from escutil import AssertEQ, GetCursorPosition, vtLevel

class CBTTests(object):
  @classmethod
  def test_CBT_OneTabStopByDefault(cls):
    esccmd.CUP(Point(17, 1))
    esccmd.CBT()
    position = GetCursorPosition()
    AssertEQ(position.x(), 9)

  @classmethod
  def test_CBT_ExplicitParameter(cls):
    esccmd.CUP(Point(25, 1))
    esccmd.CBT(2)
    position = GetCursorPosition()
    AssertEQ(position.x(), 9)

  @classmethod
  def test_CBT_StopsAtLeftEdge(cls):
    esccmd.CUP(Point(25, 2))
    esccmd.CBT(5)
    position = GetCursorPosition()
    AssertEQ(position.x(), 1)
    AssertEQ(position.y(), 2)

  @classmethod
  @vtLevel(4)
  def test_CBT_IgnoresRegion(cls):
    # Set a scroll region.
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(5, 30)

    # Move to center of region
    esccmd.CUP(Point(7, 9))

    # Tab backwards out of the region.
    esccmd.CBT(2)
    position = GetCursorPosition()
    AssertEQ(position.x(), 1)

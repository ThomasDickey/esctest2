import esccmd
from escutil import AssertEQ, GetCursorPosition, GetScreenSize, vtLevel
from esctypes import Point

class CPLTests(object):

  @classmethod
  def test_CPL_DefaultParam(cls):
    """CPL moves the cursor up 1 with no parameter given."""
    esccmd.CUP(Point(5, 3))
    esccmd.CPL()
    position = GetCursorPosition()
    AssertEQ(position.x(), 1)
    AssertEQ(position.y(), 2)

  @classmethod
  def test_CPL_ExplicitParam(cls):
    """CPL moves the cursor up by the passed-in number of lines."""
    esccmd.CUP(Point(6, 5))
    esccmd.CPL(2)
    position = GetCursorPosition()
    AssertEQ(position.x(), 1)
    AssertEQ(position.y(), 3)

  @classmethod
  def test_CPL_StopsAtTopLine(cls):
    """CPL moves the cursor up, stopping at the last line."""
    esccmd.CUP(Point(6, 3))
    height = GetScreenSize().height()
    esccmd.CPL(height)
    position = GetCursorPosition()
    AssertEQ(position.x(), 1)
    AssertEQ(position.y(), 1)

  @classmethod
  @vtLevel(4)
  def test_CPL_StopsAtTopLineWhenBegunAboveScrollRegion(cls):
    """When the cursor starts above the scroll region, CPL moves it up to the
    top of the screen."""
    # Set a scroll region. This must be done first because DECSTBM moves the cursor to the origin.
    esccmd.DECSTBM(4, 5)
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(5, 10)

    # Position the cursor below the scroll region
    esccmd.CUP(Point(7, 3))

    # Move it up by a lot
    height = GetScreenSize().height()
    esccmd.CPL(height)

    # Ensure it stopped at the top of the screen
    position = GetCursorPosition()
    AssertEQ(position.y(), 1)
    AssertEQ(position.x(), 5)

  @classmethod
  @vtLevel(4)
  def test_CPL_StopsAtTopMarginInScrollRegion(cls):
    """When the cursor starts within the scroll region, CPL moves it up to the
    top margin but no farther."""
    # Set a scroll region. This must be done first because DECSTBM moves the cursor to the origin.
    esccmd.DECSTBM(2, 4)
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(5, 10)

    # Position the cursor within the scroll region
    esccmd.CUP(Point(7, 3))

    # Move it up by more than the height of the scroll region
    esccmd.CPL(99)

    # Ensure it stopped at the top of the scroll region.
    position = GetCursorPosition()
    AssertEQ(position.y(), 2)
    AssertEQ(position.x(), 5)

import escargs
import esccmd
import escio

from esccmd import CUB
from esccmd import CUP
from esccmd import DECSET
from esccmd import DECSLRM

from escutil import AssertEQ
from escutil import GetCursorPosition
from escutil import GetScreenSize
from escutil import knownBug
from escutil import vtLevel

from esctypes import Point

class CUBTests(object):

  @classmethod
  def test_CUB_DefaultParam(cls):
    """CUB moves the cursor left 1 with no parameter given."""
    CUP(Point(5, 3))
    CUB()
    position = GetCursorPosition()
    AssertEQ(position.x(), 4)
    AssertEQ(position.y(), 3)

  @classmethod
  def test_CUB_ExplicitParam(cls):
    """CUB moves the cursor left by the passed-in number of columns."""
    CUP(Point(5, 4))
    CUB(2)
    AssertEQ(GetCursorPosition().x(), 3)

  @classmethod
  def test_CUB_StopsAtLeftEdge(cls):
    """CUB moves the cursor left, stopping at the first column."""
    CUP(Point(5, 3))
    CUB(99)
    AssertEQ(GetCursorPosition().x(), 1)

  @classmethod
  @vtLevel(4)
  def test_CUB_StopsAtLeftEdgeWhenBegunLeftOfScrollRegion(cls):
    """When the cursor starts left of the scroll region, CUB moves it left to the
    left edge of the screen."""
    # Set a scroll region.
    DECSET(esccmd.DECLRMM)
    DECSLRM(5, 10)

    # Position the cursor left of the scroll region
    CUP(Point(4, 3))

    # Move it left by a lot
    CUB(99)

    # Ensure it stopped at the left edge of the screen
    AssertEQ(GetCursorPosition().x(), 1)

  @classmethod
  @vtLevel(4)
  def test_CUB_StopsAtLeftMarginInScrollRegion(cls):
    """When the cursor starts within the scroll region, CUB moves it left to the
    left margin but no farther."""
    # Set a scroll region. This must be done first because DECSTBM moves the cursor to the origin.
    DECSET(esccmd.DECLRMM)
    DECSLRM(5, 10)

    # Position the cursor within the scroll region
    CUP(Point(7, 3))

    # Move it left by more than the height of the scroll region
    CUB(99)

    # Ensure it stopped at the top of the scroll region.
    AssertEQ(GetCursorPosition().x(), 5)

  @classmethod
  @knownBug(terminal="iTerm2", reason="Differs from xterm.")
  @knownBug(terminal="iTerm2beta", reason="Differs from xterm.")
  def test_CUB_AfterNoWrappedInlines(cls):
    '''Backspace after lines that did not wrap will not wrap to prior lines'''
    DECSET(esccmd.DECAWM)
    DECSET(esccmd.ReverseWrapInline)
    size = GetScreenSize()
    fill = "*" * (size.width() - 2) + "\n"
    CUP(Point(1, 3))
    # write two lines without wrapping
    escio.Write(fill)
    escio.Write(fill)
    # write enough backspaces to go before the two lines, if unconstrained
    CUP(Point(5, 5))
    CUB(size.width() * 2)
    if escargs.args.xterm_reverse_wrap >= 383:
      AssertEQ(GetCursorPosition(), Point(1, 4))
    else:
      AssertEQ(GetCursorPosition(), Point(5, 3))

  @classmethod
  @knownBug(terminal="iTerm2", reason="Differs from xterm.")
  @knownBug(terminal="iTerm2beta", reason="Differs from xterm.")
  def test_CUB_AfterOneWrappedInline(cls):
    '''Backspace after wrapped line may wrap to the beginning of the line.'''
    DECSET(esccmd.DECAWM)
    DECSET(esccmd.ReverseWrapInline)
    size = GetScreenSize()
    fill = "*" * (size.width() + 2) * 2
    # write two copies of filler, each a little longer than the line size.
    CUP(Point(1, 3))
    escio.Write(fill + "\n" + fill)
    # backspace enough to go before both copies, if unconstrained
    CUB(size.width() * 5)
    if escargs.args.xterm_reverse_wrap >= 383:
      AssertEQ(GetCursorPosition(), Point(1, 6))
    else:
      AssertEQ(GetCursorPosition(), Point(9, 3))

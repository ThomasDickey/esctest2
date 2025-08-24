import esc
import escargs
import esccmd
import escio

from esccmd import CUP
from esccmd import DECSET
from esccmd import DECRESET
from esccmd import DECSLRM
from esccmd import DECSTBM

from escutil import AssertEQ
from escutil import AssertScreenCharsInRectEqual
from escutil import GetCursorPosition
from escutil import GetScreenSize
from escutil import knownBug
from escutil import vtLevel

from esctypes import Point, Rect

class BSTests(object):

  @classmethod
  def test_BS_Basic(cls):
    CUP(Point(3, 3))
    escio.Write(esc.BS)
    AssertEQ(GetCursorPosition(), Point(2, 3))

  @classmethod
  def test_BS_NoWrapByDefault(cls):
    CUP(Point(1, 3))
    escio.Write(esc.BS)
    AssertEQ(GetCursorPosition(), Point(1, 3))

  @classmethod
  def test_BS_WrapsInWraparoundMode(cls):
    DECSET(esccmd.DECAWM)
    DECSET(esccmd.ReverseWraparound())
    CUP(Point(1, 3))
    escio.Write(esc.BS)
    size = GetScreenSize()
    AssertEQ(GetCursorPosition(), Point(size.width(), 2))

  @classmethod
  def test_BS_InitialReverseWraparound(cls):
    DECSET(esccmd.DECAWM)
    DECSET(esccmd.ReverseWrapInline)
    CUP(Point(1, 1))
    esccmd.NEL() # moves to next line without setting wrap flag
    escio.Write(esc.BS) # does not move to previous (non-wrapped) line
    AssertEQ(GetCursorPosition(), Point(1, 2))

  @classmethod
  def test_BS_ReverseWrapRequiresDECAWM(cls):
    DECRESET(esccmd.DECAWM)
    DECSET(esccmd.ReverseWraparound())
    CUP(Point(1, 3))
    escio.Write(esc.BS)
    AssertEQ(GetCursorPosition(), Point(1, 3))

    DECSET(esccmd.DECAWM)
    DECRESET(esccmd.ReverseWraparound())
    CUP(Point(1, 3))
    escio.Write(esc.BS)
    AssertEQ(GetCursorPosition(), Point(1, 3))

  @classmethod
  @vtLevel(4)
  def test_BS_ReverseWrapWithLeftRight(cls):
    DECSET(esccmd.DECAWM)
    DECSET(esccmd.ReverseWraparound())
    DECSET(esccmd.DECLRMM)
    DECSLRM(5, 10)
    CUP(Point(5, 3))
    escio.Write(esc.BS)
    AssertEQ(GetCursorPosition(), Point(10, 2))

  @classmethod
  @vtLevel(4)
  def test_BS_ReversewrapFromLeftEdgeToRightMargin(cls):
    """If cursor starts at left edge of screen, left of left margin, backspace
    takes it to the right margin."""
    DECSET(esccmd.DECAWM)
    DECSET(esccmd.ReverseWraparound())
    DECSET(esccmd.DECLRMM)
    DECSLRM(5, 10)
    CUP(Point(1, 3))
    escio.Write(esc.BS)
    AssertEQ(GetCursorPosition(), Point(10, 2))

  @classmethod
  @knownBug(terminal="iTerm2", reason="Does not wrap around properly")
  @knownBug(terminal="iTerm2beta", reason="Does not wrap around properly")
  def test_BS_ReverseWrapGoesToBottom(cls):
    """If the cursor starts within the top/bottom margins, after doing a
    reverse wrap, the cursor remains within those margins.

    Reverse-wrap is a feature of xterm since its first release in 1986.
    The X10.4 version would reverse-wrap (as some hardware terminals did)
    from the upper-left corner of the screen to the lower-right.

    Left/right margin support, which was added to xterm in 2012,
    modified the reverse-wrap feature to limit the cursor to those margins.

    Because top/bottom margins should be treated consistently,
    xterm was modified in 2018 to further amend the handling of
    reverse-wrap.

    In 2023, xterm was modified to change the behavior of private mode 45
    to limit it to the original goal (assisting editing of long wrapped
    lines), and add a new private mode 1045 which behaves like the original
    private mode (allowing wrapping around the top/bottom lines)."""
    DECSET(esccmd.DECAWM)
    DECSET(esccmd.ReverseWraparound())
    DECSTBM(2, 5)
    CUP(Point(1, 2))
    escio.Write(esc.BS)
    AssertEQ(GetCursorPosition(), Point(80, 5))

  @classmethod
  @vtLevel(4)
  def test_BS_StopsAtLeftMargin(cls):
    DECSET(esccmd.DECLRMM)
    DECSLRM(5, 10)
    CUP(Point(5, 1))
    escio.Write(esc.BS)
    DECRESET(esccmd.DECLRMM)
    AssertEQ(GetCursorPosition(), Point(5, 1))

  @classmethod
  @vtLevel(4)
  def test_BS_MovesLeftWhenLeftOfLeftMargin(cls):
    DECSET(esccmd.DECLRMM)
    DECSLRM(5, 10)
    CUP(Point(4, 1))
    escio.Write(esc.BS)
    DECRESET(esccmd.DECLRMM)
    AssertEQ(GetCursorPosition(), Point(3, 1))

  @classmethod
  def test_BS_StopsAtOrigin(cls):
    CUP(Point(1, 1))
    escio.Write(esc.BS)
    AssertEQ(GetCursorPosition(), Point(1, 1))

  @classmethod
  @vtLevel(4)
  def test_BS_CursorStartsInDoWrapPosition(cls):
    """Cursor is right of right edge of screen."""
    size = GetScreenSize()
    CUP(Point(size.width() - 1, 1))
    escio.Write("ab")
    escio.Write(esc.BS)
    escio.Write("X")
    AssertScreenCharsInRectEqual(Rect(size.width() - 1, 1, size.width(), 1),
                                 ["Xb"])

  @classmethod
  @vtLevel(4)
  def test_BS_ReverseWrapStartingInDoWrapPosition(cls):
    """Cursor is right of right edge of screen."""
    esccmd.DECSET(esccmd.DECAWM)
    esccmd.DECSET(esccmd.ReverseWraparound())
    size = GetScreenSize()
    esccmd.CUP(Point(size.width() - 1, 1))
    escio.Write("ab")
    escio.Write(esc.BS)
    escio.Write("X")
    AssertScreenCharsInRectEqual(Rect(size.width() - 1, 1, size.width(), 1),
                                 ["aX"])

  @classmethod
  def test_BS_AfterNoWrappedInlines(cls):
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
    escio.Write(esc.BS * size.width() * 2)
    if escargs.args.xterm_reverse_wrap >= 383:
      AssertEQ(GetCursorPosition(), Point(1, 4))
    else:
      AssertEQ(GetCursorPosition(), Point(5, 3))

  @classmethod
  def test_BS_AfterOneWrappedInline(cls):
    '''Backspace after wrapped line may wrap to the beginning of the line.'''
    DECSET(esccmd.DECAWM)
    DECSET(esccmd.ReverseWrapInline)
    size = GetScreenSize()
    fill = "*" * (size.width() + 2) * 2
    # write two copies of filler, each a little longer than the line size.
    CUP(Point(1, 3))
    escio.Write(fill + "\n" + fill)
    # backspace enough to go before both copies, if unconstrained
    escio.Write(esc.BS * (size.width() * 5))
    if escargs.args.xterm_reverse_wrap >= 383:
      AssertEQ(GetCursorPosition(), Point(1, 6))
    else:
      AssertEQ(GetCursorPosition(), Point(9, 3))

from esc import empty, TAB
import esccmd
import escio
from escutil import AssertEQ, AssertScreenCharsInRectEqual, GetCursorPosition, GetScreenSize, GetIconTitle, GetWindowTitle, knownBug, vtLevel
from esctypes import Point, Rect

class RISTests(object):
  @vtLevel(4)
  def test_RIS_ClearsScreen(self):
    escio.Write("x")

    esccmd.RIS()

    AssertScreenCharsInRectEqual(Rect(1, 1, 1, 1), [empty()])

  def test_RIS_CursorToOrigin(self):
    esccmd.CUP(Point(5, 6))

    esccmd.RIS()

    AssertEQ(GetCursorPosition(), Point(1, 1))

  def test_RIS_ResetTabs(self):
    esccmd.HTS()
    esccmd.CUF()
    esccmd.HTS()
    esccmd.CUF()
    esccmd.HTS()

    esccmd.RIS()

    escio.Write(TAB)
    AssertEQ(GetCursorPosition(), Point(9, 1))

  @knownBug(terminal="iTerm2", reason="RM_Title and SM_Title not implemented.")
  def test_RIS_ResetTitleMode(self):
    esccmd.RM_Title(esccmd.SET_UTF8, esccmd.QUERY_UTF8)
    esccmd.SM_Title(esccmd.SET_HEX, esccmd.QUERY_HEX)

    esccmd.RIS()

    esccmd.ChangeWindowTitle("ab")
    AssertEQ(GetWindowTitle(), "ab")
    esccmd.ChangeWindowTitle("a")
    AssertEQ(GetWindowTitle(), "a")

    esccmd.ChangeIconTitle("ab")
    AssertEQ(GetIconTitle(), "ab")
    esccmd.ChangeIconTitle("a")
    AssertEQ(GetIconTitle(), "a")

  @vtLevel(4)
  def test_RIS_ExitAltScreen(self):
    escio.Write("m")
    esccmd.DECSET(esccmd.ALTBUF)
    esccmd.CUP(Point(1, 1))
    escio.Write("a")

    esccmd.RIS()

    AssertScreenCharsInRectEqual(Rect(1, 1, 1, 1), [empty()])
    esccmd.DECSET(esccmd.ALTBUF)
    AssertScreenCharsInRectEqual(Rect(1, 1, 1, 1), ["a"])

  def test_RIS_ResetDECCOLM(self):
    """Test whether RIS resets DECCOLM.

    The control sequence allowing 80/132 switching is an xterm feature
    not found in DEC terminals.  When doing a full reset, xterm checks
    that, as well as checking if the terminal is currently in 132-column
    mode.  Older versions of xterm would reset the 132-column mode
    before checking if it was enabled, failing this test."""
    esccmd.DECSET(esccmd.Allow80To132)
    esccmd.DECSET(esccmd.DECCOLM)
    AssertEQ(GetScreenSize().width(), 132)

    esccmd.RIS()

    AssertEQ(GetScreenSize().width(), 80)

  @vtLevel(4)
  def test_RIS_ResetDECOM(self):
    esccmd.DECSTBM(5, 7)
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(5, 7)
    esccmd.DECSET(esccmd.DECOM)
    esccmd.RIS()
    esccmd.CUP(Point(1, 1))
    escio.Write("X")

    esccmd.DECRESET(esccmd.DECLRMM)
    esccmd.DECSTBM()

    AssertScreenCharsInRectEqual(Rect(1, 1, 1, 1), ["X"])

  @vtLevel(4)
  def test_RIS_RemoveMargins(self):
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(3, 5)
    esccmd.DECSTBM(4, 6)

    esccmd.RIS()

    esccmd.CUP(Point(3, 4))
    esccmd.CUB()
    AssertEQ(GetCursorPosition(), Point(2, 4))
    esccmd.CUU()
    AssertEQ(GetCursorPosition(), Point(2, 3))

    esccmd.CUP(Point(5, 6))
    esccmd.CUF()
    AssertEQ(GetCursorPosition(), Point(6, 6))
    esccmd.CUD()
    AssertEQ(GetCursorPosition(), Point(6, 7))

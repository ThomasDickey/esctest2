from esc import empty, TAB

import esccmd
import escio

from escutil import AssertEQ
from escutil import AssertScreenCharsInRectEqual
from escutil import GetCursorPosition
from escutil import GetScreenSize
from escutil import GetIconTitle
from escutil import GetWindowTitle
from escutil import knownBug
from escutil import vtLevel

from esctypes import Point, Rect

class RISTests(object):

  @classmethod
  @vtLevel(4)
  def test_RIS_ClearsScreen(cls):
    escio.Write("x")

    esccmd.RIS()

    AssertScreenCharsInRectEqual(Rect(1, 1, 1, 1), [empty()])

  @classmethod
  def test_RIS_CursorToOrigin(cls):
    esccmd.CUP(Point(5, 6))

    esccmd.RIS()

    AssertEQ(GetCursorPosition(), Point(1, 1))

  @classmethod
  def test_RIS_ResetTabs(cls):
    esccmd.HTS()
    esccmd.CUF()
    esccmd.HTS()
    esccmd.CUF()
    esccmd.HTS()

    esccmd.RIS()

    escio.Write(TAB)
    AssertEQ(GetCursorPosition(), Point(9, 1))

  @classmethod
  def test_RIS_ResetTitleMode(cls):
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

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Matches older xterm behavior.")
  @knownBug(terminal="iTerm2beta", reason="Matches older xterm behavior.")
  def test_RIS_ExitAltScreen(cls):
    escio.Write("m")
    esccmd.DECSET(esccmd.ALTBUF)
    esccmd.CUP(Point(1, 1))
    escio.Write("a")

    esccmd.RIS()

    AssertScreenCharsInRectEqual(Rect(1, 1, 1, 1), [empty()])
    esccmd.DECSET(esccmd.ALTBUF)
    AssertScreenCharsInRectEqual(Rect(1, 1, 1, 1), [empty()])

  @classmethod
  def test_RIS_ResetDECCOLM(cls):
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

  @classmethod
  @vtLevel(4)
  def test_RIS_ResetDECOM(cls):
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

  @classmethod
  @vtLevel(4)
  def test_RIS_RemoveMargins(cls):
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

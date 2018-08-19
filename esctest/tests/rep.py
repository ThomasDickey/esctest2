"""Tests for REP (repeat).

DEC STD 070 does not mention this feature.  It is adapted from ECMA-48,
which in turn does not mention margins, by xterm, to follow the DEC standard
which limits editing and cursor movement using top/bottom and left/right
margins.  Top/bottom margins are a VT100 feature; left/right margins were
introduced with the VT420.
"""
from esc import empty
import esccmd
import escio
from escutil import AssertScreenCharsInRectEqual, GetScreenSize, knownBug, vtLevel
from esctypes import Point, Rect

class REPTests(object):
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_REP_DefaultParam(self):
    escio.Write("a")
    esccmd.REP()
    AssertScreenCharsInRectEqual(Rect(1, 1, 3, 1), ["aa" + empty()])

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_REP_ExplicitParam(self):
    escio.Write("a")
    esccmd.REP(2)
    AssertScreenCharsInRectEqual(Rect(1, 1, 4, 1), ["aaa" + empty()])

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_REP_RespectsLeftRightMargins(self):
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(2, 4)
    esccmd.CUP(Point(2, 1))
    escio.Write("a")
    esccmd.REP(3)
    esccmd.DECRESET(esccmd.DECLRMM)

    AssertScreenCharsInRectEqual(Rect(1, 1, 5, 2),
                                 [empty() + "aaa" + empty(),
                                  empty() + "a" + empty() * 3])

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_REP_RespectsTopBottomMargins(self):
    width = GetScreenSize().width()
    esccmd.DECSTBM(2, 4)
    esccmd.CUP(Point(width - 2, 4))
    escio.Write("a")
    esccmd.REP(3)

    AssertScreenCharsInRectEqual(Rect(1, 3, width, 4),
                                 [empty() * (width - 3) + "aaa",
                                  "a" + empty() * (width - 1)])

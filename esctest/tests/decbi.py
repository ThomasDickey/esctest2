from esc import blank
import esccmd
import escio
from escutil import AssertEQ
from escutil import AssertScreenCharsInRectEqual
from escutil import GetCursorPosition
from escutil import Point
from escutil import Rect
from escutil import knownBug
from escutil import vtLevel

class DECBITests(object):
  """Move cursor back or scroll data within margins right."""

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  def test_DECBI_Basic(cls):
    esccmd.CUP(Point(5, 6))
    esccmd.DECBI()
    AssertEQ(GetCursorPosition(), Point(4, 6))

  @classmethod
  @vtLevel(4)
  def test_DECBI_NoWrapOnLeftEdge(cls):
    esccmd.CUP(Point(1, 2))
    esccmd.DECBI()
    AssertEQ(GetCursorPosition(), Point(1, 2))

  @classmethod
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  @vtLevel(4)
  def test_DECBI_Scrolls(cls):
    strings = ["abcde",
               "fghij",
               "klmno",
               "pqrst",
               "uvwxy"]
    y = 3
    for s in strings:
      esccmd.CUP(Point(2, y))
      escio.Write(s)
      y += 1

    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(3, 5)
    esccmd.DECSTBM(4, 6)

    esccmd.CUP(Point(3, 5))
    esccmd.DECBI()

    AssertScreenCharsInRectEqual(Rect(2, 3, 6, 7),
                                 ["abcde",
                                  "f" + blank() + "ghj",
                                  "k" + blank() + "lmo",
                                  "p" + blank() + "qrt",
                                  "uvwxy"])

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  def test_DECBI_LeftOfMargin(cls):
    """Test DECBI (back-index) when the cursor is before the left-margin.

    DEC STD 070 says DECBI can move when outside the margins."""
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(3, 5)
    esccmd.CUP(Point(2, 1))
    esccmd.DECBI()
    AssertEQ(GetCursorPosition(), Point(1, 1))

  @classmethod
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  @vtLevel(4)
  def test_DECBI_WholeScreenScrolls(cls):
    """Test DECBI (back-index) when the cursor is before the left-margin, but
    at the left edge of the screen.

    Refer to DEC STD 070, which says if the cursor is outside the margins,
    at the left edge of the page (which xterm equates with its screen),
    the command is ignored."""
    escio.Write("x")
    esccmd.CUP(Point(1, 1))
    esccmd.DECBI()
    AssertScreenCharsInRectEqual(Rect(1, 1, 2, 1), [blank() + "x"])

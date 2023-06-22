"""Tests for DECFI (forward-index).

Quoting from DEC STD 070 (Page 5-37 29-Jun-1990):

FORWARD INDEX
Levels:  4x (Horizontal Scrolling) DECFI
Purpose: Move the Active Position forward one column, scrolling if necessary.
Format:  ESC  9
         1/11 3/9

Description:  The DECFI control causes the active position to move forward one
column.  If the active position was already at the right margin, the contents
of the Logical Display Page within the right, left, top and bottom margins
shifts left one column.  The column shifting beyond the left margin is deleted.
A new column is inserted at the right margin with all attributes turned off and
the cursor appears in this column.

If the active position is outside the left or right margin when the command is
received the active position moves forward one column.  If the active position
was at the right edge of the page, the command is ignored.
"""
from esc import empty
import esccmd
import escio
from escutil import AssertEQ
from escutil import AssertScreenCharsInRectEqual
from escutil import GetCursorPosition
from escutil import GetScreenSize
from escutil import Point
from escutil import Rect
from escutil import knownBug
from escutil import vtLevel

class DECFITests(object):
  """Move cursor forward or scroll data within margins right."""

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  def test_DECFI_Basic(cls):
    esccmd.CUP(Point(5, 6))
    esccmd.DECFI()
    AssertEQ(GetCursorPosition(), Point(6, 6))

  @classmethod
  @vtLevel(4)
  def test_DECFI_NoWrapOnRightEdge(cls):
    size = GetScreenSize()
    esccmd.CUP(Point(size.width(), 2))
    esccmd.DECFI()
    AssertEQ(GetCursorPosition(), Point(size.width(), 2))

  @classmethod
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  @vtLevel(4)
  def test_DECFI_Scrolls(cls):
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

    esccmd.CUP(Point(5, 5))
    esccmd.DECFI()

    AssertScreenCharsInRectEqual(Rect(2, 3, 6, 7),
                                 ["abcde",
                                  "fhi" + empty() + "j",
                                  "kmn" + empty() + "o",
                                  "prs" + empty() + "t",
                                  "uvwxy"])

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  def test_DECFI_RightOfMargin(cls):
    """DEC STD 070 says DECFI can move when outside the margins."""
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(3, 5)
    esccmd.CUP(Point(6, 1))
    esccmd.DECFI()
    AssertEQ(GetCursorPosition(), Point(7, 1))

  @classmethod
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  @vtLevel(4)
  def test_DECFI_WholeScreenScrolls(cls):
    """Starting with the cursor at the right edge of the page (outside the
    margins), verify that DECFI is ignored."""
    size = GetScreenSize()
    esccmd.CUP(Point(size.width(), 1))
    escio.Write("x")
    esccmd.DECFI()
    AssertScreenCharsInRectEqual(Rect(size.width() - 1, 1, size.width(), 1),
                                 ["x" + empty()])

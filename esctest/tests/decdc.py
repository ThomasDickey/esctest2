"""Tests for DEC DELETE COLUMN (DECDC).

Quoting DEC STD 070:
DELETE COLUMN
Level:   4x (Horizontal Scrolling)
Purpose: Delete columns at the Active Position
Format:  CSI   Pn  '    ~        default Pn: 1
         9/11  Pn  2/7  7/14
Description:  The DECDC control causes Pn columns to be deleted at the active
column position.  The contents of the display are shifted to the left from
the right margin to the active column.  Columns containing blank characters
with normal rendition are shifted into the display from the right margin.
Only that portion of the display between the top, bottom, left, and right
margins is affected.  DECDC is ignored if the active position is outside the
Scroll Area.
"""
from esc import empty, CR, LF
import esccmd
import escio
from escutil import AssertEQ
from escutil import GetCursorPosition
from escutil import GetScreenSize
from escutil import AssertScreenCharsInRectEqual
from escutil import knownBug
from escutil import vtLevel
from esctypes import Point, Rect

class DECDCTests(object):

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_DECDC_DefaultParam(cls):
    """Test DECDC with default parameter """
    esccmd.CUP(Point(1, 1))
    AssertEQ(GetCursorPosition().x(), 1)
    escio.Write("abcdefg" + CR + LF + "ABCDEFG")
    esccmd.CUP(Point(2, 1))
    AssertEQ(GetCursorPosition().x(), 2)
    esccmd.DECDC()

    AssertScreenCharsInRectEqual(Rect(1, 1, 7, 2),
                                 ["acdefg" + empty(),
                                  "ACDEFG" + empty()])

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_DECDC_ExplicitParam(cls):
    """Test DECDC with explicit parameter. Also verifies lines above and below
    the cursor are affected."""
    esccmd.CUP(Point(1, 1))
    AssertEQ(GetCursorPosition().x(), 1)
    escio.Write("abcdefg" + CR + LF + "ABCDEFG" + CR + LF + "zyxwvut")
    esccmd.CUP(Point(2, 2))
    AssertEQ(GetCursorPosition().x(), 2)
    esccmd.DECDC(2)

    AssertScreenCharsInRectEqual(Rect(1, 1, 7, 3),
                                 ["adefg" + empty() * 2,
                                  "ADEFG" + empty() * 2,
                                  "zwvut" + empty() * 2])

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_DECDC_CursorWithinTopBottom(cls):
    """DECDC should only affect rows inside region."""
    esccmd.DECSTBM()
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(1, 20)
    # Write four lines. The middle two will be in the scroll region.
    esccmd.CUP(Point(1, 1))
    escio.Write("abcdefg" + CR + LF +
                "ABCDEFG" + CR + LF +
                "zyxwvut" + CR + LF +
                "ZYXWVUT")
    # Define a scroll region. Place the cursor in it. Insert a column.
    esccmd.DECSTBM(2, 3)
    esccmd.CUP(Point(2, 2))
    esccmd.DECDC(2)

    # Remove scroll region and see if it worked.
    esccmd.DECSTBM()
    esccmd.DECRESET(esccmd.DECLRMM)
    AssertScreenCharsInRectEqual(Rect(1, 1, 7, 4),
                                 ["abcdefg",
                                  "ADEFG" + empty() * 2,
                                  "zwvut" + empty() * 2,
                                  "ZYXWVUT"])

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented", noop=True)
  def test_DECDC_IsNoOpWhenCursorBeginsOutsideScrollRegion(cls):
    """Ensure DECDC does nothing when the cursor starts out outside the scroll
    region.

    DEC STD 070 is explicit on this, saying:
    DECDC is ignored if the active position is outside the Scroll Area.
    """
    esccmd.CUP(Point(1, 1))
    escio.Write("abcdefg" + CR + LF + "ABCDEFG")

    # Set margin: from columns 2 to 5
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(2, 5)

    # Position cursor outside margins
    esccmd.CUP(Point(1, 1))

    # Insert blanks
    esccmd.DECDC(10)

    # Ensure nothing happened.
    esccmd.DECRESET(esccmd.DECLRMM)
    AssertScreenCharsInRectEqual(Rect(1, 1, 7, 2),
                                 ["abcdefg",
                                  "ABCDEFG"])

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_DECDC_DeleteAll(cls):
    """Test DECDC behavior when deleting more columns than are available."""
    width = GetScreenSize().width()
    s = "abcdefg"
    startX = width - len(s) + 1
    esccmd.CUP(Point(startX, 1))
    escio.Write(s)
    esccmd.CUP(Point(startX, 2))
    escio.Write(s.upper())
    esccmd.CUP(Point(startX + 1, 1))
    esccmd.DECDC(width + 10)

    AssertScreenCharsInRectEqual(Rect(startX, 1, width, 2),
                                 ["a" + empty() * 6,
                                  "A" + empty() * 6])
    # Ensure there is no wrap-around.
    AssertScreenCharsInRectEqual(Rect(1, 2, 1, 3), [empty(), empty()])

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_DECDC_DeleteWithLeftRightMargins(cls):
    """Test DECDC when cursor is within the scroll region."""
    esccmd.CUP(Point(1, 1))
    s = "abcdefg"
    escio.Write(s)
    esccmd.CUP(Point(1, 2))
    escio.Write(s.upper())

    # Set margin: from columns 2 to 5
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(2, 5)

    # Position cursor inside margins
    esccmd.CUP(Point(3, 1))

    # Insert blank
    esccmd.DECDC()

    # Ensure the 'e' gets dropped.
    esccmd.DECRESET(esccmd.DECLRMM)
    AssertScreenCharsInRectEqual(Rect(1, 1, 7, 2),
                                 ["abde" + empty() + "fg",
                                  "ABDE" + empty() + "FG"])


  @classmethod
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_DECDC_DeleteAllWithLeftRightMargins(cls):
    """Test DECDC when cursor is within the scroll region."""
    esccmd.CUP(Point(1, 1))
    s = "abcdefg"
    escio.Write(s)
    esccmd.CUP(Point(1, 2))
    escio.Write(s.upper())

    # Set margin: from columns 2 to 5
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(2, 5)

    # Position cursor inside margins
    esccmd.CUP(Point(3, 1))

    # Insert blank
    esccmd.DECDC(99)

    esccmd.DECRESET(esccmd.DECLRMM)
    AssertScreenCharsInRectEqual(Rect(1, 1, 7, 2),
                                 ["ab" + empty() * 3 + "fg",
                                  "AB" + empty() * 3 + "FG"])

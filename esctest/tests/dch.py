from esc import empty
import esccmd
import escio
from esctypes import Point, Rect
from escutil import AssertScreenCharsInRectEqual, vtLevel

class DCHTests(object):

  @classmethod
  @vtLevel(4)
  def test_DCH_DefaultParam(cls):
    """DCH with no parameter should delete one character at the cursor."""
    escio.Write("abcd")
    esccmd.CUP(Point(2, 1))
    esccmd.DCH()
    AssertScreenCharsInRectEqual(Rect(1, 1, 4, 1), ["acd" + empty()])

  @classmethod
  @vtLevel(4)
  def test_DCH_ExplicitParam(cls):
    """DCH deletes the specified number of parameters."""
    escio.Write("abcd")
    esccmd.CUP(Point(2, 1))
    esccmd.DCH(2)
    AssertScreenCharsInRectEqual(Rect(1, 1, 4, 1), ["ad" + empty() * 2])

  @classmethod
  @vtLevel(4)
  def test_DCH_RespectsMargins(cls):
    """DCH respects left-right margins."""
    escio.Write("abcde")
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(2, 4)
    esccmd.CUP(Point(3, 1))
    esccmd.DCH()
    esccmd.DECRESET(esccmd.DECLRMM)

    AssertScreenCharsInRectEqual(Rect(1, 1, 5, 1), ["abd" + empty() + "e"])

  @classmethod
  @vtLevel(4)
  def test_DCH_DeleteAllWithMargins(cls):
    """Delete all characters up to right margin."""
    escio.Write("abcde")
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(2, 4)
    esccmd.CUP(Point(3, 1))
    esccmd.DCH(99)
    esccmd.DECRESET(esccmd.DECLRMM)

    AssertScreenCharsInRectEqual(Rect(1, 1, 5, 1), ["ab" + empty() * 2 + "e"])

  @classmethod
  @vtLevel(4)
  def test_DCH_DoesNothingOutsideLeftRightMargin(cls):
    """DCH should do nothing outside left-right margins."""
    escio.Write("abcde")
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(2, 4)
    esccmd.CUP(Point(1, 1))
    esccmd.DCH(99)
    esccmd.DECRESET(esccmd.DECLRMM)

    AssertScreenCharsInRectEqual(Rect(1, 1, 5, 1), ["abcde"])

  @classmethod
  @vtLevel(4)
  def test_DCH_WorksOutsideTopBottomMargin(cls):
    """Per Thomas Dickey, DCH should work outside scrolling margin (see xterm
    changelog for patch 316)."""
    escio.Write("abcde")
    esccmd.DECSTBM(2, 3)
    esccmd.CUP(Point(1, 1))
    esccmd.DCH(99)
    esccmd.DECSTBM()

    AssertScreenCharsInRectEqual(Rect(1, 1, 5, 1), [empty() * 5])

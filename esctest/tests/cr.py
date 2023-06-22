import esc
import esccmd
import escio
from escutil import AssertEQ, AssertScreenCharsInRectEqual, GetCursorPosition, vtLevel
from esctypes import Point, Rect

class CRTests(object):

  @classmethod
  def test_CR_Basic(cls):
    esccmd.CUP(Point(3, 3))
    escio.Write(esc.CR)
    AssertEQ(GetCursorPosition(), Point(1, 3))

  @classmethod
  @vtLevel(4)
  def test_CR_MovesToLeftMarginWhenRightOfLeftMargin(cls):
    """Move the cursor to the left margin if it starts right of it."""
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(5, 10)
    esccmd.CUP(Point(6, 1))
    escio.Write(esc.CR)
    esccmd.DECRESET(esccmd.DECLRMM)
    AssertEQ(GetCursorPosition(), Point(5, 1))

  @classmethod
  @vtLevel(4)
  def test_CR_MovesToLeftOfScreenWhenLeftOfLeftMargin(cls):
    """Move the cursor to the left edge of the screen when it starts of left the margin."""
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(5, 10)
    esccmd.CUP(Point(4, 1))
    escio.Write(esc.CR)
    esccmd.DECRESET(esccmd.DECLRMM)
    AssertEQ(GetCursorPosition(), Point(1, 1))

  @classmethod
  @vtLevel(4)
  def test_CR_StaysPutWhenAtLeftMargin(cls):
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(5, 10)
    esccmd.CUP(Point(5, 1))
    escio.Write(esc.CR)
    esccmd.DECRESET(esccmd.DECLRMM)
    AssertEQ(GetCursorPosition(), Point(5, 1))

  @classmethod
  @vtLevel(4)
  def test_CR_MovesToLeftMarginWhenLeftOfLeftMarginInOriginMode(cls):
    """In origin mode, always go to the left margin, even if the cursor starts left of it."""
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(5, 10)
    esccmd.DECSET(esccmd.DECOM)
    esccmd.CUP(Point(4, 1))
    escio.Write(esc.CR)
    esccmd.DECRESET(esccmd.DECLRMM)
    escio.Write("x")
    esccmd.DECRESET(esccmd.DECOM)
    AssertScreenCharsInRectEqual(Rect(5, 1, 5, 1), ["x"])

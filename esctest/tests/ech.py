from esc import blank
import esccmd
import escio
from esctypes import Point, Rect
from escutil import AssertScreenCharsInRectEqual, knownBug, vtLevel

class ECHTests(object):
  @vtLevel(4)
  def test_ECH_DefaultParam(self):
    """Should erase the character under the cursor."""
    escio.Write("abc")
    esccmd.CUP(Point(1, 1))
    esccmd.ECH()
    AssertScreenCharsInRectEqual(Rect(1, 1, 3, 1), [blank() + "bc"])

  @vtLevel(4)
  def test_ECH_ExplicitParam(self):
    """Should erase N characters starting at the cursor."""
    escio.Write("abc")
    esccmd.CUP(Point(1, 1))
    esccmd.ECH(2)
    AssertScreenCharsInRectEqual(Rect(1, 1, 3, 1), [blank() * 2 + "c"])

  @vtLevel(4)
  def test_ECH_IgnoresScrollRegion(self):
    """ECH ignores the scroll region when the cursor is inside it"""
    escio.Write("abcdefg")
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(2, 4)
    esccmd.CUP(Point(3, 1))
    esccmd.ECH(4)
    esccmd.DECRESET(esccmd.DECLRMM)

    AssertScreenCharsInRectEqual(Rect(1, 1, 7, 1), ["ab" + blank() * 4 + "g"])

  @vtLevel(4)
  def test_ECH_OutsideScrollRegion(self):
    """ECH ignores the scroll region when the cursor is outside it"""
    escio.Write("abcdefg")
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(2, 4)
    esccmd.CUP(Point(1, 1))
    esccmd.ECH(4)
    esccmd.DECRESET(esccmd.DECLRMM)

    AssertScreenCharsInRectEqual(Rect(1, 1, 7, 1), [blank() * 4 + "efg"])

  @vtLevel(4)
  def test_ECH_doesNotRespectDECPRotection(self):
    """ECH should not respect DECSCA."""
    escio.Write("a")
    escio.Write("b")
    esccmd.DECSCA(1)
    escio.Write("c")
    esccmd.DECSCA(0)
    esccmd.CUP(Point(1, 1))
    esccmd.ECH(3)
    AssertScreenCharsInRectEqual(Rect(1, 1, 3, 1),
                                 [blank() * 3])

  @vtLevel(4)
  @knownBug(terminal="iTerm2",
            reason="Protection not implemented.")
  def test_ECH_respectsISOProtection(self):
    """ECH respects SPA/EPA."""
    escio.Write("a")
    escio.Write("b")
    esccmd.SPA()
    escio.Write("c")
    esccmd.EPA()
    esccmd.CUP(Point(1, 1))
    esccmd.ECH(3)
    AssertScreenCharsInRectEqual(Rect(1, 1, 3, 1),
                                 [blank() * 2 + "c"])


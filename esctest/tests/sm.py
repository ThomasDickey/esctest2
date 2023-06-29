from esc import empty, LF, VT, FF
import esccmd
import escio
from escutil import AssertEQ
from escutil import AssertScreenCharsInRectEqual
from escutil import GetCursorPosition
from escutil import GetScreenSize
from escutil import knownBug
from escutil import vtLevel
from esctypes import Point, Rect

# AM, SRM, and LNM should also be supported but are not currently testable
# because they require user interaction.
class SMTests(object):

  @classmethod
  @vtLevel(4)
  def test_SM_IRM(cls):
    """Turn on insert mode."""
    escio.Write("abc")
    esccmd.CUP(Point(1, 1))
    esccmd.SM(esccmd.IRM)
    escio.Write("X")
    AssertScreenCharsInRectEqual(Rect(1, 1, 4, 1), ["Xabc"])

  @classmethod
  @vtLevel(4)
  def test_SM_IRM_DoesNotWrapUnlessCursorAtMargin(cls):
    """Insert mode does not cause wrapping."""
    size = GetScreenSize()
    escio.Write("a" * (size.width() - 1))
    escio.Write("b")
    esccmd.CUP(Point(1, 1))
    esccmd.SM(esccmd.IRM)
    AssertScreenCharsInRectEqual(Rect(1, 2, 1, 2), [empty()])
    escio.Write("X")
    AssertScreenCharsInRectEqual(Rect(1, 2, 1, 2), [empty()])
    esccmd.CUP(Point(size.width(), 1))
    escio.Write("YZ")
    AssertScreenCharsInRectEqual(Rect(1, 2, 1, 2), ["Z"])

  @classmethod
  @vtLevel(4)
  def test_SM_IRM_TruncatesAtRightMargin(cls):
    """When a left-right margin is set, insert truncates the line at the right margin."""
    esccmd.CUP(Point(5, 1))

    escio.Write("abcdef")

    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(5, 10)

    esccmd.CUP(Point(7, 1))
    esccmd.SM(esccmd.IRM)
    escio.Write("X")
    esccmd.DECRESET(esccmd.DECLRMM)

    AssertScreenCharsInRectEqual(Rect(5, 1, 11, 1), ["abXcde" + empty()])

  @classmethod
  def doLinefeedModeTest(cls, code):
    esccmd.RM(esccmd.LNM)
    esccmd.CUP(Point(5, 1))
    escio.Write(code)
    AssertEQ(GetCursorPosition(), Point(5, 2))

    esccmd.SM(esccmd.LNM)
    esccmd.CUP(Point(5, 1))
    escio.Write(code)
    AssertEQ(GetCursorPosition(), Point(1, 2))

  @knownBug(terminal="iTerm2", reason="LNN not implemented.")
  @knownBug(terminal="iTerm2beta", reason="LNN not implemented.")
  def test_SM_LNM(self):
    """In linefeed mode LF, VT, and FF perform a carriage return after doing
    an index. Also any report with a CR gets a CR LF instead, but I'm not sure
    when that would happen."""
    self.doLinefeedModeTest(LF)
    self.doLinefeedModeTest(VT)
    self.doLinefeedModeTest(FF)

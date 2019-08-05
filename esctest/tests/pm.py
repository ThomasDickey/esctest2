from esc import empty, ST, S7C1T, S8C1T
import escargs
import esccmd
import escio
from escutil import AssertScreenCharsInRectEqual, knownBug, optionRequired, vtLevel
from esctypes import Rect

class PMTests(object):
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  def test_PM_Basic(self):
    esccmd.PM()
    escio.Write("xyz")
    escio.Write(ST)
    escio.Write("A")

    AssertScreenCharsInRectEqual(Rect(1, 1, 3, 1),
                                 ["A" + empty() * 2])

  @vtLevel(4)
  @optionRequired(terminal="xterm", option=escargs.DISABLE_WIDE_CHARS)
  @knownBug(terminal="iTerm2", reason="PM not implemented.")
  def test_PM_8bit(self):
    escio.use8BitControls = True
    escio.Write(S8C1T)
    esccmd.PM()
    escio.Write("xyz")
    escio.Write(ST)
    escio.Write("A")
    escio.Write(S7C1T)
    escio.use8BitControls = False

    AssertScreenCharsInRectEqual(Rect(1, 1, 3, 1),
                                 ["A" + empty() * 2])

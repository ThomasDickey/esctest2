from esc import empty, S7C1T, S8C1T
import escargs
import esccmd
import escio
from escutil import AssertScreenCharsInRectEqual, knownBug, optionRequired, vtLevel
from esctypes import Rect

class PMTests(object):

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  @knownBug(terminal="iTerm2beta", reason="Not implemented.")
  def test_PM_Basic(cls):
    esccmd.PM()
    escio.Write("xyz")
    esccmd.ST()
    escio.Write("A")

    AssertScreenCharsInRectEqual(Rect(1, 1, 3, 1),
                                 ["A" + empty() * 2])

  @classmethod
  @vtLevel(4)
  @optionRequired(terminal="xterm", option=escargs.DISABLE_WIDE_CHARS, allowPassWithoutOption=escargs.ALLOW_C2_CONTROLS)
  @knownBug(terminal="iTerm2", reason="PM not implemented.")
  @knownBug(terminal="iTerm2beta", reason="PM not implemented.")
  def test_PM_8bit(cls):
    escio.use8BitControls = True
    escio.Write(S8C1T)
    esccmd.PM()
    escio.Write("xyz")
    esccmd.ST()
    escio.Write("A")
    escio.Write(S7C1T)
    escio.use8BitControls = False

    AssertScreenCharsInRectEqual(Rect(1, 1, 3, 1),
                                 ["A" + empty() * 2])

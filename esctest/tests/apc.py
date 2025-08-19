from esc import empty, S7C1T, S8C1T
import escargs
import escio
from escutil import AssertScreenCharsInRectEqual, optionRequired, vtLevel
from esctypes import Rect

class APCTests(object):

  @classmethod
  @vtLevel(4)
  def test_APC_Basic(cls):
    escio.WriteAPC("xyz")
    escio.Write("A")

    AssertScreenCharsInRectEqual(Rect(1, 1, 3, 1),
                                 ["A" + empty() * 2])

  @classmethod
  @vtLevel(4)
  @optionRequired(terminal="xterm", option=escargs.DISABLE_WIDE_CHARS, allowPassWithoutOption=escargs.ALLOW_C2_CONTROLS)
  @optionRequired(terminal="iTerm2", option=escargs.DISABLE_WIDE_CHARS)
  @optionRequired(terminal="iTerm2beta", option=escargs.DISABLE_WIDE_CHARS)
  def test_APC_8bit(cls):
    escio.use8BitControls = True
    escio.Write(S8C1T)

    escio.WriteAPC("xyz")
    escio.Write("A")

    escio.Write(S7C1T)
    escio.use8BitControls = False

    AssertScreenCharsInRectEqual(Rect(1, 1, 3, 1),
                                 ["A" + empty() * 2])

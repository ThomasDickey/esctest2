from esc import S8C1T, S7C1T
import escargs
import esccmd
import escio
from escutil import AssertTrue, knownBug, optionRequired

class DECIDTests(object):

  @classmethod
  @knownBug(terminal="iTerm2", reason="Not implemented.", shouldTry=False)
  @knownBug(terminal="iTerm2beta", reason="Not implemented.", shouldTry=False)
  def test_DECID_Basic(cls):
    esccmd.DECID()
    params = escio.ReadCSI("c", expected_prefix="?")
    AssertTrue(len(params) > 0)

  @classmethod
  @optionRequired(terminal="xterm", option=escargs.DISABLE_WIDE_CHARS, allowPassWithoutOption=escargs.ALLOW_C2_CONTROLS)
  @knownBug(terminal="iTerm2", reason="DECID not implemented.")
  @knownBug(terminal="iTerm2beta", reason="DECID not implemented.")
  def test_DECID_8bit(cls):
    escio.use8BitControls = True
    escio.Write(S8C1T)

    esccmd.DECID()
    params = escio.ReadCSI("c", expected_prefix="?")
    AssertTrue(len(params) > 0)

    escio.Write(S7C1T)
    escio.use8BitControls = False

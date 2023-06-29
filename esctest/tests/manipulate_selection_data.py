import base64
import escargs
import esccmd
import escio
from escutil import AssertEQ, knownBug, optionRequired
import escoding

class ManipulateSelectionDataTests(object):
  """No tests for buffers besides default; they're so x-specific that they're
  not worth testing for my purposes."""

  @classmethod
  @optionRequired(terminal="xterm", option=escargs.XTERM_WINOPS_ENABLED)
  @knownBug(terminal="iTerm2", reason="'OSC 52 ; ?' (query) not supported")
  @knownBug(terminal="iTerm2beta", reason="'OSC 52 ; ?' (query) not supported")
  def test_ManipulateSelectionData_default(cls):
    s = escoding.to_binary("testing 123")
    esccmd.ManipulateSelectionData(Pd=base64.b64encode(s))
    esccmd.ManipulateSelectionData(Pd="?")
    r = escio.ReadOSC("52")
    AssertEQ(r, ";s0;" + escoding.to_string(base64.b64encode(s)))

import esccmd
import escio
from escutil import AssertEQ, knownBug

class ResetColorTests(object):

  @classmethod
  @knownBug(terminal="iTerm2", reason="Query not implemented.")
  def test_ResetColor_Standard(cls):
    n = "0"
    esccmd.ChangeColor(n, "?")
    original = escio.ReadOSC("4")

    esccmd.ChangeColor(n, "#aaaabbbbcccc")
    esccmd.ChangeColor(n, "?")
    AssertEQ(escio.ReadOSC("4"), ";" + n + ";rgb:aaaa/bbbb/cccc")

    esccmd.ResetColor(n)
    esccmd.ChangeColor(n, "?")
    AssertEQ(escio.ReadOSC("4"), original)

  @classmethod
  @knownBug(terminal="iTerm2", reason="Query not implemented.")
  def test_ResetColor_All(cls):
    esccmd.ChangeColor("3", "?")
    original = escio.ReadOSC("4")

    esccmd.ChangeColor("3", "#aabbcc")
    esccmd.ChangeColor("3", "?")
    AssertEQ(escio.ReadOSC("4"), ";3;rgb:aaaa/bbbb/cccc")

    esccmd.ResetColor()
    esccmd.ChangeColor("3", "?")
    AssertEQ(escio.ReadOSC("4"), original)

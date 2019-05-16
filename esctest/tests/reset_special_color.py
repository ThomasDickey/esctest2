import esccmd
import escio
from escutil import AssertEQ, knownBug

class ResetSpecialColorTests(object):
  @knownBug(terminal="iTerm2", reason="Query not implemented.")
  def test_ResetSpecialColor_Single(self):
    n = "0"
    esccmd.ChangeSpecialColor(n, "?")
    original = escio.ReadOSC("5")

    esccmd.ChangeSpecialColor(n, "#aaaabbbbcccc")
    esccmd.ChangeSpecialColor(n, "?")
    AssertEQ(escio.ReadOSC("5"), ";" + str(int(n)) + ";rgb:aaaa/bbbb/cccc")

    esccmd.ResetSpecialColor(n)
    esccmd.ChangeSpecialColor(n, "?")
    AssertEQ(escio.ReadOSC("5"), original)

  @knownBug(terminal="iTerm2", reason="Query not implemented.")
  def test_ResetSpecialColor_Multiple(self):
    n1 = "0"
    n2 = "1"
    esccmd.ChangeSpecialColor(n1, "?", n2, "?")
    original1 = escio.ReadOSC("5")
    original2 = escio.ReadOSC("5")

    esccmd.ChangeSpecialColor(n1, "#aaaabbbbcccc")
    esccmd.ChangeSpecialColor(n2, "#ddddeeeeffff")
    esccmd.ChangeSpecialColor(n1, "?")
    AssertEQ(escio.ReadOSC("5"), ";" + str(int(n1)) + ";rgb:aaaa/bbbb/cccc")
    esccmd.ChangeSpecialColor(n2, "?")
    AssertEQ(escio.ReadOSC("5"), ";" + str(int(n2)) + ";rgb:dddd/eeee/ffff")

    esccmd.ResetSpecialColor(n1, n2)
    esccmd.ChangeSpecialColor(n1, "?", n2, "?")
    actual1 = escio.ReadOSC("5")
    actual2 = escio.ReadOSC("5")
    AssertEQ(actual1, original1)
    AssertEQ(actual2, original2)

  @knownBug(terminal="iTerm2", reason="Query not implemented.")
  def test_ResetSpecialColor_Dynamic(self):
    esccmd.ChangeSpecialColor("10", "?")
    original = escio.ReadOSC("10")

    esccmd.ChangeSpecialColor("10", "#aaaabbbbcccc")
    esccmd.ChangeSpecialColor("10", "?")
    AssertEQ(escio.ReadOSC("10"), ";rgb:aaaa/bbbb/cccc")

    esccmd.ResetDynamicColor("110")
    esccmd.ChangeSpecialColor("10", "?")
    AssertEQ(escio.ReadOSC("10"), original)


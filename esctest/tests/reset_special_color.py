import esccmd
import escio
from escutil import AssertEQ, knownBug
from escutil import GetIndexedColors

class ResetSpecialColorTests(object):

  @classmethod
  @knownBug(terminal="iTerm2", reason="Query not implemented.")
  @knownBug(terminal="iTerm2beta", reason="Query not implemented.")
  def test_ResetSpecialColor_Single(cls):
    offset = GetIndexedColors()
    n = "0"
    esccmd.ChangeSpecialColor(n, "?")
    original = escio.ReadOSC("4")

    esccmd.ChangeSpecialColor(n, "#aaaabbbbcccc")
    esccmd.ChangeSpecialColor(n, "?")
    AssertEQ(escio.ReadOSC("4"), ";" + str(int(n) + offset) + ";rgb:aaaa/bbbb/cccc")

    esccmd.ResetSpecialColor(n)
    esccmd.ChangeSpecialColor(n, "?")
    AssertEQ(escio.ReadOSC("4"), original)

  @classmethod
  @knownBug(terminal="iTerm2", reason="Query not implemented.")
  @knownBug(terminal="iTerm2beta", reason="Query not implemented.")
  def test_ResetSpecialColor_Single2(cls):
    n = "0"
    esccmd.ChangeSpecialColor2(n, "?")
    original = escio.ReadOSC("5")

    esccmd.ChangeSpecialColor2(n, "#aaaabbbbcccc")
    esccmd.ChangeSpecialColor2(n, "?")
    AssertEQ(escio.ReadOSC("5"), ";" + str(int(n)) + ";rgb:aaaa/bbbb/cccc")

    esccmd.ResetSpecialColor(n)
    esccmd.ChangeSpecialColor2(n, "?")
    AssertEQ(escio.ReadOSC("5"), original)

  @classmethod
  @knownBug(terminal="iTerm2", reason="Query not implemented.")
  @knownBug(terminal="iTerm2beta", reason="Query not implemented.")
  def test_ResetSpecialColor_Multiple(cls):
    offset = GetIndexedColors()
    n1 = "0"
    n2 = "1"
    esccmd.ChangeSpecialColor(n1, "?", n2, "?")
    original1 = escio.ReadOSC("4")
    original2 = escio.ReadOSC("4")

    esccmd.ChangeSpecialColor(n1, "#aaaabbbbcccc")
    esccmd.ChangeSpecialColor(n2, "#ddddeeeeffff")
    esccmd.ChangeSpecialColor(n1, "?")
    AssertEQ(escio.ReadOSC("4"), ";" + str(int(n1) + offset) + ";rgb:aaaa/bbbb/cccc")
    esccmd.ChangeSpecialColor(n2, "?")
    AssertEQ(escio.ReadOSC("4"), ";" + str(int(n2) + offset) + ";rgb:dddd/eeee/ffff")

    esccmd.ResetSpecialColor(n1, n2)
    esccmd.ChangeSpecialColor(n1, "?", n2, "?")
    actual1 = escio.ReadOSC("4")
    actual2 = escio.ReadOSC("4")
    AssertEQ(actual1, original1)
    AssertEQ(actual2, original2)

  @classmethod
  @knownBug(terminal="iTerm2", reason="Query not implemented.")
  @knownBug(terminal="iTerm2beta", reason="Query not implemented.")
  def test_ResetSpecialColor_Multiple2(cls):
    n1 = "0"
    n2 = "1"
    esccmd.ChangeSpecialColor2(n1, "?", n2, "?")
    original1 = escio.ReadOSC("5")
    original2 = escio.ReadOSC("5")

    esccmd.ChangeSpecialColor2(n1, "#aaaabbbbcccc")
    esccmd.ChangeSpecialColor2(n2, "#ddddeeeeffff")
    esccmd.ChangeSpecialColor2(n1, "?")
    AssertEQ(escio.ReadOSC("5"), ";" + str(int(n1)) + ";rgb:aaaa/bbbb/cccc")
    esccmd.ChangeSpecialColor2(n2, "?")
    AssertEQ(escio.ReadOSC("5"), ";" + str(int(n2)) + ";rgb:dddd/eeee/ffff")

    esccmd.ResetSpecialColor(n1, n2)
    esccmd.ChangeSpecialColor2(n1, "?", n2, "?")
    actual1 = escio.ReadOSC("5")
    actual2 = escio.ReadOSC("5")
    AssertEQ(actual1, original1)
    AssertEQ(actual2, original2)

  @classmethod
  @knownBug(terminal="iTerm2", reason="Query not implemented.")
  @knownBug(terminal="iTerm2beta", reason="Query not implemented.")
  def test_ResetSpecialColor_Dynamic(cls):
    esccmd.ChangeSpecialColor("10", "?")
    original = escio.ReadOSC("10")

    esccmd.ChangeSpecialColor("10", "#aaaabbbbcccc")
    esccmd.ChangeSpecialColor("10", "?")
    AssertEQ(escio.ReadOSC("10"), ";rgb:aaaa/bbbb/cccc")

    esccmd.ResetDynamicColor("110")
    esccmd.ChangeSpecialColor("10", "?")
    AssertEQ(escio.ReadOSC("10"), original)

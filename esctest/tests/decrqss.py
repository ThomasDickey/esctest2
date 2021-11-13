import escargs
import esccmd
import escio
from escutil import AssertEQ, knownBug, vtLevel

class DECRQSSTests(object):
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  def test_DECRQSS_DECSCA(self):
    esccmd.DECSCA(1)
    esccmd.DECRQSS('"q')
    result = escio.ReadDCS()
    AssertEQ(result, '1$r1"q')

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="VT400 not implemented yet (will report a lower value).")
  def test_DECRQSS_DECSCL(self):
    esccmd.DECSCL(65, 1)
    esccmd.DECRQSS('"p')
    result = escio.ReadDCS()
    AssertEQ(result, '1$r6' + str(escargs.args.max_vt_level) + ';1"p')

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  def test_DECRQSS_DECSTBM(self):
    esccmd.DECSTBM(5, 6)
    esccmd.DECRQSS("r")
    result = escio.ReadDCS()
    AssertEQ(result, "1$r5;6r")

  @vtLevel(4)
  def test_DECRQSS_SGR(self):
    esccmd.SGR(1)
    esccmd.DECRQSS("m")
    result = escio.ReadDCS()
    AssertEQ(result, "1$r0;1m")

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  def test_DECRQSS_DECSCUSR(self):
    esccmd.DECSCUSR(4)
    esccmd.DECRQSS(" q")
    result = escio.ReadDCS()
    AssertEQ(result, "1$r4 q")

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  def test_DECRQSS_DECSLRM(self):
    """Note: not in xcode docs, but supported."""
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(3, 4)
    esccmd.DECRQSS("s")
    result = escio.ReadDCS()
    AssertEQ(result, "1$r3;4s")

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  def test_DECRQSS_DECSLPP(self):
    esccmd.XTERM_WINOPS(27)
    esccmd.DECRQSS("t")
    result = escio.ReadDCS()
    AssertEQ(result, "1$r27t")

import escargs
import esccmd
import escio
from escutil import AssertEQ, knownBug, vtLevel

class DECRQSSTests(object):

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="xterm", reason="Not implemented.")
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  @knownBug(terminal="iTerm2beta", reason="Not implemented.")
  def test_DECRQSS_DECELF(cls):
    '''Report: Enable local functions'''
    esccmd.DECELF(0)
    esccmd.DECRQSS('+q')
    result = escio.ReadDCS()
    AssertEQ(result, '1$r0+q')

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="xterm", reason="Not implemented.")
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  @knownBug(terminal="iTerm2beta", reason="Not implemented.")
  def test_DECRQSS_DECLFKC(cls):
    '''Report: Enable local function key control'''
    esccmd.DECLFKC(0)
    esccmd.DECRQSS('*}')
    result = escio.ReadDCS()
    AssertEQ(result, '1$r0*}')

  @classmethod
  @vtLevel(3)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  @knownBug(terminal="iTerm2beta", reason="Not implemented.")
  def test_DECRQSS_DECSASD(cls):
    '''Report: Select active status display'''
    esccmd.DECSASD(0)
    esccmd.DECRQSS('$}')
    result = escio.ReadDCS()
    AssertEQ(result, '1$r0$}')

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  @knownBug(terminal="iTerm2beta", reason="Not implemented.")
  def test_DECRQSS_DECSACE(cls):
    '''Report: Select attribute change extent'''
    esccmd.DECSACE(0)
    esccmd.DECRQSS('*x')
    result = escio.ReadDCS()
    AssertEQ(result, '1$r0*x')

  @classmethod
  @vtLevel(2)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  def test_DECRQSS_DECSCA(cls):
    '''Report: Set character attribute'''
    esccmd.DECSCA(1)
    esccmd.DECRQSS('"q')
    result = escio.ReadDCS()
    AssertEQ(result, '1$r1"q')

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="VT400 not implemented yet (will report a lower value).")
  @knownBug(terminal="iTerm2beta", reason="VT400 not implemented yet (will report a lower value).")
  def test_DECRQSS_DECSCL(cls):
    '''Report: Set conformance level'''
    esccmd.DECSCL(65, 1)
    esccmd.DECRQSS('"p')
    result = escio.ReadDCS()
    AssertEQ(result, '1$r6' + str(escargs.args.max_vt_level) + ';1"p')

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  def test_DECRQSS_DECSTBM(cls):
    '''Report: Set top and bottom margins'''
    esccmd.DECSTBM(5, 6)
    esccmd.DECRQSS("r")
    result = escio.ReadDCS()
    AssertEQ(result, "1$r5;6r")

  @classmethod
  @vtLevel(4)
  def test_DECRQSS_SGR(cls):
    """Report: Select graphic rendition"""
    esccmd.SGR(1)
    esccmd.DECRQSS("m")
    result = escio.ReadDCS()
    AssertEQ(result, "1$r0;1m")

  @classmethod
  @vtLevel(4)
  def test_DECRQSS_DECSCUSR(cls):
    """Report: Set cursor style"""
    esccmd.DECSCUSR(4)
    esccmd.DECRQSS(" q")
    result = escio.ReadDCS()
    AssertEQ(result, "1$r4 q")

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  def test_DECRQSS_DECSLRM(cls):
    """Report: Set left and right margins"""
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(3, 4)
    esccmd.DECRQSS("s")
    result = escio.ReadDCS()
    AssertEQ(result, "1$r3;4s")

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  def test_DECRQSS_DECSLPP(cls):
    """Report: Set number of lines per page"""
    esccmd.XTERM_WINOPS(27)
    esccmd.DECRQSS("t")
    result = escio.ReadDCS()
    AssertEQ(result, "1$r27t")

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="xterm", reason="Not implemented.")
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  @knownBug(terminal="iTerm2beta", reason="Not implemented.")
  def test_DECRQSS_DECSMKR(cls):
    """Report: Set modifier key reporting"""
    esccmd.DECSMKR(0)
    esccmd.DECRQSS("+r")
    result = escio.ReadDCS()
    AssertEQ(result, "1$r0+r")

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  @knownBug(terminal="iTerm2beta", reason="Not implemented.")
  def test_DECRQSS_DECSNLS(cls):
    """Report: Set number of lines per screen"""
    esccmd.DECSNLS(24)
    esccmd.DECRQSS("*|")
    result = escio.ReadDCS()
    AssertEQ(result, "1$r24*|")

  @classmethod
  @vtLevel(3)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  @knownBug(terminal="iTerm2beta", reason="Not implemented.")
  def test_DECRQSS_DECSSDT(cls):
    """Report: Set status line type"""
    esccmd.DECSSDT(0)
    esccmd.DECRQSS("$~")
    result = escio.ReadDCS()
    AssertEQ(result, "1$r0$~")

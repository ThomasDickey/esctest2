import esccmd
import escio
from escutil import AssertEQ, AssertTrue, knownBug, vtLevel
from esctypes import Point

class DECDSRTests(object):

  @classmethod
  def getVTLevel(cls):
    esccmd.DA2()
    params = escio.ReadCSI('c', expected_prefix='>')
    myLevel = params[0]
    if myLevel <= 24:
      if myLevel < 18:
        return 2
      return 3
    return 4

  @vtLevel(3)
  @knownBug(terminal="iTerm2beta", reason="Page is omitted")
  def test_DECDSR_DECXCPR(self):
    """DECXCPR reports the cursor position. Response is:
    CSI ? Pl ; Pc ; Pr R
      Pl - line
      Pc - column
      Pr - page"""
    # First, get the VT level.
    myLevel = self.getVTLevel()

    esccmd.CUP(Point(5, 6))
    esccmd.DECDSR(esccmd.DECXCPR)
    params = escio.ReadCSI('R', expected_prefix='?')

    if myLevel >= 4:
      # VT400+
      # Last arg is page, which is always 1 (at least in xterm, and I think
      # that's reasonable in all modern terminals, which won't have a direct
      # notion of a page.)
      AssertEQ(params, [6, 5, 1])
    else:
      AssertEQ(params, [6, 5])

  @classmethod
  @vtLevel(2)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  def test_DECDSR_DSRPrinterPort(cls):
    """Requests printer status. The allowed responses are:
        CSI ? Pn n
      Where Pn is:
        10 - Ready
        11 - Not ready
        13 - No printer
        18 - Busy
        19 - Assigned to other session.
      There's no way for the test to know what the actual printer status is,
      but the response should be legal."""
    esccmd.DECDSR(esccmd.DSRPrinterPort)
    params = escio.ReadCSI('n', expected_prefix='?')
    AssertEQ(len(params), 1)
    AssertTrue(params[0] in [10, 11, 13, 18, 19])

  @classmethod
  @vtLevel(2)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  def test_DECDSR_DSRUDKLocked(cls):
    """Tests if user-defined keys are locked or unlocked. The allowed repsonses are:
      CSI ? Pn n
    Where Pn is:
      20 - Unlocked
      21 - Locked
    This test simply ensures the value is legal. It should be extended to
    ensure that when locked UDKs are not settable, and when unlocked that UDKs
    are settable."""
    esccmd.DECDSR(esccmd.DSRUDKLocked)
    params = escio.ReadCSI('n', expected_prefix='?')
    AssertEQ(len(params), 1)
    AssertTrue(params[0] in [20, 21])

  @vtLevel(2)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  @knownBug(terminal="iTerm2beta", reason="Not implemented.")
  def test_DECDSR_DSRKeyboard(self):
    """Gets info about the keyboard. The response is:
      CSI ? 27; Pn; Pst; Ptyp n
    Where
      Pn - Keyboard language
        0 - Not known
        1 - North American
        2...19, 22, 28, 29...31, 33, 35, 36, 38...40 - Various other legal values
      Pst - Keyboard status - Per the VT 510 manual, this is level 4 only.
            However, it is documented in "VT330/VT340 Programmer Reference Manual
            Volume 1: Text Programming".
        0 - Ready
        3 - No keyboard
        8 - Keyboard busy in other session
      Ptyp - Keyboard type - VT level 4 only
        0 - LK201  # DEC 420
        1 - LK401  # DEC 420
        4 - LK450  # DEC 510
        5 - PCXAL  # DEC 510"""
    # First get the VT level with a DA2
    myLevel = self.getVTLevel()
    esccmd.DECDSR(esccmd.DSRKeyboard)
    params = escio.ReadCSI('n', expected_prefix='?')
    if myLevel <= 2:
      # VT240 or earlier
      AssertEQ(len(params), 2)
    elif myLevel == 3:
      # VT340 or earlier
      AssertEQ(len(params), 3)
    else:
      # VT420+
      AssertEQ(len(params), 4)
    AssertEQ(params[0], 27)
    if len(params) > 1:
      AssertTrue(params[1] in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                               10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 22, 28,
                               29, 30, 31, 33, 35, 36, 38, 39, 40])
    if len(params) > 2:
      AssertTrue(params[2] in [0, 3, 8])
    if len(params) > 3:
      AssertTrue(params[3] in [0, 1, 4, 5])

  @classmethod
  @vtLevel(4)
  def doLocatorStatusTest(cls, code):
    """I couldn't find docs on these codes outside xterm. 53 and 55 seem to be
    the same. Returns 50 if no locator, 53 if available."""
    esccmd.DECDSR(code)
    params = escio.ReadCSI('n', expected_prefix='?')

    AssertEQ(len(params), 1)
    AssertTrue(params[0] in [50, 53, 55])

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  def test_DECDSR_DSRDECLocatorStatus(self):
    self.doLocatorStatusTest(esccmd.DSRDECLocatorStatus)

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  def test_DECDSR_DSRXtermLocatorStatus(self):
    self.doLocatorStatusTest(esccmd.DSRXtermLocatorStatus)

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  def test_DECDSR_LocatorType(cls):
    """Get the type of the locator (pointing device.)
    0 - unknown (not documented)
    1 - mouse
    2 - tablet"""
    esccmd.DECDSR(esccmd.DSRLocatorId)
    params = escio.ReadCSI('n', expected_prefix='?')

    AssertEQ(params[0], 57)
    AssertTrue(params[1] in [0, 1, 2])
  # 1 = mouse, 2 = tablet, pretty sure 1 is the only reasonable response.

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  def test_DECDSR_DECMSR(cls):
    """Get space available for macros. This test assumes it's always 0."""
    esccmd.DECDSR(esccmd.DECMSR)
    params = escio.ReadCSI('*{')

    # Assume the terminal being tested doesn't support macros. May need to add
    # code some day for a more capable terminal.
    AssertEQ(len(params), 1)
    AssertEQ(params[0], 0)

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  def test_DECDSR_DECCKSR(cls):
    """Get checksum of macros. This test assumes it's always 0."""
    esccmd.DECDSR(Ps=esccmd.DECCKSR, Pid=123)
    value = escio.ReadDCS()
    AssertEQ(value, "123!~0000")

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  def test_DECDSR_DSRDataIntegrity(cls):
    """Check for link errors. Should always report OK."""
    esccmd.DECDSR(esccmd.DSRIntegrityReport)
    params = escio.ReadCSI('n', expected_prefix='?')
    AssertEQ(len(params), 1)
    AssertEQ(params[0], 70)

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented.")
  def test_DECDSR_DSRMultipleSessionStatus(cls):
    """Checks on the status of multiple sessons. SSU refers to some proprietary
    DEC technology that multilexes multiple sessions over a single link using
    the "TDSMP" protocol. Lots of detail here:
    http://paperlined.org/apps/terminals/control_characters/TDSMP.html

    It's safe to assume TDSMP is dead and buried.

    CSI ? 80 ; Ps2 n
      Multiple sessions are operating using the session support utility (SSU)
      and the current SSU state is enabled. Ps2 indicates the maximum number of
      sessions available. Default: Ps2 = 2
    CSI ? 81 ; Ps2 n
      The terminal is currently configured for multiple sessions using SSU but
      the current SSU state is pending. Ps2 indicates the maximum number of
      sessions available. Default: Ps2 = 2
    CSI ? 83 n
      The terminal is not configured for multiple-session operation.
    CSI ? 87 n
      Multiple sessions are operating using a separate physical line for each
      session, not SSU."""
    esccmd.DECDSR(esccmd.DSRMultipleSessionStatus)
    params = escio.ReadCSI('n', expected_prefix='?')
    AssertEQ(len(params), 1)
    # 83 and 87 both seem like reasonable responses for a terminal that
    # supports tabs or windows.
    AssertTrue(params[0] in [83, 87])

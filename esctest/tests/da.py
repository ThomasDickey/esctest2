import escargs
import esccmd
import escio
from escutil import AssertEQ, AssertGE, AssertTrue, knownBug

class DATests(object):

  @classmethod
  def handleDAResponse(cls):
    params = escio.ReadCSI('c', expected_prefix='?')
    # From vttest:
    # 1 = 132 columns
    # 2 = printer port
    # 4 = sixel graphics
    # 6 = selective erase
    # 9 = national replacement character-sets
    # 15 = DEC technical set
    # 16 = locator device port (ReGIS)
    # 17 = terminal state reports
    # 18 = user windows
    # 21 = horizontal scrolling
    # 22 = color
    # 28 = rectangular editing
    # 29 = ANSI text locator
    if escargs.args.expected_terminal == "xterm":
      # This is for a default build. There are various options that could
      # change this, both compile-time and run-time.  XTerm's control sequences
      # document lists the ones it may return.  For a more comprehensive list,
      # see the example for VT420 page 4 of EL-00070-04 Terminal Management
      # (DEC STD 070).
      if escargs.args.max_vt_level == 5:
        expected = [65, 1, 2, 6, 9, 15, 16, 17, 18, 21, 22, 28, 29]
      elif escargs.args.max_vt_level == 4:
        expected = [64, 1, 2, 6, 9, 15, 16, 17, 18, 21, 22, 28, 29]
      elif escargs.args.max_vt_level == 3:
        expected = [63, 1, 2, 6, 9, 15, 22, 29]
      elif escargs.args.max_vt_level == 2:
        expected = [62, 1, 2, 6, 9, 15, 22, 29]
      elif escargs.args.max_vt_level == 1:
        expected = [1, 2] # xterm extension (VT100)
      else:
        expected = [0] # xterm extension
    elif escargs.args.expected_terminal == "iTerm2":
      # 3.4.19
      expected = [62, 4]
    elif escargs.args.expected_terminal == "iTerm2beta":
      # 3.5.0beta10
      expected = [1, 2, 4, 6, 17, 18, 21, 22]
    # Our interest in the primary device attributes is to ensure that the
    # terminal asserts that it supports the features we need.  It may support
    # other features; without a detailed analysis we cannot determine which
    # additional features are inappropriate, e.g, rectangular editing on VT320.
    AssertGE(len(params), len(expected))
    AssertEQ(params[0], expected[0])
    for param in expected:
      AssertTrue(param in params)

  @knownBug(terminal="iTerm2beta", reason="Bug: misinterprets DA as DA2")
  def test_DA_NoParameter(self):
    esccmd.DA()
    self.handleDAResponse()

  @knownBug(terminal="iTerm2beta", reason="Bug: misinterprets DA as DA2")
  def test_DA_0(self):
    esccmd.DA(0)
    self.handleDAResponse()

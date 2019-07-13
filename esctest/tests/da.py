import escargs
import esccmd
import escio
from escutil import AssertEQ, AssertGE, AssertTrue, knownBug

class DATests(object):
  @knownBug(terminal="iTerm2", reason="iTerm2 doesn't report 18 or 22.")
  def handleDAResponse(self):
    params = escio.ReadCSI('c', expected_prefix='?')
    if escargs.args.expected_terminal == "xterm":
      # This is for a default build. There are various options that could
      # change this, both compile-time and run-time.  XTerm's control sequences
      # document lists the ones it may return.  For a more comprehensive list,
      # see DEC STD 070, page 4.
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
      # TODO:  Determine which VT levels are completely supported and add 6,
      # 62, 63, or 64.
      # I believe 18 means we support DECSTB and DECSLRM but I can't find any
      # evidence to substantiate this belief.
      expected = [1, 2, 18, 22]
    # Our interest in the primary device attributes is to ensure that the
    # terminal asserts that it supports the features we need.  It may support
    # other features; without a detailed analysis we cannot determine which
    # additional features are inappropriate, e.g, rectangular editing on VT320.
    AssertGE(len(params), len(expected))
    AssertEQ(params[0], expected[0])
    for param in expected:
      AssertTrue(param in params)

  def test_DA_NoParameter(self):
    esccmd.DA()
    self.handleDAResponse()

  def test_DA_0(self):
    esccmd.DA(0)
    self.handleDAResponse()




import escargs
import esccmd
from esccmd import SET_HEX, QUERY_HEX, SET_UTF8, QUERY_UTF8
from escutil import AssertEQ, GetIconTitle, GetWindowTitle, knownBug, optionRequired


class SMTitleTests(object):

  @classmethod
  @optionRequired(terminal="xterm", option=escargs.XTERM_WINOPS_ENABLED,
                  allowPassWithoutOption=True)
  @knownBug(terminal="iTerm2", reason="SM_Title not implemented.")
  @knownBug(terminal="iTerm2beta", reason="SM_Title not implemented.")
  def test_SMTitle_SetHexQueryUTF8(cls):
    esccmd.RM_Title(SET_UTF8, QUERY_HEX)
    esccmd.SM_Title(SET_HEX, QUERY_UTF8)

    esccmd.ChangeWindowTitle("6162")
    AssertEQ(GetWindowTitle(), "ab")
    esccmd.ChangeWindowTitle("61")
    AssertEQ(GetWindowTitle(), "a")

    esccmd.ChangeIconTitle("6162")
    AssertEQ(GetIconTitle(), "ab")
    esccmd.ChangeIconTitle("61")
    AssertEQ(GetIconTitle(), "a")

  @classmethod
  @optionRequired(terminal="xterm", option=escargs.XTERM_WINOPS_ENABLED,
                  allowPassWithoutOption=True)
  # NOTE: This passes by accident on iTerm2 because it's a silly test that
  # passes when the mode is UTF-8, as it always is in iTerm2.
  def test_SMTitle_SetUTF8QueryUTF8(cls):
    esccmd.RM_Title(SET_HEX, QUERY_HEX)
    esccmd.SM_Title(SET_UTF8, QUERY_UTF8)

    esccmd.ChangeWindowTitle("ab")
    AssertEQ(GetWindowTitle(), "ab")
    esccmd.ChangeWindowTitle("a")
    AssertEQ(GetWindowTitle(), "a")

    esccmd.ChangeIconTitle("ab")
    AssertEQ(GetIconTitle(), "ab")
    esccmd.ChangeIconTitle("a")
    AssertEQ(GetIconTitle(), "a")

  @classmethod
  @optionRequired(terminal="xterm", option=escargs.XTERM_WINOPS_ENABLED,
                  allowPassWithoutOption=True)
  @knownBug(terminal="iTerm2", reason="SM_Title not implemented.")
  @knownBug(terminal="iTerm2beta", reason="SM_Title not implemented.")
  def test_SMTitle_SetUTF8QueryHex(cls):
    esccmd.RM_Title(SET_HEX, QUERY_UTF8)
    esccmd.SM_Title(SET_UTF8, QUERY_HEX)

    esccmd.ChangeWindowTitle("ab")
    AssertEQ(GetWindowTitle(), "6162")
    esccmd.ChangeWindowTitle("a")
    AssertEQ(GetWindowTitle(), "61")

    esccmd.ChangeIconTitle("ab")
    AssertEQ(GetIconTitle(), "6162")
    esccmd.ChangeIconTitle("a")
    AssertEQ(GetIconTitle(), "61")

  @classmethod
  @optionRequired(terminal="xterm", option=escargs.XTERM_WINOPS_ENABLED,
                  allowPassWithoutOption=True)
  # NOTE: This passes by accident on iTerm2 because it's a silly test that
  # passes when both get and set mode are UTF-8.
  def test_SMTitle_SetHexQueryHex(cls):
    esccmd.RM_Title(SET_UTF8, QUERY_UTF8)
    esccmd.SM_Title(SET_HEX, QUERY_HEX)

    esccmd.ChangeWindowTitle("6162")
    AssertEQ(GetWindowTitle(), "6162")
    esccmd.ChangeWindowTitle("61")
    AssertEQ(GetWindowTitle(), "61")

    esccmd.ChangeIconTitle("6162")
    AssertEQ(GetIconTitle(), "6162")
    esccmd.ChangeIconTitle("61")
    AssertEQ(GetIconTitle(), "61")

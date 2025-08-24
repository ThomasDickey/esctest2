# Restoring the cursor does the following things that are not testable:
# * Turn off character attributes
# * Maps the ASCII character set into GL, and the DEC Supplemental Graphic set into GR.
# * Status bar has a separate saved cursor.

# From the Xterm docs, there are several variants of DECRC with different names.

# * CSI u (ANSI RC)
#     ANSI version of DECRC.
# * ESC 8 (DECRC)
#     Restore cursor. Same as CSI u.
# * CSI ? 1048 l (DECRESET TITE INHIBIT)
#     XTerm extension, same as CSI u but can be disabled by a resource.

# Likewise, DECSC can be done with:
# * CSI s (ANSI SC)
#     ANSI version of DECSC, but is disabled in left-right mode (DECSLRM).
# * ESC 7 (DECSC)
#     Saves the cursor
# * CSI ? 1048 h (DECSET TITE INHIBIT)
#     XTerm extension, same as ESC 7 but can be disabled by a resource.
import esc
import esccmd
import escargs
import escio
from esc import empty
from escutil import AssertEQ
from escutil import AssertScreenCharsInRectEqual
from escutil import GetCursorPosition
from escutil import GetScreenSize
from escutil import Rect
from escutil import knownBug
from escutil import vtLevel
from esctypes import Point

class SaveRestoreCursorTests(object):
  """Base class for ANSI SC/RC, DECRC/DECSC, and DECSET/DECRESET TITE
  INHIBIT. Subclasses should implement saveCursor() and restoreCursor()."""

  @classmethod
  def saveCursor(cls):
    return

  @classmethod
  def restoreCursor(cls):
    return

  def test_SaveRestoreCursor_Basic(self):
    esccmd.CUP(Point(5, 6))
    self.saveCursor()
    esccmd.CUP(Point(1, 1))
    self.restoreCursor()
    AssertEQ(GetCursorPosition(), Point(5, 6))

  def test_SaveRestoreCursor_MoveToHomeWhenNotSaved(self):
    esccmd.DECSTR()
    esccmd.CUP(Point(5, 6))
    self.restoreCursor()
    AssertEQ(GetCursorPosition(), Point(1, 1))

  @vtLevel(4)
  def test_SaveRestoreCursor_Reset(self):
    escio.Write("a")        # cursor is now at 2,1
    self.saveCursor()       # remember that...
    esccmd.DECSTR()         # resets saved-location to 1,1, not moving cursor
    escio.Write("b")        # writes text at 2,1
    self.restoreCursor()    # restores cursor to 1,1
    escio.Write("c")        # writes text at 1,1
    AssertScreenCharsInRectEqual(Rect(1, 1, 2, 1), ["cb"])

  @vtLevel(4)
  def test_SaveRestoreCursor_ResetsOriginMode(self):
    esccmd.CUP(Point(5, 6))
    self.saveCursor()

    # Set up margins.
    esccmd.DECSTBM(5, 7)
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(5, 7)

    # Enter origin mode.
    esccmd.DECSET(esccmd.DECOM)

    # Do DECRC, which should reset origin mode.
    self.restoreCursor()

    # Move home
    esccmd.CUP(Point(1, 1))

    # Place an X at cursor, which should be at (1, 1) if DECOM was reset.
    escio.Write("X")

    # Remove margins and ensure origin mode is off for valid test.
    esccmd.DECRESET(esccmd.DECLRMM)
    esccmd.DECSTBM()
    esccmd.DECRESET(esccmd.DECOM)

    # Ensure the X was placed at the true origin
    AssertScreenCharsInRectEqual(Rect(1, 1, 1, 1), ["X"])

  @vtLevel(4)
  def test_SaveRestoreCursor_WorksInLRM(self, shouldWork=True):
    """Subclasses may cause shouldWork to be set to false."""
    esccmd.CUP(Point(2, 3))
    self.saveCursor()
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(1, 10)
    esccmd.CUP(Point(5, 6))
    self.saveCursor()

    esccmd.CUP(Point(4, 5))
    self.restoreCursor()

    if shouldWork:
      AssertEQ(GetCursorPosition(), Point(5, 6))
    else:
      AssertEQ(GetCursorPosition(), Point(2, 3))

  def test_SaveRestoreCursor_AltVsMain(self):
    """Separate saved cursor in alternate screen versus main screen.

    This is xterm-specific, not DEC, because DEC terminals did not implement
    an alternate screen.  xterm maintains separate saved-cursor state for
    the normal (main) and alternate screens so that it can restore the
    position of the cursor in the normal screen when switching back from
    the alternate screen."""
    esccmd.CUP(Point(2, 3))
    self.saveCursor()

    esccmd.DECSET(esccmd.ALTBUF)

    esccmd.CUP(Point(6, 7))
    self.saveCursor()

    esccmd.DECRESET(esccmd.ALTBUF)

    self.restoreCursor()
    AssertEQ(GetCursorPosition(), Point(2, 3))

    esccmd.DECSET(esccmd.ALTBUF)
    self.restoreCursor()
    AssertEQ(GetCursorPosition(), Point(6, 7))

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="DECSCA and DECSERA not implemented", noop=True)
  @knownBug(terminal="iTerm2beta", reason="DECSCA and DECSERA not implemented", noop=True)
  def test_SaveRestoreCursor_Protection(self):
    # Turn on protection and save
    esccmd.DECSCA(1)
    self.saveCursor()

    # Turn off and restore. Restore should turn protection back on.
    esccmd.DECSCA(0)
    self.restoreCursor()

    # Write a protected character and try to erase it, which should fail.
    escio.Write("a")
    esccmd.DECSERA(1, 1, 1, 1)
    AssertScreenCharsInRectEqual(Rect(1, 1, 1, 1), ["a"])

  def test_SaveRestoreCursor_Wrap(self):
    """Test the position of the cursor after turning auto-wrap mode on and off.

    According to DEC STD 070 (see description on page 5-139 as well as
    pseudo-code on following pages), resetting auto-wrap mode resets the
    terminal's last-column flag, which tells the terminal if it is in the
    special wrap/last-column state.  Older versions of xterm did not
    save/restore the last-column flag in DECRC, causing the cursor to be the
    second column rather than the first when text is written "past" the
    wrapping point.
    """
    # Turn on wrap and save
    esccmd.DECSET(esccmd.DECAWM)
    self.saveCursor()

    # Turn off and restore
    esccmd.DECRESET(esccmd.DECAWM)
    self.restoreCursor()

    # See if we're wrapping.
    esccmd.CUP(Point(GetScreenSize().width() - 1, 1))
    escio.Write("abcd")
    if escargs.args.expected_terminal == "xterm":
      AssertEQ(GetCursorPosition().y(), 1)
    else:
      AssertEQ(GetCursorPosition().y(), 2)

  def test_SaveRestoreCursor_ReverseWrapNotAffected(self):
    # Turn on reverse wrap and save
    esccmd.DECSET(esccmd.ReverseWraparound())
    self.saveCursor()

    # Turn off reverse wrap and restore. Restore should turn reverse wrap on.
    esccmd.DECRESET(esccmd.ReverseWraparound())
    self.restoreCursor()

    # See if reverse wrap is still off.
    esccmd.CUP(Point(1, 2))
    escio.Write(esc.BS)
    AssertEQ(GetCursorPosition().x(), 1)

  @vtLevel(4)
  def test_SaveRestoreCursor_InsertNotAffected(self):
    # Turn on insert and save
    esccmd.SM(esccmd.IRM)
    self.saveCursor()

    # Turn off insert and restore. Restore should not turn insert on.
    esccmd.RM(esccmd.IRM)
    self.restoreCursor()

    # See if insert is still off
    esccmd.CUP(Point(1, 1))
    escio.Write("a")
    esccmd.CUP(Point(1, 1))
    escio.Write("b")
    AssertScreenCharsInRectEqual(Rect(1, 1, 2, 1), ["b" + empty()])

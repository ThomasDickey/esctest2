from esc import empty, blank
import esccmd
import escio
from esctypes import Point, Rect
from escutil import AssertScreenCharsInRectEqual, knownBug, vtLevel

class DECSELTests(object):

  @classmethod
  def prepare(cls):
    """Initializes the screen to abcdefghij on the first line with the cursor
    on the 'e'."""
    esccmd.CUP(Point(1, 1))
    escio.Write("abcdefghij")
    esccmd.CUP(Point(5, 1))

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  @knownBug(terminal="iTerm2beta", reason="Not implemented")
  def test_DECSEL_Default(self):
    """Should erase to right of cursor."""
    self.prepare()
    esccmd.DECSEL()
    AssertScreenCharsInRectEqual(Rect(1, 1, 10, 1),
                                 ["abcd" + 6 * empty()])

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  @knownBug(terminal="iTerm2beta", reason="Not implemented")
  def test_DECSEL_0(self):
    """Should erase to right of cursor."""
    self.prepare()
    esccmd.DECSEL(0)
    AssertScreenCharsInRectEqual(Rect(1, 1, 10, 1),
                                 ["abcd" + 6 * empty()])

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  @knownBug(terminal="iTerm2beta", reason="Not implemented")
  def test_DECSEL_1(self):
    """Should erase to left of cursor."""
    self.prepare()
    esccmd.DECSEL(1)
    AssertScreenCharsInRectEqual(Rect(1, 1, 10, 1),
                                 [5 * blank() + "fghij"])

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  @knownBug(terminal="iTerm2beta", reason="Not implemented")
  def test_DECSEL_2(self):
    """Should erase whole line."""
    self.prepare()
    esccmd.DECSEL(2)
    AssertScreenCharsInRectEqual(Rect(1, 1, 10, 1),
                                 [10 * empty()])

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  @knownBug(terminal="iTerm2beta", reason="Not implemented")
  def test_DECSEL_IgnoresScrollRegion(self):
    """Should erase whole line."""
    self.prepare()
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(2, 4)
    esccmd.CUP(Point(5, 1))
    esccmd.DECSEL(2)
    esccmd.DECRESET(esccmd.DECLRMM)
    AssertScreenCharsInRectEqual(Rect(1, 1, 10, 1),
                                 [10 * empty()])

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  @knownBug(terminal="iTerm2beta", reason="Not implemented")
  def test_DECSEL_Default_Protection(self):
    """Should erase to right of cursor."""
    esccmd.DECSCA(1)
    self.prepare()

    # Write an X at 1,1 without protection
    esccmd.DECSCA(0)
    esccmd.CUP(Point(10, 1))
    escio.Write("X")
    esccmd.CUP(Point(5, 1))

    esccmd.DECSEL()
    AssertScreenCharsInRectEqual(Rect(1, 1, 10, 1),
                                 ["abcdefghi" + empty()])

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  @knownBug(terminal="iTerm2beta", reason="Not implemented")
  def test_DECSEL_0_Protection(self):
    """All letters are protected so nothing should happen."""
    esccmd.DECSCA(1)
    self.prepare()

    # Write an X at 1,1 without protection
    esccmd.DECSCA(0)
    esccmd.CUP(Point(10, 1))
    escio.Write("X")

    esccmd.CUP(Point(5, 1))
    esccmd.DECSEL(0)

    AssertScreenCharsInRectEqual(Rect(1, 1, 10, 1),
                                 ["abcdefghi" + empty()])

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  @knownBug(terminal="iTerm2beta", reason="Not implemented")
  def test_DECSEL_1_Protection(self):
    """All letters are protected so nothing should happen."""
    esccmd.DECSCA(1)
    self.prepare()

    # Write an X at 1,1 without protection
    esccmd.DECSCA(0)
    esccmd.CUP(Point(1, 1))
    escio.Write("X")

    esccmd.CUP(Point(5, 1))
    esccmd.DECSEL(1)
    AssertScreenCharsInRectEqual(Rect(1, 1, 10, 1),
                                 [blank() + "bcdefghij"])

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  @knownBug(terminal="iTerm2beta", reason="Not implemented")
  def test_DECSEL_2_Protection(self):
    """All letters are protected so nothing should happen."""
    esccmd.DECSCA(1)
    self.prepare()

    # Write an X at 1,1 without protection
    esccmd.DECSCA(0)
    esccmd.CUP(Point(1, 1))
    escio.Write("X")

    esccmd.DECSEL(2)
    AssertScreenCharsInRectEqual(Rect(1, 1, 10, 1),
                                 [blank() + "bcdefghij"])

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  @knownBug(terminal="iTerm2beta", reason="Not implemented")
  def test_DECSEL_IgnoresScrollRegion_Protection(self):
    """All letters are protected so nothing should happen."""
    esccmd.DECSCA(1)
    self.prepare()

    # Write an X at 1,1 without protection
    esccmd.DECSCA(0)
    esccmd.CUP(Point(1, 1))
    escio.Write("X")

    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(2, 4)
    esccmd.CUP(Point(5, 1))
    esccmd.DECSEL(2)
    esccmd.DECRESET(esccmd.DECLRMM)
    AssertScreenCharsInRectEqual(Rect(1, 1, 10, 1),
                                 [blank() + "bcdefghij"])

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="xterm",
            reason="DECSEL respects ISO protection for backward compatibility,"
            + " per email from Thomas")
  @knownBug(terminal="iTerm2", reason="DECSED not implemented")
  @knownBug(terminal="iTerm2beta", reason="DECSED not implemented")
  def test_DECSEL_doesNotRespectISOProtect(cls):
    """DECSEL does not respect ISO protection."""
    escio.Write("a")
    esccmd.SPA()
    escio.Write("b")
    esccmd.EPA()
    esccmd.DECSEL(2)
    AssertScreenCharsInRectEqual(Rect(1, 1, 2, 1), [blank() * 2])

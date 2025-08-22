import tests.decrectops
import esc
import esccmd
import escio
from escutil import AssertScreenCharsInRectEqual, Point, Rect, knownBug, vtLevel
from tests.decrectops import FillRectangleTests

class DECSERATests(FillRectangleTests):
  def __init__(self):
    tests.decrectops.FillRectangleTests.__init__(self)
    self._always_return_blank = False

  def prepare(self):
    esccmd.CUP(Point(1, 1))
    i = 1
    for line in self.data():
      # Protect odd-numbered rows
      esccmd.DECSCA(i)
      escio.Write(line + esc.CR + esc.LF)
      i = 1 - i
    esccmd.DECSCA(0)

  def fill(self, top=None, left=None, bottom=None, right=None):
    esccmd.DECSERA(top, left, bottom, right)

  def characters(self, point, count):
    if self._always_return_blank:
      return esc.blank() * count
    s = ""
    data = self.data()
    for i in range(count):
      p = Point(point.x() + i, point.y())
      if p.y() >= len(data):
        s += esc.blank()
        continue
      line = data[p.y() - 1]
      if p.x() >= len(line):
        s += esc.blank()
        continue
      if point.y() % 2 == 1:
        s += line[p.x() - 1]
      else:
        s += esc.blank()
    return s

  @knownBug(terminal="iTerm2beta", reason="Erase fills rather than clears.")
  def test_DECSERA_basic(self):
    self.fillRectangle_basic()

  def test_DECSERA_invalidRectDoesNothing(self):
    self.fillRectangle_invalidRectDoesNothing()

  @knownBug(terminal="iTerm2beta", reason="Erase fills rather than clears.")
  def test_DECSERA_defaultArgs(self):
    try:
      self._always_return_blank = True
      self.fillRectangle_defaultArgs()
    finally:
      self._always_return_blank = False

  @knownBug(terminal="iTerm2beta", reason="Erase fills rather than clears.")
  def test_DECSERA_respectsOriginMode(self):
    self.fillRectangle_respectsOriginMode()

  @knownBug(terminal="iTerm2beta", reason="Erase fills rather than clears.")
  def test_DECSERA_overlyLargeSourceClippedToScreenSize(self):
    self.fillRectangle_overlyLargeSourceClippedToScreenSize()

  def test_DECSERA_cursorDoesNotMove(self):
    self.fillRectangle_cursorDoesNotMove()

  @knownBug(terminal="iTerm2beta", reason="Erase fills rather than clears.")
  def test_DECSERA_ignoresMargins(self):
    self.fillRectangle_ignoresMargins()

  @classmethod
  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="DECSED not implemented")
  @knownBug(terminal="iTerm2beta", reason="DECSED not implemented")
  def test_DECSERA_doesNotRespectISOProtect(cls):
    """DECSERA does not respect ISO protection."""
    escio.Write("a")
    esccmd.SPA()
    escio.Write("b")
    esccmd.EPA()
    esccmd.DECSERA(1, 1, 1, 2)
    AssertScreenCharsInRectEqual(Rect(1, 1, 2, 1), [esc.blank() * 2])

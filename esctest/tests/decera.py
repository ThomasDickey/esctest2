import esc
import esccmd

from tests.decrectops import FillRectangleTests
from escutil import knownBug

class DECERATests(FillRectangleTests):
  def fill(self, top=None, left=None, bottom=None, right=None):
    esccmd.DECERA(top, left, bottom, right)

  def characters(self, point, count):
    return esc.blank() * count

  @knownBug(terminal="iTerm2beta", reason="Erase fills rather than clears.")
  def test_DECERA_basic(self):
    self.fillRectangle_basic()

  def test_DECERA_invalidRectDoesNothing(self):
    self.fillRectangle_invalidRectDoesNothing()

  @knownBug(terminal="iTerm2beta", reason="Erase fills rather than clears.")
  def test_DECERA_defaultArgs(self):
    self.fillRectangle_defaultArgs()

  @knownBug(terminal="iTerm2beta", reason="Erase fills rather than clears.")
  def test_DECERA_respectsOriginMode(self):
    self.fillRectangle_respectsOriginMode()

  @knownBug(terminal="iTerm2beta", reason="Erase fills rather than clears.")
  def test_DECERA_overlyLargeSourceClippedToScreenSize(self):
    self.fillRectangle_overlyLargeSourceClippedToScreenSize()

  def test_DECERA_cursorDoesNotMove(self):
    self.fillRectangle_cursorDoesNotMove()

  @knownBug(terminal="iTerm2beta", reason="Erase fills rather than clears.")
  def test_DECERA_ignoresMargins(self):
    self.fillRectangle_ignoresMargins()

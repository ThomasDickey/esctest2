import esccmd
from tests.save_restore_cursor import SaveRestoreCursorTests

class ANSIRCTests(SaveRestoreCursorTests):
  def __init__(self):
    SaveRestoreCursorTests.__init__(self)

  @classmethod
  def saveCursor(cls):
    esccmd.ANSISC()

  @classmethod
  def restoreCursor(cls):
    esccmd.ANSIRC()

  def test_SaveRestoreCursor_ResetsOriginMode(self):
    SaveRestoreCursorTests.test_SaveRestoreCursor_ResetsOriginMode(self)

  def test_SaveRestoreCursor_WorksInLRM(self, shouldWork=True):
    SaveRestoreCursorTests.test_SaveRestoreCursor_WorksInLRM(self, False)

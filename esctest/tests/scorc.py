import esccmd
from tests.save_restore_cursor import SaveRestoreCursorTests

class SCORCTests(SaveRestoreCursorTests):
  def __init__(self):
    SaveRestoreCursorTests.__init__(self)

  @classmethod
  def saveCursor(cls):
    esccmd.SCOSC()

  @classmethod
  def restoreCursor(cls):
    esccmd.SCORC()

  def test_SaveRestoreCursor_WorksInLRM(self, shouldWork=True):
    SaveRestoreCursorTests.test_SaveRestoreCursor_WorksInLRM(self, False)

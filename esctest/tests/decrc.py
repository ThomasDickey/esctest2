import esccmd
from tests.save_restore_cursor import SaveRestoreCursorTests

class DECRCTests(SaveRestoreCursorTests):

  @classmethod
  def saveCursor(cls):
    esccmd.DECSC()

  @classmethod
  def restoreCursor(cls):
    esccmd.DECRC()

  def test_SaveRestoreCursor_WorksInLRM(self, shouldWork=True):
    SaveRestoreCursorTests.test_SaveRestoreCursor_WorksInLRM(self, True)

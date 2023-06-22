import tests.save_restore_cursor
import esccmd

class DECRCTests(tests.save_restore_cursor.SaveRestoreCursorTests):

  @classmethod
  def saveCursor(cls):
    esccmd.DECSC()

  @classmethod
  def restoreCursor(cls):
    esccmd.DECRC()

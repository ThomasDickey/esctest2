from esc import empty
import escio
from escutil import AssertScreenCharsInRectEqual, vtLevel
from esctypes import Rect

class DCSTests(object):

  @classmethod
  @vtLevel(4)
  def test_DCS_Unrecognized(cls):
    """An unrecognized DCS code should be swallowed"""
    escio.WriteDCS("z", "0")
    AssertScreenCharsInRectEqual(Rect(1, 1, 1, 1), empty())

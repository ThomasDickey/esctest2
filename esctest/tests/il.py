from esc import empty
import esccmd
import escio
from esctypes import Point, Rect
from escutil import AssertScreenCharsInRectEqual, GetScreenSize, vtLevel

class ILTests(object):

  @classmethod
  def prepare_wide(cls):
    """Sets up the display as:
    abcde
    fghij
    klmno

    With the cursor on the 'h'.
    """
    esccmd.CUP(Point(1, 1))
    escio.Write("abcde")
    esccmd.CUP(Point(1, 2))
    escio.Write("fghij")
    esccmd.CUP(Point(1, 3))
    escio.Write("klmno")

    esccmd.CUP(Point(2, 3))

  @classmethod
  def prepare_region(cls):
    # The capital letters are in the scroll region
    lines = ["abcde",
             "fGHIj",
             "kLMNo",
             "pQRSt",
             "uvwxy"]
    for i in range(len(lines)):
      esccmd.CUP(Point(1, i + 1))
      escio.Write(lines[i])

    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(2, 4)
    esccmd.DECSTBM(2, 4)

    # Place cursor on the 'H'
    esccmd.CUP(Point(3, 2))

  @vtLevel(4)
  def test_IL_DefaultParam(self):
    """Should insert a single line below the cursor."""
    self.prepare_wide()
    esccmd.IL()
    AssertScreenCharsInRectEqual(Rect(1, 1, 5, 4),
                                 ["abcde",
                                  "fghij",
                                  empty() * 5,
                                  "klmno"])

  @vtLevel(4)
  def test_IL_ExplicitParam(self):
    """Should insert two lines below the cursor."""
    self.prepare_wide()
    esccmd.IL(2)
    AssertScreenCharsInRectEqual(Rect(1, 1, 5, 5),
                                 ["abcde",
                                  "fghij",
                                  empty() * 5,
                                  empty() * 5,
                                  "klmno"])

  @classmethod
  @vtLevel(4)
  def test_IL_ScrollsOffBottom(cls):
    """Lines should be scrolled off the bottom of the screen."""
    height = GetScreenSize().height()
    for i in range(height):
      esccmd.CUP(Point(1, i + 1))
      escio.Write("%04d" % (i + 1))
    esccmd.CUP(Point(1, 2))
    esccmd.IL()

    expected = 1
    for i in range(height):
      y = i + 1
      if y == 2:
        AssertScreenCharsInRectEqual(Rect(1, y, 4, y), [empty() * 4])
      else:
        AssertScreenCharsInRectEqual(Rect(1, y, 4, y), ["%04d" % expected])
        expected += 1

  @vtLevel(4)
  def test_IL_RespectsScrollRegion(self):
    """When IL is invoked while the cursor is within the scroll region, lines
    within the scroll regions hould be scrolled down; lines within should
    remain unaffected."""
    self.prepare_region()
    esccmd.IL()

    esccmd.DECRESET(esccmd.DECLRMM)
    esccmd.DECSTBM()

    AssertScreenCharsInRectEqual(Rect(1, 1, 5, 5),
                                 ["abcde",
                                  "f" + empty() * 3 + "j",
                                  "kGHIo",
                                  "pLMNt",
                                  "uvwxy"])

  @vtLevel(4)
  def test_IL_RespectsScrollRegion_Over(self):
    """Scroll by more than the available space in a region."""
    self.prepare_region()
    esccmd.IL(99)

    esccmd.DECRESET(esccmd.DECLRMM)
    esccmd.DECSTBM()

    AssertScreenCharsInRectEqual(Rect(1, 1, 5, 5),
                                 ["abcde",
                                  "f" + empty() * 3 + "j",
                                  "k" + empty() * 3 + "o",
                                  "p" + empty() * 3 + "t",
                                  "uvwxy"])

  @vtLevel(4)
  def test_IL_AboveScrollRegion(self):
    """IL is a no-op outside the scroll region."""
    self.prepare_region()
    esccmd.CUP(Point(1, 1))
    esccmd.IL()

    esccmd.DECRESET(esccmd.DECLRMM)
    esccmd.DECSTBM()

    AssertScreenCharsInRectEqual(Rect(1, 1, 5, 5),
                                 ["abcde",
                                  "fGHIj",
                                  "kLMNo",
                                  "pQRSt",
                                  "uvwxy"])

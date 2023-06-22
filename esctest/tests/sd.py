from esc import empty
import esccmd
import escio
from esctypes import Point, Rect
from escutil import AssertScreenCharsInRectEqual, GetScreenSize, vtLevel

class SDTests(object):
  """Test SD (scroll down), referred to as PAN UP in DEC STD 070.

  The DEC programmer reference manuals do not mention this, but ECMA-48
  and DEC STD 070 both state that the "Active Position" (the cursor)
  does not move along with the data.
  """

  @classmethod
  def prepare(cls):
    """Sets the screen up as
    abcde
    fghij
    klmno
    pqrst
    uvwxy

    With the cursor on the 'h'."""
    lines = ["abcde",
             "fghij",
             "klmno",
             "pqrst",
             "uvwxy"]
    for i in range(len(lines)):
      y = i + 1
      line = lines[i]
      esccmd.CUP(Point(1, y))
      escio.Write(line)
    esccmd.CUP(Point(3, 2))

  @vtLevel(4)
  def test_SD_DefaultParam(self):
    """SD with no parameter should scroll the screen contents down one line."""
    self.prepare()
    esccmd.SD()
    expected_lines = [empty() * 5,
                      "abcde",
                      "fghij",
                      "klmno",
                      "pqrst"]
    AssertScreenCharsInRectEqual(Rect(1, 1, 5, 5), expected_lines)

  @vtLevel(4)
  def test_SD_ExplicitParam(self):
    """SD should scroll the screen down by the number of lines given in the parameter."""
    self.prepare()
    esccmd.SD(2)
    expected_lines = [empty() * 5,
                      empty() * 5,
                      "abcde",
                      "fghij",
                      "klmno"]
    AssertScreenCharsInRectEqual(Rect(1, 1, 5, 5), expected_lines)

  @classmethod
  @vtLevel(4)
  def test_SD_CanClearScreen(cls):
    """An SD equal to the height of the screen clears it.

    Some older versions of xterm failed this test, due to an incorrect fix
    for debugging-assertions in patch #318.  That was corrected in #332.
    """
    # Fill the screen with 0001, 0002, ..., height. Fill expected_lines with empty rows.
    height = GetScreenSize().height()
    expected_lines = []
    for i in range(height):
      y = i + 1
      esccmd.CUP(Point(1, y))
      escio.Write("%04d" % y)
      expected_lines.append(empty() * 4)

    # Scroll by |height|
    esccmd.SD(height)

    # Ensure the screen is empty
    AssertScreenCharsInRectEqual(Rect(1, 1, 4, height), expected_lines)

  @vtLevel(4)
  def test_SD_RespectsTopBottomScrollRegion(self):
    """When the cursor is inside the scroll region, SD should scroll the
    contents of the scroll region only."""
    self.prepare()
    esccmd.DECSTBM(2, 4)
    esccmd.CUP(Point(3, 2))
    esccmd.SD(2)
    esccmd.DECSTBM()

    expected_lines = ["abcde",
                      empty() * 5,
                      empty() * 5,
                      "fghij",
                      "uvwxy"]
    AssertScreenCharsInRectEqual(Rect(1, 1, 5, 5), expected_lines)

  @vtLevel(4)
  def test_SD_OutsideTopBottomScrollRegion(self):
    """When the cursor is outside the scroll region, SD should scroll the
    contents of the scroll region only."""
    self.prepare()
    esccmd.DECSTBM(2, 4)
    esccmd.CUP(Point(1, 1))
    esccmd.SD(2)
    esccmd.DECSTBM()

    expected_lines = ["abcde",
                      empty() * 5,
                      empty() * 5,
                      "fghij",
                      "uvwxy"]
    AssertScreenCharsInRectEqual(Rect(1, 1, 5, 5), expected_lines)

  @vtLevel(4)
  def test_SD_RespectsLeftRightScrollRegion(self):
    """When the cursor is inside the scroll region, SD should scroll the
    contents of the scroll region only."""
    self.prepare()
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(2, 4)
    esccmd.CUP(Point(3, 2))
    esccmd.SD(2)
    esccmd.DECRESET(esccmd.DECLRMM)

    expected_lines = ["a" + empty() * 3 + "e",
                      "f" + empty() * 3 + "j",
                      "kbcdo",
                      "pghit",
                      "ulmny"]
    AssertScreenCharsInRectEqual(Rect(1, 1, 5, 5), expected_lines)

  @vtLevel(4)
  def test_SD_OutsideLeftRightScrollRegion(self):
    """When the cursor is outside the scroll region, SD should scroll the
    contents of the scroll region only."""
    self.prepare()
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(2, 4)
    esccmd.CUP(Point(1, 2))
    esccmd.SD(2)
    esccmd.DECSTBM()
    esccmd.DECRESET(esccmd.DECLRMM)

    expected_lines = ["a" + empty() * 3 + "e",
                      "f" + empty() * 3 + "j",
                      "kbcdo",
                      "pghit",
                      "ulmny",
                      empty() + "qrs" + empty(),
                      empty() + "vwx" + empty()]
    AssertScreenCharsInRectEqual(Rect(1, 1, 5, 7), expected_lines)

  @vtLevel(4)
  def test_SD_LeftRightAndTopBottomScrollRegion(self):
    """When the cursor is outside the scroll region, SD should scroll the
    contents of the scroll region only."""
    self.prepare()
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(2, 4)
    esccmd.DECSTBM(2, 4)
    esccmd.CUP(Point(1, 2))
    esccmd.SD(2)
    esccmd.DECSTBM()
    esccmd.DECRESET(esccmd.DECLRMM)

    expected_lines = ["abcde",
                      "f" + empty() * 3 + "j",
                      "k" + empty() * 3 + "o",
                      "pghit",
                      "uvwxy"]
    AssertScreenCharsInRectEqual(Rect(1, 1, 5, 5), expected_lines)

  @vtLevel(4)
  def test_SD_BigScrollLeftRightAndTopBottomScrollRegion(self):
    """Scroll a lr and tb scroll region by more than its height."""
    self.prepare()
    esccmd.DECSET(esccmd.DECLRMM)
    esccmd.DECSLRM(2, 4)
    esccmd.DECSTBM(2, 4)
    esccmd.CUP(Point(1, 2))
    esccmd.SD(99)
    esccmd.DECSTBM()
    esccmd.DECRESET(esccmd.DECLRMM)

    expected_lines = ["abcde",
                      "f" + empty() * 3 + "j",
                      "k" + empty() * 3 + "o",
                      "p" + empty() * 3 + "t",
                      "uvwxy"]
    AssertScreenCharsInRectEqual(Rect(1, 1, 5, 5), expected_lines)

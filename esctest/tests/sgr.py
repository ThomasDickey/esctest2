import esccmd
import escio
from escutil import AssertCharHasSGR
from esctypes import Point

class SGRTests(object):

  @classmethod
  def test_SGR_Bold(cls):
    """Tests bold."""
    escio.Write("x")
    esccmd.SGR(esccmd.SGR_BOLD)
    escio.Write("y")
    AssertCharHasSGR(Point(1, 1),
                     [esccmd.SGR_FG_DEFAULT,
                      esccmd.SGR_BG_DEFAULT],
                     [esccmd.SGR_BOLD])
    AssertCharHasSGR(Point(2, 1),
                     [esccmd.SGR_FG_DEFAULT,
                      esccmd.SGR_BG_DEFAULT,
                      esccmd.SGR_BOLD])

# TODO: Write a lot more tests :)

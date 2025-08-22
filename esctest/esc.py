import escargs

NUL = chr(0)
BEL = chr(7)
BS = chr(8)
TAB = chr(9)
LF = chr(10)
VT = chr(11)
CR = chr(13)
FF = chr(12)
ESC = chr(27)

S7C1T = ESC + " F"
S8C1T = ESC + " G"

# VT x00 level. vtLevel may be 1, 2, 3, 4, or 5.
vtLevel = 1

# xterm distinguishes "blanks" (cells where a space was written) from empty
# space (after an erase) to use that in selection.  DEC's documentation does
# not have anything analogous (although screenshots demonstrate that it gives a
# similar result).  These scripts use DECRQCRA to guess what a given cell
# contains, and make the assumption that a NUL corresponds to the latter.
#
# The checksum computation in xterm patch #279 kept the distinction, returning
# zero for cells which were empty.  xterm patch #334 changed DECRQCRA for
# better consistency with the existing documentation, and computed empty
# and blank cells as if both hold a space.  This function assumes that the
# terminal has been set up to use that convention if the --xterm-checksum=334
# option was given.
def empty():
  if escargs.args.xterm_checksum >= 334:
    return ' '
  return NUL

def blank():
  if escargs.args.expected_terminal == "xterm":
    return ' '
  return NUL

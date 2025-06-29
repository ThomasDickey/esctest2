# -----------------------------------------------------------------------------
# Copyright 2025 by Thomas E. Dickey
#
#                         All Rights Reserved
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE ABOVE LISTED COPYRIGHT HOLDER(S) BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Except as contained in this notice, the name(s) of the above copyright
# holders shall not be used in advertising or otherwise to promote the
# sale, use or other dealings in this Software without prior written
# authorization.
# -----------------------------------------------------------------------------
'''
Given an X window-id, find the child of the root window which matches or
contains that window. to provide the outer and inner window dimensions.
'''

import os
import re
import array as arr

from esclog import LogInfo, LogDebug
from esctypes import Point, Size

outer_size = Size(0, 0)
inner_size = Size(0, 0)
pointed_to = Point(0, 0)

def read_info(window_id):
  '''
  Read "tree" output of xwininfo from the root (top-level) window, to locate a
  given window-id.  The "tree" output contains additional information, but all
  we are interest in are the lines whose first nonspace text is a hexadecimal
  value (a window-id).

  The indentation of these window-id lines tells us the depth in the window
  hierarchy.  The root window can contain several windows, which may be the
  one we are looking for, or its parent.  When we have distinct parent and
  target windows, the inner window typically has "window decorations", i.e.,
  a border and (usually) a title (within its own window).

  After the window-id, these lines have the command (e.g., WM_COMMAND) and
  the window-title (e.g,, the WM_NAME property).  Those are not useful, so
  we discard them.

  After the command and title strings are the numbers that we want.  There
  are two chunks (separated by whitespace), documented in the X manual page:

  The first chunk has WIDTHxHEIGHT+XOFF+YOFF where the "+XOFF+YOFF" (with
  either "+" or "-" sign) gives the position of this window within its parent.

  The second chunk can be ignored.  It gives the position of the window on the
  screen.
  '''
  global outer_size, inner_size, pointed_to
  LogInfo(f"Reading X window info for {hex(window_id)}")
  if window_id == 0:
    return
  try:
    indents = arr.array('i', [0])
    windows = arr.array('i', [0])
    numbers = [0]
    level = 0
    with os.popen("xwininfo -root -tree", "r") as stream:
      for line in stream:
        if not re.match(r"^\s+0x[0-9A-Fa-f]+\s+.*:\s+", line):
          continue
        line = line[:-1]
        LogInfo(line)
        leading = len(re.sub("0x.*", "", line))
        LogDebug(f"checking {leading} vs indents[{len(indents)-1}]: {indents[len(indents)-1]}")
        if leading > indents[len(indents) - 1]:
          level = len(indents)
          indents.append(leading)
          LogDebug(f"append indents[{len(indents) - 1}]: {leading}")
        else:
          for i in range(len(indents) - 1):
            LogDebug(f"search indents[{i}:{len(indents)-1}]: {indents[i]}")
            if indents[i] == leading:
              level = i
              LogDebug(f"match indents[{i}]: {indents[i]}")
              break
        while len(numbers) <= level:
          numbers.extend([0])
          windows.extend([0])
        numbers[level] = _parse_numbers(line)
        windows[level] = _parse_windows(line)
        LogDebug(f"trimmed {numbers[level]}")
        LogDebug(f"level {level}:{len(indents) - 1} {leading} vs {indents[level]}")
        if windows[level] == window_id:
          LogInfo("found target")
          for i in range(1, level + 1):
            LogInfo(f"stack {i}:{numbers[i]}")
          outer_size = _parse_dimension(numbers[1])
          inner_size = _parse_dimension(numbers[level])
          # TODO what if there is intermediate window?
          # TODO what if position is relative to right/bottom?
          pointed_to = _parse_position(numbers[level])
          break
  except Exception as err:
    LogInfo(f"Exception occurred: {err}")

def have_info():
  '''
  check if we have parsed size and coordination information from xwininfo
  '''
  return outer_size.height() > 0 \
    and outer_size.width() > 0 \
    and outer_size.height() >= inner_size.height() \
    and outer_size.width() >= inner_size.width()

def top_margin():
  ''' retrieve the inner window's top-margin '''
  result = 0
  if outer_size != inner_size:
    result = pointed_to.y()
  return result

def left_margin():
  ''' retrieve the inner window's left-margin '''
  result = 0
  if outer_size != inner_size:
    result = pointed_to.x()
  return result

def _parse_dimension(numbers):
  w_by_h = re.sub(r'^\s*0x\S+\s+(\d+)x(\d+).*', r'\1 \2', numbers).split(" ")
  LogInfo(f"dimension {numbers} -> {w_by_h[0]} by {w_by_h[1]}")
  return Size(w_by_h[0], w_by_h[1])

def _parse_position(numbers):
  offset = re.sub(r'^\s*0x\S+\s+\d+x\d+\+(\d+)\+(\d+).*', r'\1 \2', numbers).split(" ")
  LogInfo(f"position {numbers} -> ( {offset[0]} , {offset[1]} )")
  return Point(offset[0], offset[1])

def _parse_numbers(value):
  '''
  xwininfo returns window information in this form:
      0xe0000e "sh": ("xterm" "XTerm")  724x364+5+29  +105+129
  We don't want the middle part.  Trim it out, leaving numbers.
  '''
  return re.sub(r'\s+("[^"]*"|\([^)]*\)):\s+("[^"]*"|\([^)]*\))\s+', " ", value).strip()

def _parse_windows(value):
  return int(re.sub(r'^(0x\S+)\s.*', r'\1', _parse_numbers(value)), 16)

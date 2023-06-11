''' workaround for Python encoding-related regressions '''
import sys

def to_binary(s):
  ''' convert str to bytes '''
  if sys.version_info >= (3, 0):
    return s.encode('latin-1')
  return s

def to_string(s):
  ''' convert bytes to str '''
  if sys.version_info >= (3, 0):
    return s.decode('latin-1')
  return s

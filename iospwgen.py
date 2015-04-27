from __future__ import division, print_function

from binascii import hexlify
from functools import partial
from math import log
from os import urandom
from zlib import decompress
import sys

WORDLIST = decompress(open('wordlist.csv.zlib').read()).split(',')
WORDLIST_BITS = log(len(WORDLIST), 2)

def getrandbits(bitlength):
  """Return a Python long with `k` random bits."""
  num_bytes = (bitlength + 7) // 8
  mask = 2 ** bitlength - 1
  s = urandom(num_bytes)
  return mask & int(hexlify(s), 16)


def randbelow(upper):
  """Return a Python long less than or equal to upper."""
  bits = int(log(upper, 2))
  candidate = getrandbits(bits)
  while candidate > upper:
    candidate = getrandbits(bits)
  return candidate

IOS_SYMBOLS = r''''-/:;()$&@.,?!'"123456789'''
IOS_ALPHABET = 'abcdefghijkmnopqrstuvwxyz' + 'ABCDEFGHIJKLMNPQRSTUVWXYZ'
IOS = IOS_SYMBOLS + IOS_ALPHABET
IOS_BPS = log(len(IOS), 2)

ZBASE32 = 'ybndrfg8ejkmcpqxot1uwisza345h769'

def group(s, grouplen, groupchar=' '):
  """Group characters in a string with groupchar."""
  out = ''.join((x + groupchar if (i and ((i % grouplen) == 0)) else x)
                for i, x in enumerate(s))
  return out

def pwgen(it, bits=92, by=3, sort=False):
  """Note that sorting the characters rather decreases the
  guessing strength of the password.
  """
  length = (bits // int(log(len(it), 2)))
  s = [it[randbelow(len(it))] for _ in range(length)]
  s = sorted(s) if sort else s
  return group(''.join(s), by)

pwgen_zbase32 = partial(pwgen, ZBASE32, bits=80, by=4)
pwgen_ios = partial(pwgen, IOS, bits=92, by=3)

def pwgen_words(bits=92):
  it = WORDLIST
  length = (bits // int(log(len(it), 2)))
  s = [it[randbelow(len(it))] for _ in range(length)]
  return ' '.join(s)

if __name__ == '__main__':
  bits = int(sys.argv[1]) if len(sys.argv) > 1 else None
  if bits is None:
    t = raw_input('bits: ')
    bits = int(t)
  while True:
    i = 0
    t = raw_input('[ziwZI]: ')
    if t.lower() == 'z':
      print(pwgen_zbase32(bits=bits, sort=(t == 'Z')))
    if t.lower() == 'i':
      print(pwgen_ios(bits=bits, sort=(t == 'I')))
    if t == 'w':
      print(pwgen_words(bits=bits))

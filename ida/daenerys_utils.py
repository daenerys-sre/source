# Daenerys IDA/Ghidra interop framework
# by Elias Bachaalany <elias.bachaalany@gmail.com>
#
# Python utility functions

import numbers

def is_number(n):
	return isinstance(n, numbers.Number)
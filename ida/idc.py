#idc.py adapter
#@category Daenerys.Framework.IDAPython

"""
Daenerys IDA/Ghidra interop library
by Elias Bachaalany <elias.bachaalany@gmail.com>
"""

import idaapi

INF_MIN_EA     = 76           # ea_t;    The lowest address used in the program
INF_MAX_EA     = 80           # ea_t;    The highest address used in the program

BADADDR = idaapi.BADADDR

def ScreenEA(): 
	return idaapi.get_screen_ea()


def here(): 
	return idaapi.get_screen_ea()


def MinEA(): 
	return get_inf_attr(INF_MIN_EA)


def MaxEA(): 
	return get_inf_attr(INF_MAX_EA)


def get_inf_attr(offset):
	if offset == INF_MIN_EA:
		return idaapi.cvar.inf.min_ea
	elif offset == INF_MAX_EA:
		return idaapi.cvar.inf.max_ea


def Byte(ea):
	return idaapi.get_wide_byte(ea)


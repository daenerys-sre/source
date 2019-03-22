#idaapi.py adapter
#@category Daenerys.Framework.IDAPython

"""
Daenerys IDA/Ghidra interop library
by Elias Bachaalany <elias.bachaalany@gmail.com>
"""

import sys
import inspect
import daenerys_utils as utils

from ghidra.program.model.address import GenericAddress
from ghidra.program.model.address import Address

# -------------------------------------------------------------------
class ea_t(long):
    """Effective address class. It can also store the Ghidra Address object in it.
    An effective address in IDA Pro is a 32-bits or 64-bits number.
    """
    @staticmethod
    def init(ea, addr):
        ea = ea_t(ea)
        ea.address = addr
        return ea


# -------------------------------------------------------------------
# Ghidra initialization

def ghidra_state():
    """Current Ghidra script state"""
    return _state


def _deduce_state_variables():
    """Deduce the needed invocation context"""

    var_names = ('currentAddress', 'currentHighlight', 'currentLocation', 'currentProgram', 'currentSelection', 'state')
    """Sentinel variables that we can use to detect the invocation context"""
    for s in inspect.stack():
        if isinstance(s, tuple): s = s[0]
        if all(x in s.f_locals for x in var_names):
            # Bring all the state variables to this module's global scope
            for x in var_names:
                globals()['_' + x] = s.f_locals[x]
            return

    raise Exception('Failed to initialize Daenerys idaapi module!')

_deduce_state_variables()

# Store the state for use from other modules (w/o requiring to import this module)
sys.__ghidra_state__ = _state

# Assume program bitness based on the first memory block pointer size
BADADDR = ea_t.init(
    0xFFFFFFFFFFFFFFFF if _currentProgram.getMinAddress().getPointerSize() == 8 else 0xFFFFFFFF,
    Address.NO_ADDRESS)


_memory = _currentProgram.getMemory()

# -------------------------------------------------------------------
# Ghidra helper functions

def AddressToEA(addr):
    """Converts a Ghidra Address object to an ea"""
    return ea_t.init(addr.getOffset(), addr)


def eaToAddress(ea):
    """Converts an effective address to a Ghidra Address object"""
    if isinstance(ea, GenericAddress):
        # No conversion needed
        return ea
    elif isinstance(ea, ea_t):
        return ea.address
    elif utils.is_number(ea):
        addrs = _currentProgram.parseAddress("0x%x" % ea)
        # Return the first memory address
        for addr in addrs:
            if addr.isMemoryAddress():
                return addr

    return Address.NO_ADDRESS


def ghidra_program_getMinAddress():
    return _currentProgram.getMinAddress()


def ghidra_program_getMaxAddress():
    return _currentProgram.getMaxAddress()


# ------------------------------------------------------------------------
def get_wide_byte(ea):
    """Reads a byte (ida_bytes.get_wide_byte()"""
    return _memory.getByte(eaToAddress(ea)) & 0xff


# ------------------------------------------------------------------------
def get_screen_ea():
    """ida_kernwin.get_screen_ea()"""
    return AddressToEA(_state.getCurrentAddress())


# ------------------------------------------------------------------------
# IDA inf global variable emulator
class _inf(object):
    @property
    def min_ea(self):
        return AddressToEA(ghidra_program_getMinAddress())

    @property
    def max_ea(self):
        return AddressToEA(ghidra_program_getMaxAddress())

class _cvar(object):
    inf  = _inf()


cvar = _cvar()

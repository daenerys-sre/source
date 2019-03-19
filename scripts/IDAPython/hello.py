# Daenerys IDAPython "hello world" example script

#@category Daenerys.IDAPython.Examples

import idc

print("Hello world from Ghidra...")
print("Current address is: %x" % idc.here())
print("Min address: %x - Max address: %x" % (idc.MinEA(), idc.MaxEA()))
print("Byte at current address is: %02x" % idc.Byte(idc.here()))
print("BADADDR=%x" % idc.BADADDR)

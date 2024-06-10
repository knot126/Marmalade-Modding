#!/usr/bin/env python3
"""
Print out basic info about a uncompressed s3e's header
"""

import struct
import sys

def hexdump(data, perline = 16):
	"""
	Generate a hexdump as a string
	"""
	
	line = 0
	buf = []
	result = ""
	
	for d in data:
		buf.append("{:02x}".format(d))
		
		if (len(buf) == perline):
			result += "{:06x}  ".format(perline * line) + " ".join(buf) + "\n"
			buf = []
			line += 1
	
	if buf:
		result += "{:06x}  ".format(perline * line) + " ".join(buf) + "\n"
	
	return result

def main():
	if (len(sys.argv) < 2):
		print(f"Usage: {sys.argv[0]} <s3e file>")
	
	f = open(sys.argv[1], "rb")
	
	# Basic header
	basic_bytes = f.read(0x40)
	mv = memoryview(basic_bytes)
	header = mv.cast("I")
	header_short = mv.cast("H")
	
	print(f" *** BASIC HEADER *** ")
	print(f"ident        = {hex(header[0])} ({basic_bytes[0:4].decode('latin-1')})")
	old_format = ((header[1] >> 0x10) & 0xff) == 0
	if (old_format):
		print(f"version      = {hex(header[1])} ({header[1] >> 12}.{header[1] & 0xff})")
	else:
		print(f"version      = {hex(header[1])} ({header[1] >> 16}.{(header[1] >> 8) & 0xff}.{header[1] & 0xff})")
	print(f"flags        = {bin(header_short[2 * 2 + 0])}")
	if (old_format):
		print(f"arch         = {hex(header_short[2 * 2 + 1])}")
	else:
		print(f"arch         = {hex(header_short[2 * 2 + 1] & 0xff)}")
		print(f"vfp          = {hex(header_short[2 * 2 + 1] >> 8)}")
	print(f"fixupOffset  = {hex(header[3])}")
	print(f"fixupSize    = {hex(header[4])}")
	print(f"codeOffset   = {hex(header[5])}")
	print(f"codeFileSize = {hex(header[6])}")
	print(f"codeMemSize  = {hex(header[7])}")
	print(f"sigOffset    = {hex(header[8])}")
	print(f"sigSize      = {hex(header[9])}")
	print(f"entryOffset  = {hex(header[10])}")
	print(f"configOffset = {hex(header[11])}")
	print(f"configSize   = {hex(header[12])}")
	print(f"baseAddrOrig = {hex(header[13])}")
	print(f"extraOffset  = {hex(header[14])}")
	print(f"extraSize    = {hex(header[15])}")
	
	# Extended header
	print(f"\n *** EXTENDED HEADER *** ")
	
	ext_length = memoryview(f.read(4)).cast("I")[0]
	print(f"extended header length = {hex(ext_length)}")
	print(f"hexdump of extended header:")
	print(hexdump(f.read(ext_length - 4)), end="")
	
	f.close()

if (__name__ == "__main__"):
	main()

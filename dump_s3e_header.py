#!/usr/bin/env python3
"""
Print out basic info about a uncompressed s3e's header
"""

import struct
import sys

def main():
	if (len(sys.argv) < 2):
		print(f"Usage: {sys.argv[0]} <s3e file>")
	
	f = open(sys.argv[1], "rb")
	mv = memoryview(f.read(0x40))
	header = mv.cast("I")
	header_short = mv.cast("H")
	f.close()
	
	print(f" *** BASIC HEADER *** ")
	print(f"ident        = {hex(header[0])}")
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

if (__name__ == "__main__"):
	main()

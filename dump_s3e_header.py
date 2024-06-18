#!/usr/bin/env python3
"""
Print out basic info about a uncompressed s3e's header
"""

import struct
import argparse

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
	parser = argparse.ArgumentParser()
	parser.add_argument("file", help="An uncompressed s3e file to parse")
	parser.add_argument("--fixup", help="Dump the section into a file", action="store_true")
	parser.add_argument("--config", help="Dump the section into a file", action="store_true")
	parser.add_argument("--code", help="Dump the section into a file", action="store_true")
	parser.add_argument("--extra", help="Dump the section into a file", action="store_true")
	parser.add_argument("--sig", help="Dump the section into a file", action="store_true")
	args = parser.parse_args()
	
	f = open(args.file, "rb")
	
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
	fixupOffset = header[3]
	fixupSize = header[4]
	codeOffset   = header[5]
	codeFileSize = header[6]
	codeMemSize  = header[7]
	sigOffset    = header[8]
	sigSize      = header[9]
	entryOffset  = header[10]
	configOffset = header[11]
	configSize   = header[12]
	baseAddrOrig = header[13]
	extraOffset  = header[14]
	extraSize    = header[15]
	print(f"fixupOffset  = {hex(fixupOffset)}")
	print(f"fixupSize    = {hex(fixupSize)}")
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
	ext_header = memoryview(f.read(ext_length - 4)).cast("I")
	# note: these are both in the code section, for some reason
	print(f"loaded code size       = {hex(ext_header[0])} ({ext_header[0]})")
	print(f"loaded data size       = {hex(header[6] - ext_header[0])} ({header[6] - ext_header[0]}) (implicit)")
	print(f"show splash screen     = {hex(ext_header[1])}")
	
	if (args.fixup):
		with open(f"{args.file}.fixup-dump", "wb") as g:
			f.seek(fixupOffset, 0)
			g.write(f.read(fixupSize))
	
	if (args.code):
		with open(f"{args.file}.code-dump", "wb") as g:
			f.seek(codeOffset, 0)
			g.write(f.read(codeSize))
	
	if (args.sig):
		with open(f"{args.file}.sig-dump", "wb") as g:
			f.seek(sigOffset, 0)
			g.write(f.read(sigSize))
	
	if (args.config):
		with open(f"{args.file}.config-dump", "wb") as g:
			f.seek(configOffset, 0)
			g.write(f.read(configSize))
	
	if (args.extra):
		with open(f"{args.file}.extra-dump", "wb") as g:
			f.seek(extraOffset, 0)
			g.write(f.read(extraSize))
	
	f.close()

if (__name__ == "__main__"):
	main()

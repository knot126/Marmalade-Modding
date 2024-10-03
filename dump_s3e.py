#!/usr/bin/env python3
"""
Print out basic info about a uncompressed s3e's header
"""

import struct
import argparse
from FileStream import FileStream

MAX_INTERNAL_RELOCS_TO_PRINT = 1024

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
	parser.add_argument("--fixup", help="Print contents of the relocaction information section (very large!)", action="store_true")
	parser.add_argument("--config", help="Print embedded icf", action="store_true")
	# parser.add_argument("--code", help="", action="store_true")
	# parser.add_argument("--extra", help="", action="store_true")
	# parser.add_argument("--sig", help="", action="store_true")
	args = parser.parse_args()
	
	f = FileStream(args.file, "rb")
	
	# Basic header
	s3e_magic = f.read(4)
	
	if (s3e_magic != b"XE3U"):
		print("Invalid s3e binary - maybe you need to decompress it first?")
		return
	
	f.setpos(0)
	s3e_ident = f.readUInt32()
	s3e_version = f.readUInt32()
	s3e_flags = f.readUInt16()
	s3e_arch = f.readUInt16()
	s3e_fixupOffset = f.readUInt32()
	s3e_fixupSize = f.readUInt32()
	s3e_codeOffset = f.readUInt32()
	s3e_codeFileSize = f.readUInt32()
	s3e_codeMemSize = f.readUInt32()
	s3e_sigOffset = f.readUInt32()
	s3e_sigSize = f.readUInt32()
	s3e_entryOffset = f.readUInt32()
	s3e_configOffset = f.readUInt32()
	s3e_configSize = f.readUInt32()
	s3e_baseAddrOrig = f.readUInt32()
	s3e_extraOffset = f.readUInt32()
	s3e_extraSize = f.readUInt32()
	
	# Extended header
	# TODO: Find out what versions use extended header and read based on that
	# instead of just guessing, though that works for now.
	s3e_extHeaderSize = f.readUInt32()
	s3e_dataOffset = None
	s3e_isJuice = None
	
	if (s3e_extHeaderSize == 0xc):
		# For some reason, the code section contains both code and data and the
		# extra header contains the size of the real code section itself
		s3e_dataOffset = f.readUInt32()
		s3e_isJuice = f.readUInt32()
	else:
		s3e_extHeaderSize = None
	
	print(f" *** BASIC HEADER *** ")
	print(f"ident        = {s3e_ident} ({s3e_magic.decode('latin-1')})")
	old_format = ((s3e_version >> 0x10) & 0xff) == 0
	
	if (old_format):
		print(f"version      = {hex(s3e_version)} ({s3e_version >> 12}.{s3e_version & 0xff})")
	else:
		print(f"version      = {hex(s3e_version)} ({s3e_version >> 16}.{(s3e_version >> 8) & 0xff}.{s3e_version & 0xff})")
	
	print(f"flags        = {bin(s3e_flags)} ({', '.join(interpret_s3e_flags(s3e_flags))})")
	
	if (old_format):
		print(f"arch         = {hex(s3e_arch)} ({interpret_s3e_arch(s3e_arch)})")
	else:
		print(f"arch         = {hex(s3e_arch & 0xff)} ({interpret_s3e_arch(s3e_arch)})")
		print(f"vfp          = {hex(s3e_arch >> 8)}")
	
	print(f"fixupOffset  = {hex(s3e_fixupOffset)}")
	print(f"fixupSize    = {hex(s3e_fixupSize)}")
	print(f"codeOffset   = {hex(s3e_codeOffset)}")
	print(f"codeFileSize = {hex(s3e_codeFileSize)}")
	print(f"codeMemSize  = {hex(s3e_codeMemSize)}")
	print(f"sigOffset    = {hex(s3e_sigOffset)}")
	print(f"sigSize      = {hex(s3e_sigSize)}")
	print(f"entryOffset  = {hex(s3e_entryOffset)}")
	print(f"configOffset = {hex(s3e_configOffset)}")
	print(f"configSize   = {hex(s3e_configSize)}")
	print(f"baseAddrOrig = {hex(s3e_baseAddrOrig)}")
	print(f"extraOffset  = {hex(s3e_extraOffset)}")
	print(f"extraSize    = {hex(s3e_extraSize)}")
	
	print()
	
	# TODO: Verify that s3e's without the extended header dont actually
	# distinguish between code and data sections.
	print(f"Section information:")
	print(f" - has a data section: {'yes' if s3e_dataOffset != None else 'no'}")
	
	if s3e_dataOffset != None:
		print(f" - code size = {hex(s3e_dataOffset)}")
		print(f" - data size = {hex(s3e_codeFileSize - s3e_dataOffset)}")
	else:
		print(f" - code + data size = {hex(s3e_codeFileSize)}")
	
	print(f" - bss size = {hex(s3e_codeMemSize - s3e_codeFileSize)} (implicit)")
	
	# Extended header
	if s3e_extHeaderSize != None:
		print(f"\n *** EXTENDED HEADER *** ")
		
		print(f"extended header length = {hex(s3e_extHeaderSize)}")
		print(f"data segment offset    = {hex(s3e_dataOffset)}")
		print(f"uses marmalade juice   = {hex(s3e_isJuice)}")
	
	# Print relocation information/fixups, if wanted
	if (args.fixup):
		symbols = []
		
		print("\n *** FIXUP CONTENTS *** ")
		f.setpos(s3e_fixupOffset)
		
		while (f.getpos() < s3e_fixupOffset + s3e_fixupSize):
			fixupSectionOffset = f.getpos()
			fixupSectionType = f.readUInt32()
			fixupSectionSize = f.readUInt32() - 8
			
			match fixupSectionType:
				case 0:
					symbolCount = f.readUInt16()
					
					print(f"Have {symbolCount} symbol names:")
					
					for i in range(symbolCount):
						newSymbol = f.readString()
						symbols.append(newSymbol)
						print(f" * [{i}] {newSymbol}")
				
				case 1:
					intRelocCount = f.readUInt32()
					
					print(f"Have {intRelocCount} internal relocations:")
					
					if (intRelocCount > MAX_INTERNAL_RELOCS_TO_PRINT):
						print("[too many internal relocs to print]")
					
					for i in range(intRelocCount):
						offset = f.readUInt32()
						if (intRelocCount <= MAX_INTERNAL_RELOCS_TO_PRINT):
							print(f" - {hex(offset)}")
				
				case 2 | 3 | 4: # These all look the same to me ... see IwS3ERead from iOS .o file
					extRelocCount = f.readUInt32()
					
					print(f"Have {extRelocCount} external relocs")
					
					for i in range(extRelocCount):
						hi = f.readUInt16()
						lo = f.readUInt16()
						offset = (hi << 16) | (lo)
						symbolIndex = f.readUInt16()
						
						print(f" + {hex(offset)} -> {symbols[symbolIndex]} ({symbolIndex})")
				
				case _:
					print(f"Skip unknown section type {fixupSectionType} of size {fixupSectionSize} at file pos {hex(f.getpos())}")
					f.read(fixupSectionSize)
			
			unreadBytes = fixupSectionOffset + fixupSectionSize + 8 - f.getpos()
			
			if (unreadBytes != 0):
				print(f"Note: still had {hex(unreadBytes)} unread bytes at end of section parsing...")
			
			f.setpos(fixupSectionOffset + fixupSectionSize + 8)
	
# 	if (args.code):
# 		with open(f"{args.file}.code-dump", "wb") as g:
# 			f.seek(codeOffset, 0)
# 			g.write(f.read(codeSize))
# 	
# 	if (args.sig):
# 		with open(f"{args.file}.sig-dump", "wb") as g:
# 			f.seek(sigOffset, 0)
# 			g.write(f.read(sigSize))
	
	if (args.config):
		print("\n *** CONFIG FILE *** ")
		# Not sure exactly what versions this quirk applies to
		if s3e_version < 0x1005:
			f.setpos(s3e_configOffset - s3e_configSize)
		else:
			f.setpos(s3e_configOffset)
		
		print(f.read(s3e_configSize).decode("latin-1"))
	
# 	if (args.extra):
# 		with open(f"{args.file}.extra-dump", "wb") as g:
# 			f.seek(extraOffset, 0)
# 			g.write(f.read(extraSize))
	
	f.close()

def interpret_s3e_flags(flags):
	KNOWN_FLAGS = ["debug", "gcc", "rvct", "pie", "64bit"]
	result = []
	
	for i in range(len(KNOWN_FLAGS)):
		if flags & (1 << i):
			result.append(KNOWN_FLAGS[i])
	
	return result

def interpret_s3e_arch(arch):
	return ["ARMv4t", "ARMv4", "ARMv5t", "ARMv5te", "ARMv5tej", "ARMv6", "ARMv6k", "ARMv6t2", "ARMv6z", "x86", "PPC", "AMD64", "x86_64", "ARMv7a", "ARMv8a", "ARMv8a-aarch64", "NACL-x86_64"][arch]

if (__name__ == "__main__"):
	main()

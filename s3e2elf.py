import struct
import sys
from FileStream import FileStream

def s3e2elf(input_path, output_path):
	input = FileStream(input_path, mode = "rb")
	# output = FileStream(output_path, mode = "wb")
	
	# Read some initial values from the s3e that we need
	if (input.read(4) != b"XE3U"):
		print("Invalid s3e binary, did you extract it first?")
		return
	
	s3e_version = input.readUInt32()
	s3e_flags = input.readUInt16()
	s3e_arch = input.readUInt16()
	s3e_fixupOffset = input.readUInt32()
	s3e_fixupSize = input.readUInt32()
	s3e_codeOffset = input.readUInt32()
	s3e_codeFileSize = input.readUInt32()
	s3e_codeMemSize = input.readUInt32()
	s3e_sigOffset = input.readUInt32()
	s3e_sigSize = input.readUInt32()
	s3e_entryOffset = input.readUInt32()
	s3e_configOffset = input.readUInt32()
	s3e_configSize = input.readUInt32()
	s3e_baseAddrOrig = input.readUInt32()
	s3e_extraOffset = input.readUInt32()
	s3e_extraSize = input.readUInt32()
	s3e_extHeaderSize = input.readUInt32()
	s3e_realCodeSize = 0
	s3e_extShowSplash = 0
	if (s3e_extHeaderSize == 0xc):
		# For some reason, the code section contains both code and data and the
		# extra header contains the size of the real code section itself
		s3e_realCodeSize = input.readUInt32()
		s3e_extShowSplash = input.readUInt32()
	

def main():
	if (len(sys.argv) < 3):
		print(f"Usage: {sys.argv[0]} <input s3e> <output elf>")
		sys.exit(1)
	
	s3e2elf(sys.argv[1], sys.argv[2])

if (__name__ == "__main__"):
	main()

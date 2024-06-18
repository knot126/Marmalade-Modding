import struct
import sys

class FileStream():
	"""
	Nice way to read binary files
	"""
	
	def __init__(self, path, mode = "r+b"):
		self.f = open(path, mode)
		self.endian = "<"
	
	def close(self):
		self.f.close()
	
	def read(self, n):
		"""Read n bytes"""
		
		return self.f.read(n)
	
	def write(self, b):
		"""Write bytes"""
		
		self.f.write(b)
	
	def getpos(self):
		return self.f.tell()
	
	def setpos(self, pos):
		self.f.seek(pos, 0)
	
	def readFormatted(self, fmt):
		fmt = f"{self.endian}{fmt}"
		return struct.unpack(fmt, self.read(struct.calcsize(fmt)))[0]
	
	def writeFormatted(self, fmt, val):
		fmt = f"{self.endian}{fmt}"
		self.write(struct.pack(fmt, val))
	
	def readInt8(self): return self.readFormatted("b")
	def readUInt8(self): return self.readFormatted("B")
	def readInt16(self): return self.readFormatted("h")
	def readUInt16(self): return self.readFormatted("H")
	def readInt32(self): return self.readFormatted("i")
	def readUInt32(self): return self.readFormatted("I")
	
	def writeInt8(self, val): self.writeFormatted("b", val)
	def writeUInt8(self, val): self.writeFormatted("B", val)
	def writeInt16(self, val): self.writeFormatted("h", val)
	def writeUInt16(self, val): self.writeFormatted("H", val)
	def writeInt32(self, val): self.writeFormatted("i", val)
	def writeUInt32(self, val): self.writeFormatted("I", val)

def s3e2elf(input_path, output_path):
	input = FileStream(input_path, mode = "rb")
	output = FileStream(output_path, mode = "wb")
	
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
	
	# read the fixup table
# 	input.setpos(s3e_fixupOffset)
# 	
# 	while (input.getpos() < s3e_fixupOffset + s3e_fixupSize):
# 		cmd = input.readUInt32()
# 		
# 		match cmd:
# 			case 0x0:
# 				unknown = input.readInt32()
# 				numberOfStrings = input.readInt16()
	
	# ELF header
	output.write(b"\x7FELF")
	
	# TODO: Make it work for stuff that's not armv6
	output.writeUInt8(1) # 32 bit
	output.writeUInt8(1) # little endian
	output.writeUInt8(1) # ELF v1
	output.writeUInt8(0x03) # linux
	output.writeUInt8(0) # zero in other libs so here too ig
	output.write(b"\x00" * 7) # padding
	output.writeUInt16(0x03) # dynamic object (methinks?)
	output.writeUInt16(0x28) # arm upto armv7
	output.writeUInt32(1) # version 1 (again)
	output.writeUInt32(s3e_baseAddrOrig + s3e_entryOffset) # Offset to entry point
	output.writeUInt32(0x34) # program header offset
	elf_sectionHeaderOffsetLocation = output.getpos()
	output.writeUInt32(0x0) # section header table offset (placeholder)

def main():
	if (len(sys.argv) < 3):
		print(f"Usage: {sys.argv[0]} <input s3e> <output elf>")
		sys.exit(1)
	
	s3e2elf(sys.argv[1], sys.argv[2])

if (__name__ == "__main__"):
	main()

import struct
import shutil
import gzip

class FileStream():
	"""
	Nice way to read binary files. Also transparently handles GZIP compressed
	files.
	"""
	
	def __init__(self, path, mode = "r+b", handle_gzip = False):
		self.f = open(path, mode)
		self.endian = "<"
		
		if (handle_gzip):
			if (mode != "rb"):
				raise ValueError("FileStream's transparent Gzip handling is only available in binary read mode.")
			
			if (self.read(2) == b"\x1f\x8b"):
				self.f = gzip.open(path, mode)
			else:
				self.setpos(0)
	
	def close(self):
		self.f.close()
	
	def isGzip(self):
		return type(self.f) == gzip.GzipFile
	
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
	
	def readFrom(self, pos, count):
		self.setpos(pos)
		return self.read(count)
	
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
	
	def readString(self):
		s = b""
		
		while (True):
			c = self.read(1)
			
			if (c == b"\x00"):
				break
			
			s += c
		
		return s.decode("latin-1")
	
	def writeInt8(self, val): self.writeFormatted("b", val)
	def writeUInt8(self, val): self.writeFormatted("B", val)
	def writeInt16(self, val): self.writeFormatted("h", val)
	def writeUInt16(self, val): self.writeFormatted("H", val)
	def writeInt32(self, val): self.writeFormatted("i", val)
	def writeUInt32(self, val): self.writeFormatted("I", val)

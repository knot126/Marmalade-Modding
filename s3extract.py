#!/usr/bin/python
"""
s3e (XE3U) and dz (DTRZ) archive extractor

Tested only on Bubble Mania v1.8.2.2 for Android
"""

import sys
import os
import json
import struct
import gzip # NOTE: You should use the modded version!
import zlib

class File:
	"""
	File wrapper
	"""
	
	def __init__(self, name, read_only = True, use_gzip = False):
		"""
		Initialise the file handler
		
		name: Path to the file to open
		read_only: TODO
		gzip: If the GZIP module should be used to open the file
		"""
		
		self.file = gzip.open(name, "rb") if use_gzip else open(name, "rb")
	
	def readBytes(self, count):
		"""
		Read count bytes from the file
		
		count: Number of bytes to read
		"""
		
		return self.file.read(count)
	
	def readString(self, end = b'\x00'):
		"""
		Read an 'end' terminated string
		
		end: The byte value to terminate on, NUL by default
		"""
		
		string = ""
		current = -1
		
		while (current != end):
			current = self.readBytes(1)
			
			if (current == end):
				break
			
			string += current.decode("utf-8")
		
		return string
	
	def readInt32(self):
		"""
		Read a signed 32-bit little endian integer at the current position.
		"""
		
		return struct.unpack('<i', self.readBytes(4))[0]
	
	def readUInt32(self):
		"""
		Read an unsigned 32-bit little endian integer at the current position.
		"""
		
		return struct.unpack('<I', self.readBytes(4))[0]
	
	def readInt16(self):
		"""
		Read a signed 16-bit little endian integer at the current position.
		"""
		
		return struct.unpack('<h', self.readBytes(2))[0]
	
	def readUInt16(self):
		"""
		Read an unsigned 16-bit little endian integer at the current position.
		"""
		
		return struct.unpack('<H', self.readBytes(2))[0]
	
	def verifyHeader(self, header):
		"""
		Check that the bytes in 'header' are equal to the next bytes in the
		stream.
		
		header: The header to check against
		"""
		
		return (self.readBytes(len(header)) == header)
	
	def getCompressedData(self, offset, length):
		"""
		Get a gzip-compressed file from a specific offset in the data stream
		
		offset: The offset to the gzip
		length: Length of the data to read, MUST be fully matching becuase of
		        python's not handling things well.
		"""
		
		# HACK: Fix an issue
		if (length < 0):
			length = -1
		
		# Get old position
		position = self.file.tell()
		
		# Seek to part with gzip file
		self.file.seek(offset, 0)
		
		# Read the gzip file
		data = self.readBytes(length)
		
		## If there is a second gzip file terminate here
		#next_start = data.find(b"\x1f\x8b\x08\x00", 9)
		
		## Remove excess data
		#data = data[0 : next_start if next_start >= 0 else len(data)]
		
		#print(f"ungzip: {hex(length)} {hex(next_start)}")
		
		try:
			data = gzip.decompress(data)
		except EOFError as e:
			print(e)
		
		self.file.seek(position)
		
		return data
	
	def close(self):
		"""
		Close the file
		"""
		
		self.file.close()
	
	def __del__(self):
		"""
		Destroy the file
		"""
		
		self.close()

def writeBytesToFile(filename, content):
	"""
	Write some bytes to a file
	"""
	
	f = open(filename, "wb")
	f.write(content)
	f.close()

def extract_s3e(input, output):
	"""
	S3E file extraction
	"""
	
	f = File(input, use_gzip = True)
	
	if (not f.verifyHeader(b"XE3U")):
		print("Error: This file is not a valid XE3U (*.s3e) archive.")
		return
	
	print(f"Dummy value 1: {f.readBytes(4)}")
	
	file_count = f.readUInt32()
	archive_size = f.readUInt32()
	
	print(f"File count: {file_count}\nArchive size: {archive_size}")

def extract_dz(input, output):
	"""
	DZ file extraction
	"""
	
	f = File(input)
	
	if (not f.verifyHeader(b"DTRZ")):
		print("Error: This file is not a valid DTRZ (*.dz) archive.")
		return
	
	file_count = f.readUInt16()
	unknown_bytes = f.readBytes(3) # I think the last byte is a 0 length string
	
	print(f"File count: {file_count}")
	print(f"Next three unknown bytes: {unknown_bytes}")
	
	# Read file names
	filenames = []
	
	for i in range(file_count):
		filenames.append(f.readString())
	
	# HACK
	# 
	# We have to read another string because this format doesn't handle
	# subdirectories properly. This is a hack that will only work for Bubble
	# Mania and maybe other things. Should probably look in bundled.txt before
	# this hack, but this works for now.
	f.readString()
	
	# Read file attributes (don't know what any of this does, attributes is just a guess)
	attributes = []
	
	for i in range(file_count):
		attributes.append(f.readBytes(6))
	
	# Read lengths header (not sure what everything is)
	unknown_bytes_length = f.readBytes(2)
	lengths_count = f.readUInt16()
	
	print(f"Unknown bytes (length): {unknown_bytes_length}")
	print(f"Lengths count: {lengths_count}")
	
	# Read lengths (and extra data)
	lengths = []
	
	for i in range(file_count):
		offset = f.readUInt32() # Hard offset to the file (seeking here is the file)
		length0 = f.readUInt32() # Length of the file
		length1 = f.readUInt32() # Length of the file again
		eight = f.readUInt32() # Literal value eight
		
		# HACK/FORMAT NOTE
		# 
		# It's likely one of the lengths was meant for uncompressed size but
		# they just decided it was okay to do both since the extra bit at the 
		# end and it wouldn't affect getting the files due to having the literal
		# offsets. This could be an eventual issue though...
		# 
		# EDIT: Yes, it was an issue. So instead we use the offsets to
		# calculate the actual file sizes.
		
		lengths.append((offset, length0, length1, eight))
	
	# HACK
	# 
	# Append an extra length for the end of the file so it doesn't crash
	lengths.append((0x0, 0xfffffff, 0x0, 0x8))
	
	# Write the files now that we have their data
	for i in range(file_count):
		# Get file name
		filename = filenames[i]
		
		# Use the difference between the offsets so gzip doesn't go insane
		data = f.getCompressedData(lengths[i][0], lengths[i + 1][0] - lengths[i][0])
		
		# Write file out
		writeBytesToFile(output + "/" + filename, data)
	
	# print some metadata
	for i in range(file_count):
		print(f"File: '{filenames[i]}' {attributes[i]} {lengths[i]}")

def extract(input, output):
	"""
	Find the format of the file and extract it (.s3e or .dz)
	"""
	
	f = File(input)
	
	header = f.readBytes(4)
	
	f.close()
	
	if (header == b"DTRZ"):
		extract_dz(input, output)
	elif (header == b"\x1f\x8b\x08\x00"):
		extract_s3e(input, output)
	else:
		print("Could not detect archive type.")

def main():
	input = sys.argv[1]
	output = sys.argv[2]
	
	extract(input, output)

if (__name__ == "__main__"):
	main()

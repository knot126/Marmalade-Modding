#!/usr/bin/python
"""
dz (DTRZ) archive extractor

Tested only on Bubble Mania v1.8.2.2 for Android
"""

import sys
import os
import json
import struct
import gzip # NOTE: You should use the modded version!
import zlib
from pathlib import PurePath

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

def extract_dz(input, output):
	"""
	DZ file extraction
	"""
	
	f = File(input)
	
	# Verify the header
	if (not f.verifyHeader(b"DTRZ")):
		print("Error: This file is not a valid DTRZ (*.dz) archive.")
		return
	
	# Read rest of header
	file_count = f.readUInt16()
	folder_count = f.readUInt16() - 1 # Number of strings to skip at the end
	assert(f.readBytes(1) == b'\x00') # Unused string (?)
	
	print(f"File count: {file_count}")
	print(f"Folder count: {folder_count}")
	
	# Read file names
	filenames = []
	
	for i in range(file_count):
		filenames.append(f.readString())
	
	# Read folder names (index zero is root)
	folders = [""]
	
	for i in range(folder_count):
		folder_name = f.readString()
		folders.append(folder_name)
		
		print(f"Folder: [{i + 1}] = '{folder_name}'")
	
	# Create output folder structure
	os.makedirs(output, exist_ok = True)
	
	for fname in folders:
		os.makedirs(output + "/" + fname, exist_ok = True)
	
	# Read file attributes (don't know what any of this does, attributes is just a guess)
	attributes = []
	
	for i in range(file_count):
		folder = f.readUInt16() # The folder index
		number = f.readUInt16() # The number of the file, starting from zero
		flags = f.readUInt16() # Not really known but probably flags
		attributes.append((folder, number, flags))
	
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
		# TODO: Probably make this work properly
		data = f.getCompressedData(lengths[i][0], lengths[i + 1][0] - lengths[i][0])
		
		# Write file out
		writeBytesToFile(output + "/" + folders[attributes[i][0]] + "/" + filename, data)
	
	# print some metadata
	for i in range(file_count):
		print(f"File: [{i}] = name '{filenames[i]}' flags {hex(attributes[i][2])} at {lengths[i]}")
	
	# write a dcl
	dcl = open(f"{output}.dcl", "w")
	dcl.write(f"archive {str(PurePath(input).name)}\n")
	dcl.write(f"basedir {str(PurePath(output).name)}\n\n")
	
	for i in range(file_count):
		dcl.write(f"file {(folders[attributes[i][0]] + '/' if folders[attributes[i][0]] else '') + filenames[i]} 0 zlib\n")
	
	dcl.close()

def extract(input, output):
	"""
	Find the format of the file and extract it (.s3e or .dz)
	"""
	
	f = File(input)
	
	header = f.readBytes(4)
	
	f.close()
	
	if (header == b"DTRZ"):
		extract_dz(input, output)
	else:
		print("Could not detect archive type.")

def main():
	if (len(sys.argv) != 3):
		print(f"Usage: {sys.argv[0]} <INPUT DZ> <OUTPUT DIR>")
		exit(127)
	
	input = sys.argv[1]
	output = sys.argv[2]
	
	extract(input, output)

if (__name__ == "__main__"):
	main()

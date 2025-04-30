#!/usr/bin/env python3
"""
Split a .group.bin into the individual binary assets

Note: Only tested on .group.bin format version 3.7.2

Maybe this is also helpful? https://github.com/clanner/simcitybuildit
"""

import sys, os
from pathlib import Path
from FileStream import FileStream

def split_group(path):
	print(f"=> {path}")
	
	f = FileStream(path, "rb")
	output_dir = path.removesuffix(".group.bin")
	os.makedirs(output_dir, exist_ok=True)
	
	# From: IwResSerialise.h
	if f.readUInt8() != 0x3d:
		print("Invalid magic; is this group binary compressed or encrypted?")
		sys.exit(1)
	
	print("Group Binary Header")
	print(f"Major: {f.readUInt8()}")
	print(f"Minor: {f.readUInt8()}")
	print(f"Rev: {f.readUInt8()}")
	# Found via: iwresmanager_d.lib/IwResSerialise.obj/IwResBinarySerialiseHeader
	# Appears to apply only to group bin's > 3.1.1
	print(f"Mystery number (???): {f.readUInt16()}")
	print()
	
	while True:
		name_hash = f.readUInt32()
		
		if name_hash == 0:
			print("Group Binary Terminator")
			if f.read(1) != b'':
				print("WARNING: THERE IS STILL UNREAD DATA IN THE FILE!!")
			break
		
		size = f.readUInt32()
		
		print("Binary Block")
		print(f"Block Name Hash: {name_hash:08x}")
		print(f"Block Size: {size} ({hex(size)})")
		print()
		
		# Found by trial and error with iwgxfontbrowser.group.bin from Tone
		# Sphere APK, not sure why its four specifically...
		data = f.read(size-4)
		
		Path(f"{output_dir}/{name_hash:08x}").write_bytes(data)
	
	f.close()

def main():
	if len(sys.argv) < 2:
		print(f"Usage: {sys.argv[0]} [.group.bin files ...]")
	else:
		for group_name in sys.argv[1:]:
			split_group(group_name)

if __name__ == "__main__":
	main()

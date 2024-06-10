import sys

# Patches the function that returns 1 if sig checking is enabled / 0 if not
# to return zero on android.
# only works for one specific version of libs3e_android.so right now

def main():
	if (len(sys.argv) < 2):
		print(f"Usage: {sys.argv[0]} <path to libs3e_android.so>")
	
	f = open(sys.argv[1], "r+b")
	f.seek(0x2496c, 0)
	f.write(b"\x00\x00\xa0\x13")
	f.close()
	
	print("patched!")

if __name__ == "__main__":
	main()

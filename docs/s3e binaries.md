# S3E Binaries

S3E binaries contain game code in a custom binary format.

## Format

### Header

Taken from log messages left over in `libs3e_android.so`.

```c
struct s3eHeader {
	int ident;
	int version;
	int flags;
	int arch;
	int fixupOffset;
	int fixupSize;
	int codeOffset;
	int codeFileSize;
	int codeMemSize;
	int sigOffset;
	int sigSize;
	int entryOffset;
	int configOffset;
	int configSize;
	int baseAddrOrig;
	int extraOffset;
	int extraSize;
};
```

This seems to be followed by the extended header.

### Extended Header

Starts with an `int` for the size of ext. header.

## See also

* https://web.archive.org/web/20160513163557/http://docs.madewithmarmalade.com/display/MD/Exploring+Marmalade's+architecture

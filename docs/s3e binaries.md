# S3E Binaries

S3E binaries contain game code in a custom binary format.

## Format

### Header

Taken from log messages left over in `libs3e_android.so`.

```c
struct s3eHeader {
	int ident;
	int version;
	short flags;
	short arch;
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

Note: If `(version >> 16) & 0xff` is not zero then the format is slightly different to accomidate for platforms that have an optional vector floating point unit. More specifically, it is:

This seems to be followed by the extended header.

### Extended Header

Starts with an `int` for the size of ext. header.

## See also

* https://web.archive.org/web/20160513163557/http://docs.madewithmarmalade.com/display/MD/Exploring+Marmalade's+architecture

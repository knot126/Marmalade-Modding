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

If `(version >> 16) & 0xff` is not zero then version is `major.minor.patch` (major << 16 | minor << 8 | patch), arch is actually `arch & 0xff` and `arch >> 8` stores if the app requires a floating point unit. In the other case, the version is `major.minor` (major << 8 | minor) and arch is the actual arch value.

Note that the code section is actually split into the actual code section and the data section. The extended header contains the size of the actual code section.

This seems to be followed by the extended header.

### Extended Header

```c
struct s3eExtendedHeader {
	int extHeaderSize; // size of extended header
	int realCodeSize; // offset of the data section relative to code section start
	int unknown2; // Seems like it only controls if an app splash is shown on startup
};
```

## Fixup table format

## See also

* https://web.archive.org/web/20160513163557/http://docs.madewithmarmalade.com/display/MD/Exploring+Marmalade's+architecture

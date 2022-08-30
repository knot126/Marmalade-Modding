# Dzip format info

*2022-08-30 -- First draft*

**Dzip** (`*.dz`) archives are used in some mobiles games.

## Format

There are three main data parts to a Dzip archive:

 1. The file (and subfolder) name strings.
 2. The file attributes.
 3. The file location information.

### Header

The first header is 9 bytes.

| Offset | Purpose | Type | Example | More info |
| ------ | ------- | ---- | ------- | --------- |
| `0x0` | Identifier | `char[4]` | `"DTRZ"` | The magic header for Dzip archives |
| `0x4` | File count | `uint16_t` | `1f 00` | The number of files in the archive |
| `0x6` | Folder count | `uint16_t` | `02 00` | The number of folders in the archive, including the root folder |
| `0x8` | N/A | `char[1]` | `00` | Not really known, but probably the string that is supposed to represent the root folder |

### File names

File names are stored as `NUL`-terminated strings one after another. For example: `one\0two\0three\0` where `\0` is `NUL`.

The strings are implicty stored in the order that their other properties and info will appear in. For example, the 503rd string (counting from zero) will go to the file that has the 503rd attribute record and the 503rd location information record.

After the file names, there are strings for the names of each of the subfolders in the archive, not including the root folder (since that would just be a NUL byte).

### File attributes

The next thing that is stored in the file is the file attributes. There is one file attribute record per file. There is no header, but the following structure:

| Offset | Purpose | Type | Example | More info |
| ------ | ------- | ---- | ------- | --------- |
| `0x0` | Folder | `uint16_t` | `01 00` | The number index of the folder that this file is in, zero is the root folder. |
| `0x2` | Index | `uint16_t` | `0b 00` | The index of the file, counting from zero |
| `0x4` | N/A | `uint16_t` | `ff ff` | Probably used for flags |

### Location information header

The header for the location information is 4 bytes.

| Offset | Purpose | Type | Example | More info |
| ------ | ------- | ---- | ------- | --------- |
| `0x0` | N/A | `bytes` | N/A | Unknown |
| `0x2` | File count | `uint16_t` | `1f 00` | The number of files |

### Location information

The location information records are also kind of messy, at least from the games I have looked at.

| Offset | Purpose | Type | Example | More info |
| ------ | ------- | ---- | ------- | --------- |
| `0x0` | Offset | `uint32_t` | `40 1f 00 00` | The offset to the compressed data |
| `0x4` | Size | `uint32_t` | `20 0c 00 00` | The size of the data |
| `0x8` | Size | `uint32_t` | `20 0c 00 00` | The size of the data (again) |
| `0xc` | N/A | `uint32_t` | `08 00 00 00` | Not known, but possibly the compression method |

One of the sizes is likely meant to store the compressed size, and the other is likely meant to store the uncompressed size. Many archive formats do this to make sure that memory allocation is done as little as possible.

However, it seems like the final archiver tool does not respect this and uses the uncompressed size for the data, since doing that doesn't really have much bad effect (aside from being ugly).

### Data

Following the headers is the compressed data itself, usually stored in the same order as the file names, though it probably doesn't need to be.

Compressed data can be stored in many formats, so for now I just assume it's using gzip or similar.

## More info

See [README from dzip.txt](README from dzip.txt) for info on compression formats from the official archiving tool.

# Cracking Marmalade Components

Note: Patches are in the form:

\<offset into binary\> \<byte 0, byte 1, byte 2, etc.\>

## Individual component patches

### tools/hub2/hub2.exe

The hub makes a `POST` request to `https://www.madewithmarmalade.com/verify-user`, which responds with the string `valid`, `incomplete` or `invalid`. It seems to be enough to just respond with `valid`.

### s3e/win32/s3e_qemu.exe

Apply this patch to ignore bad license statuses:

```
A6BE4  EB
A6E46  EB
```

### s3e/bin/s3e_plink.exe

Apply this patch to skip license check:

```
b140  b8 00 00 00 00 c3
```

Note the linker still requires a valid license file to embed in the s3e.

## License file format

License files live in `C:\Users\%USER%\AppData\Roaming\Marmalade\license\`.

There are seemingly three main files: `iwlicense.lic` and `license.data`.

### license.data

Seems to contains the key and a user ID, like this:

```
Key:<key>
User:<username>
```

> NOTE: Due to the IndexOfString method used the `Key:` and `User:` strings might need to be at index > 0.

When creating a demo this is set to:

```
 # Marmalade Trial, Remaining=<number of days remaining>

```

or:

```
 # Marmalade Trial.

```

### iwlicense.lic

When creating a demo license this gets set to:

```
LICENSE demo marmaladesdk 1.0 permanent uncounted hostid=any options={Type=Evaluation;LicPlat=NONE;Ftrs=Juice,DBG;}
```

## RLM note

There are many references to Reprise License Manager, which appears to be an extral license management solution: https://en.wikipedia.org/wiki/Reprise_License_Manager

See: https://blog.jackeylea.com/rlm/intro-of-reprise-license-manager/

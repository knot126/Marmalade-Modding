# Marmalade SDK modding

Some misc. utilities made while modding games made with the Marmalade SDK. You can probably find better tools online.

## Tools

* `dump_s3e.py`: Dump information about an S3E executable, including headers, the embedded config and relocation information.
* `dzextract.py`: Tries to extract a `.dz` archive and generate a DZip configuration file. There is only limited support ATM, so using the official `dzip.exe` is recommended.
* `disable_sig_check.py`: Really basic script to patch out signature verification. Only works with Marmalade loader v4.40.0.

## Ghidra S3E loader

An really really really [exprimental S3E loader](https://github.com/knot126/S3ELoader) for Ghidra is also available. You will need to compile it yourself for now!

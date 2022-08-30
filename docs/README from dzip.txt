dzip command line parameters:

dzip <options> <config_file>
where <options> are zero or more of:
  --waitatend (-w)              pause for a keypress before exiting
  --help (-h)                   print this message then exit
  --license (-L)                print the license message then exit
  --version (-V)                print the version information then exit
  --quiet (-q)                  no output
  --verbose (-v)                extended output
  --command (-c) "<command>"    extra commands (in .dcl file format)
  --decompress (-d)             Extract compressed dzip file to subdirectory
  --list (-l)                   List compressed dzip file contents
  --dir (-D) <dir>              add base dir
  --align (-A) <num>            align to <num> byte boundary
or
dzip <options> [-a|--archive <archive_file> [<files>|<file_options>]*]+
where <options> are as above and file_options are one or more of
  --type (-t) <type>            compression type: dz, zlib, bzip, zero or copy
  --start (-s) <num>[%]         previous file starts at num
  --end (-e) <num>[%]           previous file ends at num

Derbh config file format:
archive <archive_name>          file to export to (archive_name is relative to
                                config file) (first archive file contains
                                file/dir info)
master <filename>               include base file with common settings
basedir <dir>                   files are stored relative to this (there can be
                                multiple basedir's)
align <size>                    align to this boundary
file <path> <archive> <flags>   file to add to export (relative to basepath)
                                where archive is the archive file to go in and
                                flags is one or more of:
        dz            use dz compression
        zlib          use zlib compression
        bzip          use bzip compression
        zero          zero out the data
        copy          copy with no compression
        from <num>[%] start offset (optionally as a percentage)
        to <num>[%]   end offset (optionally as a percentage)

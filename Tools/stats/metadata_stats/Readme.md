### Metadata QA scripts
This directory contains necessary files to print some stats for a metadata files. The main file is `print_metadata_stats.py` and rest of the files contain supporting functions.

#### Usage

```
print_metadata_stats.py --help
usage: print_metadata_stats.py [-h] metadata_file

Print's info from metadata file(s)

positional arguments:
  metadata_file  Filename or Dir

optional arguments:
  -h, --help     show this help message and exit
```
You can specify a specific metadata file or a directory containing metadatafiles. 

Ex: `print_metadata_stats.py . | tee metastats.txt`



# PyGL FoV Agent Scripts

## PyGLFoVAgent Directory Calculator

This script allows a user to calculate FoV messages for all metadata files in a provided directory, and write the resulting metadata files to a second directory.  The script assumes that the input metadata files end in `.metadata` and will write the output metadata files with the same name (so it's important not to pass the same directory as input and output directories!).

If the output directory does not exist, the script will create the needed directories in the path.

The script will spawn multiple processes to calculate metadata files, with each process handling a single metadata file.  The number of processes / CPUs to use can be controlled with the `--num_cpu` command-line argument.

### Usage
python calculate_directory <input_path> <output_path> [num_cpu]

#### Command Line Arguments

* input_path
    * the path to the directory containing the metadata files to compute the FoV messages for
* output_path
    * the path to write generated FoV messages to
* num_cpu (optional)
    * the (maximum) number of CPUs / processes to run in parallel.


## PyGLFoVAgent Metadata Merge

This script allows a user to merge metadata files with corresponding FoV metadata files, and write the results to a third metadata file.  The script assumes that the metadata and FoV files are named the same, are in two separate directories, and end in `.metadata`.  Only FoV Summary messages will be merged.  The output metadata file will be written to a third directory, with the same name as the original and FoV metadata files.

The FoV messages will be interleaved so that an FoV message immediately follows the corresponding PlayerState message.

### Usage
python merge_metadata.py <input_path> <fov_path> <output_path> [num_cpu]

#### Command Line Arguments

* input_path
    * the path to the directory containing the original metadata files
* fov_path
    * the path to the directory containing the FoV metadata files
* output_path
    * the path to write merged metadata to
* num_cpu
    * the (maximum) number of CPUs / processes to run in parallel.


## PyFoVAgent QC Script

This script performs quality checking on metadata files expected to contain PyGLFoV messages.  Specifically, the script checks for and reports on the following:

* Total number of PlayerState and FoV messages in the metadata file
* Time range (in mission time) that FoV messages were generated
* Number of FoV messages by player
* Statistics on latency between PlayerState and FoV messages
* Time delta between subsequent FoV messages by player

At the moment, the results are simply printed to stdout.


### Usage

python qc_pyglfov.py <inputfile>
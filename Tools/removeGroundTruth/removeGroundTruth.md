## Tool: removeGroundTruth
### Description
removeGroundTruth.py is a python script which removes ground truth from .metadata files.  
### Usage
This tool can be run on a directory or metadata files and it will remove the ground truth from each file and create a new file with the ground truth remove.
The output file with the ground truth removed will have the version number incremented by 1 from the corresponding input file.
The ground truth is removed from the following records:
- the client map property in the trial start and trial end messages for each participant
- the entire measure message
### Command line arguments
- -i the path for the directory which contains all of the .metadata files which will be processed
- -o the path for the output directory where all of the cleaned files should be written.

"""
PyGLFoVAgent Directory Calculator

This script allows a user to calculate FoV messages for all metadata files in
a provided directory, and write the resulting metadata files to a second
directory.  The script assumes that the input metadata files end in `.metadata`
and will write the output metadata files with the same name (so it's important
not to pass the same directory as input and output directories!).

If the output directory does not exist, the script will create the needed
directories in the path.

The script will spawn multiple processes to calculate metadata files, with each
process handling a single metadata file.  The number of processes / CPUs to use
can be controlled with the `--num_cpu` command-line argument.

Usage
-----
python calculate_directory <input_path> <output_path> [num_cpu]

Command Line Arguments
----------------------
input_path : string
	The path to the directory containing the metadata files to compute the FoV
	messages for
output_path : string
	The path to write generated FoV messages to
num_cpu : integer, optional
	The (maximum) number of CPUs / processes to run in parallel.
"""

import multiprocessing as mp 
import argparse
import os

"""
Command template to execute the PyGLFoVAgent on a single metadata file
"""
PYGLFOV_COMMAND = 'python src/PyGLFOVAgent.py ConfigFolder/config.json -i %s -o %s'

def parse_arguments():
	"""
	Parse the command line arguments and return a Namespace instance with the
	argument contents
	"""

	parser = argparse.ArgumentParser(description="Calculate FoV messages from a directory of metadata files.")
	parser.add_argument('input_path', help='path to the directory containing input metadata files.')
	parser.add_argument('output_path', help='path to write FoV metadata files to.')
	parser.add_argument('-n', '--num_cpu', type=int, default=None, help='number of parallel processes to run.')

	args = parser.parse_args()

	print("Arguments")
	print("---------")
	print("Input Path: ", args.input_path)
	print("Output Path: ", args.output_path)
	print("Number of CPUs: ", args.num_cpu)

	return args


def run_agent(input_file_path, output_file_path):
	"""
	Run the PyGLFoVAgent on a single file.

	Arguments
	---------
	input_file_path : string
		Path to the input metadata file
	output_file_path : string
		Output metadata file
	"""

	cmd = PYGLFOV_COMMAND % (input_file_path, output_file_path)
	os.system(cmd)


def run(input_path, output_path, num_processes = None):
	"""
	Run the PyGLFoVAgent on the files in the given directory.  Only files 
	ending in `.metadata` will be processed.  FoV files will be written with
	the same filename

	Arguments
	---------
	input_path : string
		Path to the directory containing metadata files to process
	output_path : string
		Path to write FoV metadata files to after processing
	"""

	# Check to see if the output path exists, and create if it doesn't
	if not os.path.isdir(output_path):
		os.makedirs(output_path)

	# Process all the files -- create a list of input/output tuples, and then
	# use a process pool to process the pairs asynchronously
	input_output_pairs = []

	for filename in os.listdir(input_path):

		# Only process files ending in `.metadata`
		if filename.endswith('.metadata'):

			input_file_path = os.path.join(input_path, filename)
			output_file_path = os.path.join(output_path, filename)

			input_output_pairs.append((input_file_path, output_file_path))

	# If the number of processes isn't given, or is zero or negative, use all
	# the CPUs available
	if num_processes is None or num_processes < 1:
		num_processes = mp.cpu_count()

	# Create a pool of processes and perform the calculations.  Since the
	# processes don't return anything, using an async mapping should be the
	# most efficient, and not requrire any additional overhead.
	pool = mp.Pool(num_processes)
	_ = pool.starmap_async(run_agent, input_output_pairs)
	pool.close()
	pool.join()


if __name__ == '__main__':
	"""
	Main entry point for the script
	"""

	args = parse_arguments()
	run(args.input_path, args.output_path, args.num_cpu)






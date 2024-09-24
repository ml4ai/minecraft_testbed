#!/bin/bash

echo "Running PyGLFoVAgent from a metadata file"

if [[ "$#" -ne 3 ]]; then
	echo "USAGE: sh fov_from_file.sh <config_path> <input_path> <output_path>"
	exit 1
fi

echo "  Config Path: $1";
echo "  Input Path: $2";
echo "  Output Path: $3";

# Invoke the agent
python3 src/PyGLFOVAgent.py $1 -i $2 -o $3

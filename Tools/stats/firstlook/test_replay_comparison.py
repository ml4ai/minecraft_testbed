import argparse
import os
import argparse
import pytest

def test_same_file(file1):
    command_1 = 'python firstlook_file.py -r -f {}'.format(file1)

    process_1 = os.popen(command_1)
    output_1 = process_1.read()
    process_1.close()
    
    process_2 = os.popen(command_1)
    output_2 = process_2.read()
    process_2.close()
    
    assert output_1 == output_2

def test_different_files(file1, file2):
    command_1 = 'python firstlook_file.py -r -f {}'.format(file1)
    command_2 = 'python firstlook_file.py -r -f {}'.format(file2)

    process_1 = os.popen(command_1)
    output_1 = process_1.read()
    process_1.close()
    
    process_2 = os.popen(command_2)
    output_2 = process_2.read()
    process_2.close()
    
    assert output_1 == output_2

def test_file_length(file1, file2):
    count_1 = sum(1 for line in open(file1))
    count_2 = sum(1 for line in open(file2))
    assert count_1 == count_2

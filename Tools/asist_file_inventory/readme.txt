Readme:
Purpose: Takes a ls (not ls -l) of filenames and a standard for number of filename parts (e.g., 8 parts) separated by "_". Reports (1) team, trial, and count of each filetype, as well as (2) filenames that do not conform to the standard of number of parts
See examples below, run asist_file_inventory.py for help text, read the head of asist_file_inventory.py

Command for study-2 ls of GCS files
python asist_file_inventory.py 8 2 ls_study-2.txt >file_inventory_study-2.txt

Command for study-3_sprint-1 ls of GCS files
python asist_file_inventory.py 8 2 ls_study-3_sprint-1.txt >file_inventory_study-3_sprint-1.txt

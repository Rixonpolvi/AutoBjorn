#!/usr/bin/env python3.7

# run from root project directory
# edits Examples/test_input.csv rows with absolute paths
# runs autoBjorn.py with test_input_absolute.csv
# output to Example/test_output.csv

from pathlib import Path
import csv
import os

bjorn_path = Path('autobjorn/autoBjorn.py').absolute()
input_path = Path('Examples/test_input.csv').absolute()

if not input_path.exists():
    bjorn_path = Path('../autobjorn/autoBjorn.py').absolute()
    input_path = Path('../Examples/test_input.csv').absolute()

test_input_absolute = input_path.parent / 'test_input_absolute.csv'
output_path = input_path.parent / 'test_output.csv'

with open(input_path, 'r') as inputcsv, open(test_input_absolute, 'w', newline='') as outputcsv:
    reader = csv.reader(inputcsv, delimiter=',')
    next(reader, None)
    
    writer = csv.writer(outputcsv)
    writer.writerow(('image1', 'image2'))

    for row in reader:
        image1 = input_path.parent / row[0]
        image2 = input_path.parent / row[1]
        writer.writerow((image1, image2))


os.system(f'python {bjorn_path} {test_input_absolute} -o {output_path}')

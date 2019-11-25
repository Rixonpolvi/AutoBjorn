#!/usr/bin/env python3.7

# AUTOBJORN 1.0

from PIL import Image
from pathlib import Path
from skimage import metrics
import argparse
import logging
import requests
import csv
import time
import cv2
import sys


# Get local version from CHANGES.txt
# Get most recent version from CHANGES.txt in github
# Compare and notify if update exists
def check_version():

    # Get local version
    version_file = 'CHANGES.txt'

    with open(version_file, 'r') as file:
        data = file.read().split('\n')

        if not data[-1]:
            local_version = data[-2].split(',')[0]
        else:
            local_version = data[-1].split(',')[0]
    
    # Get remote version
    url = 'https://raw.githubusercontent.com/Rixonpolvi/AutoBjorn/master/CHANGES.txt'

    try:
        r = requests.get(url)

        if r.status_code == 200:
            version_info = r.text
            versions = version_info.split('\n')

            if not versions[-1]:
                latest_version = versions[-2].split(',')[0]
            else:
                latest_version = versions[-1].split(',')[0]
            
        else:
            logging.info('Version check failed - remote check unsuccessful')

    except requests.exceptions.HTTPError as e:
        print(f'Version check failed - {e}')
        logging.info(f'Version check failed - {e}')

    if local_version != latest_version:
        print(f'Update is available - {local_version} -> {latest_version}')
        logging.info(f'Update is available - {local_version} -> {latest_version}')
    logging.info(f'Version - {local_version}')


# Arguments
# input file
# Optional output file
def parse_arg():
    default_outfile = 'output.csv'

    parser = argparse.ArgumentParser(description='AutoBjorn image comparison')
    parser.add_argument('infile', type=str, help='Input CSV file')
    parser.add_argument('-o', '--outfile', type=str, help='Output CSV file', default=default_outfile)

    args = parser.parse_args()

    print(f'Input file - {args.infile}')
    print(f'Output file - {args.outfile}')

    return args


# Structural Similarity Index (SSI)  --> -1 to 1 (Different to same)
# Bjorn Similarity Index (BSI)       -->  0 to 1 (Same to different)
# Normalize [-1,1] --> [1,0] and subtract from 1 to flip
# new = 1 - (old - min/max - min)
# new = 1 - (old - -1/1 - -1)
def normalize(ssi):
    return (1 - (ssi + 1) / 2)


# Compare 2 image files
# Return ssi value and time taken
def compare_images(imageA, imageB):
    ssi_start = time.time()
    ssi = metrics.structural_similarity(imageA, imageB, multichannel=True)
    ssi_finish = time.time()
    ssi_time = ssi_finish - ssi_start
    
    return ssi, ssi_time


# Load images for comparison
# .gif not working with opencv
# image converstion using pillow.Image
def load_image(path):
    if path.suffix == '.gif':
        convert_to_png = path.parent / path.stem
        Image.open(path).save(f'{str(convert_to_png) + "_tmp"}.png', 'PNG')
        image = cv2.imread(f'{str(convert_to_png) + "_tmp"}.png', 1)
    else:
        image = cv2.imread(str(path), 1)
    return image 


# Read from args.infile
# Write to args.outfile
# N/A values if images do not exist on the filesystem
def read_write(args):
    completed = 0
    failures = 0

    with open(args.infile, 'r') as inputcsv, open(args.outfile, 'w', newline='') as outfile:
        reader = csv.reader(inputcsv, delimiter=',')
        next(reader,None)
        
        writer = csv.writer(outfile)
        writer.writerow(('image1', 'image2', 'similar', 'elapsed'))

        for row in reader:
            image1_path = Path(row[0])
            image2_path = Path(row[1])
            
            if image1_path.exists() and image2_path.exists():            
                image1 = load_image(image1_path)
                image2 = load_image(image2_path)
                
                ssi, elapsed_time = compare_images(image1, image2)
                bsi = normalize(ssi)
                
                # For differences that are undetectable to the human eye (same image, diff format)
                if bsi < 0.03:
                    bsi = 0

                writer.writerow((image1_path, image2_path, f'{bsi:.2f}', f'{elapsed_time:.3f}'))
                completed += 1
            else:
                writer.writerow((image1_path, image2_path, 'N/A', 'N/A'))
                failures += 1
    
    logging.info(f'Input file - {args.infile}')
    logging.info(f'Output file - {args.outfile}')
    logging.info(f'Completed - {completed}, failures - {failures}')


def main():
    logging.basicConfig (filename='autoBjorn.log', level=logging.INFO)
    logging.info(f'Started program - {time.time()}')
    arguments = parse_arg()
    check_version()
    read_write(arguments)
    logging.info(f'Ended program - {time.time()}')
    print('Complete')


if __name__ == '__main__':
    main()    
    


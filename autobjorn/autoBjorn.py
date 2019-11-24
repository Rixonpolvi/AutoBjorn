#!/usr/bin/env python3.7

#AUTOBJORN

from PIL import Image
from pathlib import Path
from skimage import metrics
import argparse
import logging
import csv
import time
import cv2
import sys


#Arguments
#input file
#Optional output file
def parse_arg():
    default_outfile = 'output.csv'

    parser = argparse.ArgumentParser(description='AutoBjorn image comparison')
    parser.add_argument('infile', type=str, help='Input CSV file')
    parser.add_argument('-o', '--outfile', type=str, help='Output CSV file', default=default_outfile)

    args = parser.parse_args()

    print(f'Input file - {args.infile}')
    print(f'Output file - {args.outfile}')

    return args


#Structural Similarity Index (SSI)  --> -1 to 1 (Different to same)
#Bjorn Similarity Index (BSI)       -->  0 to 1 (Same to different)
#Normalize [-1,1] --> [1,0] and subtract from 1 to flip
#new = 1 - (old - min/max - min)
def normalize(ssi):
    return (1 - (ssi + 1) / 2)


#Compare 2 image files
#Return ssi value and time taken
def compare_images(imageA, imageB):
    ssi_start = time.time()
    ssi = metrics.structural_similarity(imageA, imageB, multichannel=True)
    ssi_finish = time.time()
    ssi_time = ssi_finish - ssi_start
    
    return ssi, ssi_time


#Load images for comparison
#.gif not working with opencv
#image converstion using pillow.Image
def load_image(path):
    if path.suffix == '.gif':
        convert_to_png = path.parent / path.stem
        Image.open(path).save(f'{str(convert_to_png) + "_tmp"}.png', 'PNG')
        image = cv2.imread(f'{str(convert_to_png) + "_tmp"}.png', 1)
    else:
        image = cv2.imread(str(path), 1)
    return image 


#Read from args.infile
#Write to args.outfile
#N/A values if images do not exist on the filesystem
def read_write(args):
    completed = 0
    failures = 0

    with open(args.infile, 'r') as inputcsv, open(args.outfile, 'w') as outfile:
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
                
                #For differences that are undetectable to the human eye (same image, diff format)
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
    read_write(arguments)
    logging.info(f'Ended program - {time.time()}')
    print('Complete')


if __name__ == '__main__':
    main()    
    


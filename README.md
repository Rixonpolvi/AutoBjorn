# AutoBjorn
Calculate Bjorn Similarity Index Value of 2 Images

### Setup

Mac
> Install python3.7

```
$ brew install python3.7
```
> Install dependencies
```
$ pip install --requirement requirements.txt
```

Windows
> Download and install python3.7
```
https://www.python.org/downloads/release/python-373/
```
> Install dependencies
```
pip install --requirement requirements.txt
```

### Usage
Run `autoBjorn.py --help` to see this help message:
```
usage: autoBjorn.py [-h] [-o OUTFILE] infile

AutoBjorn image comparison

positional arguments:
  infile                Input CSV file

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        Output CSV file
```
Ex.
```
$ python autoBjorn.py input.csv
$ python autoBjorn.py input.csv -o output.csv
```


### Explanation

For a given input CSV file with N pairs of image paths:
- Read path of each image
- Open each image using OpenCV
- Compare the two images using scikit-image's Structural Similarity Index function
- Normalize [-1,1] SSI value to [0,1] Bjorn value
- Record time taken for SSI comparison
- Output - image1, image2, Bjorn value, elapsed comparison time


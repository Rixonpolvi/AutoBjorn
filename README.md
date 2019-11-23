# AutoBjorn
Calculate Bjorn Similarity Index Value of 2 Images

### Setup
Install python3.7

> Mac

```shell
$ brew install python3.7
```
> Windows

```
https://www.python.org/downloads/release/python-373/
```

Install dependencies
```
pip install --requirement requirements.txt
```

### Use
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


### Explanation

For given input CSV file containing 2 fields containing image paths with N records - 
- Read path of each image
- Open each image using OpenCV
- Compare the two images using scikit-image's Structural Similarity Index function
- Normalize [-1,1] SSI value to [0,1] Bjorn value
- Record time taken for SSI comparison
- Output - image1, image2, Bjorn value, elapsed comparison time


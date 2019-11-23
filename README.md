# AutoBjorn
Calculate Bjorn Similarity Index Value of 2 Images

### Setup

- If you want more syntax highlighting, format your code like this:

> update and install this package first

```shell
$ brew update
$ brew install fvcproductions
```

> now install npm and bower packages

```shell
$ npm install
$ bower install
```

For given input CSV file containing 2 fields containing image paths with N records - 
- Read path of each image
- Open each image using OpenCV
- Compare the two images using scikit-image's Structural Similarity Index function
- Normalize -1 to 1 SSI value to 0 to 1 Bjorn value
- Record time taken for SSI comparison
- Output image1, image2, Bjorn value and elapsed comparison time to and output CSV


#!/usr/bin/env python3.7

import unittest
from pathlib import Path
from autobjorn import autoBjorn

class autobjorn(unittest.TestCase):
        
    # test compare an image file to itself
    def test_same_image(self):
        img1_path = Path('Examples/aa.png')
        img2_path = img1_path
        img1 = autoBjorn.load_image(img1_path)
        img2 = autoBjorn.load_image(img2_path)
        ssi, ssi_time = autoBjorn.compare_images(img1, img2)
        bsi = autoBjorn.normalize(ssi)
        assert bsi == 0, 'Should be 0'

    # test compare 2 different image
    def test_diff_image(self):
        img1_path = Path('Examples/aa.png')
        img2_path = Path('Examples/ab.png') 
        img1 = autoBjorn.load_image(img1_path)
        img2 = autoBjorn.load_image(img2_path)
        ssi, ssi_time = autoBjorn.compare_images(img1, img2)
        bsi = autoBjorn.normalize(ssi)
        assert bsi != 0, 'Should not be 0'


if __name__ == '__main__':
    unittest.main()
    


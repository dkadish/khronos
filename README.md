khronos
=======

A collection of python and shell scripts for editing timelapse photo sets.

# Files

khronos consists of 2 files:
* manual-register.py
* slideshow.sh

## manual-register.py
Manual Register is the script that performs the assisted alignment of images.
It uses numpy, scikit-image and matplotlib to load photos from a folder, ask the user to select invariant points on each image, and then create transformations to shift each image to match the original.
It outputs a set of aligned images to a second folder as a numbered sequence of jpegs and also saves (in NumPy's .npy format) the set of key points from each image.

## slideshow.sh
Slideshow is a shell script that takes the image files output by manual-register.py and uses ImageMagick's convert tool to create intermediate images (blended between each aligned image.
It then calls ffmpeg to turn those images into an mp4 file.

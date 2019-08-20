# VK-Findme

This script allows you to find your (or maybe not your) faces in Vkontakte social network.

## What this script does

1. Trains face recognition model based on your images
2. Dumps all images from your friend's pages
3. Looks for similar faces

## How to

First of all you need to find 3-5 photos with needed face.
Photos should be high-quality e.g. with good resolution, without noise and blur.
One face for one image.

1. Run the script (`run.py`)
2. Script will create `train_images` folder
3. Put your training set into this folder
4. Script will pause and wait for you to hit `Enter`
5. Follow instructions/see info in command line prompt
6. Similar faces will be located in `similar_images` folder

## Changelog

* `1.1.0`
Implemented photo parsing from `wall`
* `1.0.0`
Implemented photo parsing from `photos`
Implemented face detection

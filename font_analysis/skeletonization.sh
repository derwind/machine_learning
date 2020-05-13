#! /bin/sh

INPUT_DIR=data
OUTPUT_DIR=skeletonization

for img in $INPUT_DIR/*.png
do
	#img_name=`basename ${img} .png`
	python skeletonization.py $img
done

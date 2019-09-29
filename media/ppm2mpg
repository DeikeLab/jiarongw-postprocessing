#!/bin/bash
# A script stolen from Wouter for converting .ppm into Microsoft Powerpoint compatible videos.
# Typical size and time:
# For a 1Gb .ppm file, it takes about 3 minutes to generate the mpg file which is around 60Mb.
# USAGE: "sh ppm2mp4 <sample>", excluding quotes, where <sample> is your filename stem. Do not include ".ppm" at the end of the filename.
# This is only useful for stacked PPM images.
# IF YOUR PPM IS SMALL ENOUGH, you could just use ffmpeg directly, something like:
#ffmpeg -i sample.ppm -qscale 0 sample.mpg
# Otherwise, this should work.
filename="$1.ppm"
output="$1.gif"
targetname="$1.mpg"
convert $filename $output
mkdir movies
ffmpeg -hide_banner -loglevel panic -i $output movies/fim_%05d.png
ffmpeg -hide_banner -loglevel panic -i movies/fim_%05d.png -qscale 0 -filter:v "setpts=4*PTS" $targetname
rm -r movies


# Some possible options
# -qscale:v 4 # 2-5 that controls quality, lower is higher quality
# -vcodec mpeg4 or some other format
# -filter:v "setpts=4*PTS" change the speed. >1 is slow down and vice versa.
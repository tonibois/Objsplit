To create provided outputs:

Counting & Measuring  stars example:

python objsplit_argp.py -tmin 50 -fmin 4 -f Hyades.jpg

Counting & Measuring nucleii in H&E image:

python objsplit_argp.py -tmin 40 -tmax 150 -fmin 20 -f GTEX-1314G-0526.tif

Counting & Measuring Adypocites in H&E image:

python objsplit_argp.py -tmin 210 -tmax 255 -fmin 100 -f GTEX-1314G-0526.tif

Counting Clouds in satellite image:

python objsplit_argp.py -tmin 180 -tmax 255 -fmin 30 -f terrasp.jpg
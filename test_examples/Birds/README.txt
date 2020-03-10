To produce mask_Bin70.jpg:
python objsplit_argp_v2.py -f Original_Image.jpg -fmin 100 -thm B -tmin 70 -tmax 255 -inv y
To produce mask_Bin100.jpg:
python objsplit_argp_v2.py -f Original_Image.jpg -fmin 100 -thm B -tmin 100 -tmax 255 -inv y
To produce mask_Otsu.jpg:
python objsplit_argp_v2.py -f Original_Image.jpg -fmin 100 -thm O -tmin 50 -tmax 255 -inv y
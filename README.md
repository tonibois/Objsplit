## Objsplit

 A software for object detection and computing of geometrical features on images.

 Author: Antonio Oliver Gelabert (ORCID : http://orcid.org/0000-0001-8571-2733)
 
-----------------------------------------------------------------------------------------------------------------------------
**Input**
-----------------------------------------------------------------------------------------------------------------------------
+ Sample image (JPG,PNG,TIF,GIF)
+ Input file with parameters (in INPUT_FILE_VERSION only)
-----------------------------------------------------------------------------------------------------------------------------
**Outputs** (In a labeled "out_+time" created folder)
-----------------------------------------------------------------------------------------------------------------------------
+ A subfolder "split" : all features detected by the program (Optional. Default => None)
+ timestr_parameters_and_outputs.txt : Parameter set and statistical output information file.
+ timestr_data.txt : individual information for all computed parameters derived from detected features : Lenght, Width, area perimeter and centroid coordinates.
+ timestr_allcont.tif  : the original image with overlaped contours, boxed features and identifier annotations 
+ timestr_binary.tif   : masked image file (black/white)
+ timestr_histogram.png : image of histograms for all parameters: Lenght, Width, area and perimeter
+ timestr_box.png       : image of box plots for all computed parameters derived from detected features : Lenght, Width, area and perimeter
-----------------------------------------------------------------------------------------------------------------------------
**Program Variants**
 -----------------------------------------------------------------------------------------------------------------------------
 + INPUT_FILE_VERSION/objsplit_inpfilevers.py   : Version that read parameters in input.dat file and process specific image
 + ARG_PARSED_VERSION/objsplit_argp.py          : Version to pass commands directly from the command line and process specific image
 + BATCH_VERSION/objsplit_batch.py              : Takes all images in specified directory and process all of them
 + objsplit.ipynb                               : Original version in ipython notebook format
 + objsplit.py                                  : Original version in python source code
 -----------------------------------------------------------------------------------------------------------------------------
**Parameters**
 -----------------------------------------------------------------------------------------------------------------------------
+ sc : scale conversion (in units/pixel)
+ tmin : minimum binary threshold for object detection
+ tmax : maximum binary threshold for object detection
+ fmin : minimum area filter (in units**2)
+ fmax : maximum area filter (in units**2)
+ f   : filename of the input file
+ split : Split or not in separated outputs
 -----------------------------------------------------------------------------------------------------------------------------
**Usage examples**
 -----------------------------------------------------------------------------------------------------------------------------
+ python objsplit_argp.py -tmin 210 -tmax 255 -fmin 100 -f terrasp.jpg 
+ python objsplit_batch.py
 -----------------------------------------------------------------------------------------------------------------------------

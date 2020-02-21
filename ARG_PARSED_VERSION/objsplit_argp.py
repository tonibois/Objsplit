
# coding: utf-8

# OBJECT SPLITTER (OBJSPLIT) - ARGPARSED VERSION - 
# -----------------------------------------------------------------------------------------------------------------------------
# Author: Antonio Oliver Gelabert (ORCID : http://orcid.org/0000-0001-8571-2733)
# -----------------------------------------------------------------------------------------------------------------------------
# Parameters
# -----------------------------------------------------------------------------------------------------------------------------
#   sc : scale conversion (in units/pixel)
#   tmin : minimum binary threshold for object detection
#   tmax : maximum binary threshold for object detection
#   fmin : minimum area filter (in units**2)
#   fmax : maximum area filter (in units**2)
#   f   : filename of the input file
# -----------------------------------------------------------------------------------------------------------------------------

from datetime import datetime
import time as tm
import time
import os
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
import warnings
import argparse


t0= tm.clock()

# Parsing optional arguments of the program  
ap = argparse.ArgumentParser()
ap.add_argument("-sc", "--scale", required=False, default='1', help="scale dymensions. Default value: 1 unit/pixel")
ap.add_argument("-tmin", "--tmin", required=False, default='150', help="Low threshold brightness (between 0 and 255, close to 0 and bigger, to exclude dark images). Default value:150")
ap.add_argument("-tmax", "--tmax", required=False, default='255', help="High threshold brightness (between 0 and 255, close to 0 and bigger, to exclude dark images). Default value:255")
ap.add_argument("-fmin", "--filtmin", required=False, default='500', help="Mininum area filter (in units**2). Default value:500 pixels")
ap.add_argument("-fmax", "--filtmax", required=False, default='99999999', help="maximum area filter (in units**2). Default value:no limit")
ap.add_argument("-f", "--filename", required=True, help="Filename of input images. ")
args = vars(ap.parse_args())

# Assign args to program variables

fname_sb=args["filename"]
scale=int(args["scale"])
tresh_8b_min=int(args["tmin"])
tresh_8b_max=int(args["tmax"])
filtareamin=int(args["filtmin"])/(scale*scale)
filtareamax=int(args["filtmax"])/(scale*scale)

dirstr=str(round(time.time()))
os.mkdir("out_"+dirstr)
os.mkdir("out_"+dirstr+"/split")

f2 = open("out_"+dirstr+"/"+dirstr+"_ind_data.txt", 'w')
f2.write('ID,L(km),W(km),Area(km2),perimeter(km),xc,yc\n')

#fname_sb='terrasp.jpg'
img = cv2.imread(fname_sb)

#scale=3   # km/pixels  
#tresh_8b_min=150
#tresh_8b_max=255
#filtareamin=5000/(scale*scale)  # in km2
#filtareamax=999999999/(scale*scale) #np.size(img)/(3)

#tresh_bin=int(round(tresh_8b/100*255))#84 #84 (33%), 102 (40%) , 114 (45%)
font = cv2.FONT_HERSHEY_SIMPLEX
        
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret,patt = cv2.threshold(gray,tresh_8b_min,tresh_8b_max,cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(patt, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
contpic=cv2.imread(fname_sb)# cv2.drawContours(bwcont, contours, -1, (255, 0, 0), 1)

areatot=0
areafilt=0
nfilt=0

areafstats=[]
perfstats=[]
areastats=[]
boxc=[]
Lboxst=[]
Wboxst=[]

for j in range(0,len(contours)-1,1):
    area = cv2.contourArea(contours[j])*scale**2
    perimeter = cv2.arcLength(contours[j],True)*scale
    areatot=areatot+area
    areastats.append(area)
    if (area > filtareamin) & (area < filtareamax):
        nfilt=nfilt+1
        areafstats.append(area)
        perfstats.append(perimeter)
        areafilt=areafilt+area
        
        rect = cv2.minAreaRect(contours[j])
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        boxc.append(box)
        
        x0=box[0][0]
        y0=box[0][1]
        x1=box[1][0]
        y1=box[1][1]
        x2=box[2][0]
        y2=box[2][1]
        x3=box[3][0]
        y3=box[3][1]
        
        pm0x=int(round((box[0][0]+box[1][0])/2))
        pm0y=int(round((box[0][1]+box[1][1])/2))
        pm1x=int(round((box[1][0]+box[2][0])/2))
        pm1y=int(round((box[1][1]+box[2][1])/2))
        pm2x=int(round((box[2][0]+box[3][0])/2))
        pm2y=int(round((box[2][1]+box[3][1])/2))
        pm3x=int(round((box[3][0]+box[0][0])/2))
        pm3y=int(round((box[3][1]+box[0][1])/2)) 
       
        d01box=((box[0][0]-box[1][0])**2+(box[0][1]-box[1][1])**2)**0.5
        d12box=((box[1][0]-box[2][0])**2+(box[1][1]-box[2][1])**2)**0.5
        
        Abox=d01box*d12box*scale**2
        Lbox=np.maximum(d01box,d12box)*scale
        Wbox=np.minimum(d01box,d12box)*scale    
    
        Lboxst.append(Lbox)
        Wboxst.append(Wbox)
        
        xmaxb=np.max((x0,x1,x2,x3))
        ymaxb=np.max((y0,y1,y2,y3))
        xminb=np.min((x0,x1,x2,x3))
        yminb=np.min((y0,y1,y2,y3))
        
        if(xminb < 1):
            xminb=1
        if(yminb < 1): 
            yminb=1
        if(xmaxb < 1): 
            xmaxb=1
        if(ymaxb < 1): 
            ymaxb=1
            
        #cv2.putText(contpic, str(round(area,2)), (int(round((pm0x+pm2x)*0.5)+5),int(round((pm2y+pm0y)*0.5))), font, 0.3, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(contpic, str(nfilt), (int(round((pm0x+pm2x)*0.5)+5),int(round((pm2y+pm0y)*0.5))), font, 0.3, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.drawContours(contpic, contours[j], -1, (255, 0, 0), 1)
        cv2.drawContours(contpic,[box],0,(0,255,255),1) 
        cv2.imwrite("out_"+dirstr+"/split/filtobj_"+str(nfilt)+".tif", contpic[yminb:ymaxb,xminb:xmaxb,:])
        f2.write(str(nfilt)+','+str(round(Lbox,2))+','+str(round(Wbox,2))+','+str(round(area,2))+','+str(round((pm0x+pm2x)*0.5,2))+','+str(round((pm2y+pm0y)*0.5,2))+'\n')

cv2.imwrite("out_"+dirstr+"/"+dirstr+"_allcont.tif", contpic)
f2.close()
# Initial set of parameters and statistical information 

f3 = open("out_"+dirstr+"/"+dirstr+"_parameters_and_outputs.txt", 'w')

# Cabecera del programa
now = datetime.now() 
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")
time = now.strftime("%H:%M:%S")

f3.write("************************************************************************************************************"+'\n')
f3.write("************************************************************************************************************"+'\n')
f3.write("This ouput has been generated on " + day +"th of " + month + " of year " + year + ", at local time: " + time +'\n')
f3.write("************************************************************************************************************"+'\n')
f3.write("************************************************************************************************************"+'\n')
f3.write("OBJECT DETECTOR&COUNTER IN IMAGES"+'\n')
f3.write("************************************************************************************************************"+'\n')
f3.write("************************************************************************************************************"+'\n')
f3.write("Author                : Antonio Oliver Gelabert"+'\n')
f3.write("Contact               : toni.oliver87@gmail.com"+'\n')
f3.write("************************************************************************************************************"+'\n')
f3.write("*****************************          PARAMETERS         **************************************************"+'\n')
f3.write("************************************************************************************************************"+'\n')
f3.write("Filename : "+fname_sb+'\n')
f3.write("Scale : "+str(scale)+" (reference in units/pixel)\n")
f3.write("Minimum intensity threshold : "+str(tresh_8b_min)+'\n')
f3.write("Maximum intensity threshold : "+str(tresh_8b_max)+'\n')
f3.write("Minimum area filter : "+str(filtareamin)+'\n')
f3.write("Maximum area filter :" +str(filtareamax)+'\n')
f3.write("************************************************************************************************************"+'\n')
f3.write("*****************************           OUTPUTS           **************************************************"+'\n')
f3.write("************************************************************************************************************"+'\n')
f3.write("Number of objects found: "+str(len(contours))+'\n') 
f3.write("Average leght of objects found (in units): "+ str(round(np.mean(Lboxst),2))+"+/-"+str(round(np.std(Lboxst),2))+'\n')
f3.write("Average width of objects found (in units): "+ str(round(np.mean(Wboxst),2))+"+/-"+str(round(np.std(Wboxst),2))+'\n')
f3.write("Average area of objects found (in units**2): "+ str(round(np.mean(areafstats),2))+"+/-"+str(round(np.std(areafstats),2))+'\n')
f3.write("Average perimeter of objects found (in units): "+ str(round(np.mean(perfstats),2))+"+/-"+str(round(np.std(perfstats),2))+'\n')
f3.write("************************************************************************************************************"+'\n')
f3.write("************************************************************************************************************"+'\n')

# Statistical analysis plots
# create a figure 
fig = plt.figure() 
# define subplots 
plt1 = fig.add_subplot(221) 
plt2 = fig.add_subplot(222) 
plt3 = fig.add_subplot(223) 
plt4 = fig.add_subplot(224) 
plt1.hist(areafstats, bins=10) 
plt1.set_title('Area') 
plt2.hist(Lboxst, bins=10) 
plt2.set_title('Lenght') 
plt3.hist(Wboxst, bins=10)  
plt3.set_title('Width') 
plt4.hist(perfstats, bins=10) 
plt4.set_title('Perimeter') 
# Space between subplots 
fig.subplots_adjust(hspace=.5,wspace=0.5) 
plt.savefig("out_"+dirstr+"/"+dirstr+"_histplot.png",dpi=200)

# create a figure 
fig2 = plt.figure() 
# define subplots 
plt5 = fig2.add_subplot(221) 
plt6 = fig2.add_subplot(222) 
plt7 = fig2.add_subplot(223) 
plt8 = fig2.add_subplot(224) 
plt5.boxplot(areafstats) 
plt5.set_title('Area') 
plt6.boxplot(Lboxst)  
plt6.set_title('Lenght') 
plt7.boxplot(Wboxst)    
plt7.set_title('Width') 
plt8.boxplot(perfstats)  
plt8.set_title('Perimeter') 
# Space between subplots 
fig2.subplots_adjust(hspace=.5,wspace=0.5) 
plt.savefig("out_"+dirstr+"/"+dirstr+"_boxsplot.png",dpi=200)


t1 = tm.clock()
f3.write("Job time (s) : "+ str(np.round(t1 - t0,2))+'\n') 
f3.write("************************************************************************************************************"+'\n')
f3.write("************************************************************************************************************"+'\n')
f2.close()

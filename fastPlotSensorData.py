#! /usr/bin/python
# ----------------
# Autor: Tommaso Tabarelli - Sep 2013
#
#        Optimized Aug 2016 to anable faster plotting
#        (sufficient to track at least 'medium', 
#         at times 'fast' streaming from Wireless IMU,
#         upon replacing plt.draw() with redrawing only
#         of parts of the plot that are updated) 
#
# Execute with python fastPlotSensorData.py
# -- Get sensor data with UDP and draw accelearation graphs

### ----- Import section ------------------
# For UDP socket data transmission
import socket, traceback, string
from sys import stderr
# For plotting
import matplotlib.pyplot as plt
#import matplotlib.animation as animation
import numpy
from matplotlib.ticker import AutoMinorLocator
# ----------------------------------------

### Initialize plot and axes
minorLocatorX   = AutoMinorLocator(5)
minorLocatorY   = AutoMinorLocator(5)
fig = plt.figure(figsize=(10,6),edgecolor='r',facecolor='w')  # figure size
ax = plt.axes(xlim=(0,10), ylim=(-20, 20))                    # graph size
ax.xaxis.set_minor_locator(minorLocatorX)                     # ticks
ax.yaxis.set_minor_locator(minorLocatorY)
plt.ylabel("Acceleration (m/s$^2$)")                          # labels
plt.xlabel("Time (s)")

# inizialize empty plots
hlx, = plt.plot([], [], lw=1)
hly, = plt.plot([], [], lw=1)
hlz, = plt.plot([], [], lw=1)

# legend
labels = ['$a_x$','$a_y$','$a_z$']
plt.legend(labels, ncol=3, loc='upper center', 
           bbox_to_anchor=[0.5, 1.1], 
           columnspacing=1.0, labelspacing=0.0,
           handletextpad=0.0, handlelength=1.5,
           fancybox=True, shadow=False)

# activate interactive update and draw graphs
plt.ion()
plt.pause(0.00001)

# Let's capture the background of the figure to speed up redrawing
fig.canvas.draw()
background = fig.canvas.copy_from_bbox(ax.bbox) 

# define data lists
tlist = list()
xlist = list()
ylist = list()
zlist = list()

# --- FUNCTION TO UPDATE GRAPHS CONTENTS (Still to optimize)
def update_line(hlx, hly, hlz, ttemp, xtemp, ytemp, ztemp):
# Append last element
    tlist.append(ttemp)
    xlist.append(xtemp)
    ylist.append(ytemp)
    zlist.append(ztemp)
# pop out first element, if time display exceed 4.5 s
# (this is to avoid the graph depth to grow excessive with 
# consequences on the efficiency of the process. It can be 
# done on the length of the buffer: e.g. if len(tlist)>maxLen: )
    if ttemp-float(tlist[0]) > 9.5: 
        tlist.pop(0)
        xlist.pop(0)
        ylist.pop(0)
        zlist.pop(0)
        ax = plt.gca()
        ax.set_xlim(ttemp-9.5,ttemp+0.5)
# update plots
    hlx.set_data(tlist, xlist)
    hly.set_data(tlist, ylist)
    hlz.set_data(tlist, zlist)

## MAIN Part: read data from UDP socket and call plot updater
# ---- INIT
host = ''
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))

# ---- READ DATA
tstart = 0

while 1:
    try:
        message, address = s.recvfrom(8192)
        data = message.split( "," ) # split records using comma as delimiter (data are streamed in CSV format)
# ---- manipulate time
        t = float(data[0])
        if (tstart==0): 
            tstart = float(data[0])
        temp = t-tstart
# ---- get accelerometer data
        sensorID = int(data[1])
        if sensorID==3:     # sensor ID for the eccelerometer
            gx, gy, gz = float(data[2]), float(data[3]), float(data[4])
# ---- draw (x,y)
        update_line(hlx,hly,hlz,temp,gx,gy,gz)
#        plt.draw()
        fig.canvas.restore_region(background)
        ax.draw_artist(hlx)
        ax.draw_artist(hly)
        ax.draw_artist(hlz)
        fig.canvas.blit(ax.bbox)
        plt.pause(0.00001)

# SAVE TO FILE
#            print >> open("prova.txt","a"), temp, ax, ay, az
#            print temp, ax, ay, az
# FLUSH TO STERR
        stderr.write("\r temp = %s s |  (ax,ay,az) = (%s,%s,%s) m/s^2" % (temp, gx, gy, gz) )
        stderr.flush()

    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc()

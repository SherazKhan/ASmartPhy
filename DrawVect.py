### --------  TTF - 2013, Sep 8th ---------
# Code to visualize the acceleration vector
# from data read via Wireless IMU
#
# You may want to copy also matplotlibrc for
# reasonable graphic rendering
# needs matplotlib and numpy installed
# -----------------------------------------
## LIBRARIES
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations
# For UDP socket data transmission
import socket, traceback, string
from sys import stderr
#draw a vector
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

## --- DEFINE CLASS FOR ARROWS
class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

## --- DEFINE FIGURE LAYOUT
fig = plt.figure(figsize=(7,7),edgecolor='r',facecolor='w')
fig.subplots_adjust(bottom=0.05)
fig.subplots_adjust(top=1)
fig.subplots_adjust(left=0.)
fig.subplots_adjust(right=0.95)

ax = fig.gca(projection='3d')
#ax.set_aspect("equal")
ax.view_init(30,-30)
ax.set_xlabel('$a_x (m/s^2)$')
ax.set_ylabel('$a_y (m/s^2)$')
ax.set_zlabel('$a_z (m/s^2)$')
#ax.set_axis_off()


## --- START DRAWING
## Draw axis with titles through (0,0,0)
ax.plot([-10,10],[0,0],[0,0],color='k',linestyle='--')   #line -1,1 trough 0,0
ax.plot([0,0],[-10,10],[0,0],color='k',linestyle='--')
ax.plot([0,0],[0,0],[-10,10],color='k',linestyle='--')
#ax.text(10,0,0,"$A_x$",zdir='x')                         # labels
#ax.text(0,10,0,"$A_y$",zdir='y') 
#ax.text(0,0,10,"$A_z$",zdir='z') 

## --- Reference frame
xax = Arrow3D([0,10],[0,0],[0,0], mutation_scale=10, lw=1, arrowstyle="-|>", color="k")
yax = Arrow3D([0,0],[0,10],[0,0], mutation_scale=10, lw=1, arrowstyle="-|>", color="k")
zax = Arrow3D([0,0],[0,0],[0,10], mutation_scale=10, lw=1, arrowstyle="-|>", color="k")
ax.add_artist(xax)
ax.add_artist(yax)
ax.add_artist(zax)

plt.ion()
plt.show()

## MAIN Part: read data from UDP socket and call plot updater
# ---- INIT
host = ''
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))

# ---- READ DATA
#tstart = 0

while 1:
    try:
        message, address = s.recvfrom(8192)
        data = message.split( "," ) # split records using comma as delimiter (data are streamed in CSV format)
# ---- manipulate time
#        t = float(data[0])
#        if (tstart==0): 
#            tstart = float(data[0])
#        temp = t-tstart
# ---- get accelerometer data
        sensorID = int(data[1])
        if sensorID==3:     # sensor ID for the eccelerometer
            xtemp, ytemp, ztemp = float(data[2]), float(data[3]), float(data[4])
# ---- draw (x,y)
#            print "Hello"
            vv = Arrow3D([0,xtemp],[0,ytemp],[0,ztemp], mutation_scale=20, lw=2, arrowstyle="-|>", color="m")
            v1 = Arrow3D([0,xtemp],[0,0],[0,0], mutation_scale=20, lw=2, arrowstyle="-|>", color="b")
            v2 = Arrow3D([0,0],[0,ytemp],[0,0], mutation_scale=20, lw=2, arrowstyle="-|>", color="g")
            v3 = Arrow3D([0,0],[0,0],[0,ztemp], mutation_scale=20, lw=2, arrowstyle="-|>", color="r")

            iv = ax.add_artist(vv)
            ix = ax.add_artist(v1)
            iy = ax.add_artist(v2)
            iz = ax.add_artist(v3)

        plt.draw()
        plt.pause(0.001)
        iv.remove()
        ix.remove()
        iy.remove()
        iz.remove()

# SAVE TO FILE
#            print >> open("prova.txt","a"), temp, ax, ay, az
#            print temp, ax, ay, az
# FLUSH TO STERR
#        stderr.write("\r (ax,ay,az) = (%s,%s,%s) m/s^2" % (xtemp, ytemp, ztemp) )
#        stderr.flush()

    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc()

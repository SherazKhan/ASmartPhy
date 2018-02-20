# -------------------------------------------------------
import socket, traceback, string
from sys import stderr

host = ''
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))

# print one blank line
print 

tstart=0
while 1:
    try:
        message, address = s.recvfrom(8192)
#        print message

# split records using comma as delimiter (data are streamed in CSV format)
        data = message.split( "," )

# convert to flaot for plotting purposes
        t = data[0]
        if tstart == 0:
            tstart=float(t)
        sensorID = int(data[1])
        if sensorID==3:     # sensor ID for the eccelerometer
            ax, ay, az = data[2], data[3], data[4]
# SAVE TO FILE
            print >> open("data.txt","a"), float(t)-tstart, ax, ay, az
#            print t, ax, ay, az
# FLUSH TO STERR
            stderr.write("\r t = %10.5f s |  (ax,ay,az) = (%s,%s,%s) m/s^2" % (float(t)-tstart, ax, ay, az) )
            stderr.flush()

    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc()
# -------------------------------------------------------

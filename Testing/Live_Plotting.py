# myplot.py
from bokeh.plotting import figure, curdoc
from bokeh.driving import linear
import sys
from socket import socket,AF_INET,SOCK_DGRAM
import struct
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import sys


p = figure(plot_width=400, plot_height=400)
r1 = p.line([], [], color="firebrick", line_width=2)


ds1 = r1.data_source

@linear()
def update(step):
    PORT_NUMBER = 65000
    SIZE = 1024
    hostName = gethostbyname('0.0.0.0')
    mySocket = socket(AF_INET, SOCK_DGRAM)
    mySocket.bind((hostName, PORT_NUMBER))
    print("Test server listening on port {0}\n".format(PORT_NUMBER))

    (data, addr) = mySocket.recvfrom(SIZE)
    results = struct.unpack('f', data)
    results = results[0]
    print(results)

    ds1.data['x'].append(step)
    ds1.data['y'].append(results)
    ds1.trigger('data', ds1.data, ds1.data)


curdoc().add_root(p)

# Add a periodic callback to be run every 500 milliseconds
curdoc().add_periodic_callback(update, 1000)

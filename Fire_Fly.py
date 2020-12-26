import numpy as np
import tflite_runtime.interpreter as tflite
import pandas as pd
import cv2
import os
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import sys
import time

# define a video capture object

#Testing a mp4 file
#vid = cv2.VideoCapture('/home/pi/coral/fire_fly/download.mp4')

vid = cv2.VideoCapture(0)

while (True):

    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    # Display the resulting frame
    # Comment out imshow for when running headlessly
    cv2.imshow('frame', frame)

    cv2.imwrite("/home/pi/Downloads/frame.jpg", frame)

    interpreter = tflite.Interpreter('/home/pi/coral/fire_fly/model.tflite')
    

    def testResult(file):
        X, Y = [], []
        img_size = (300, 300)
        x = cv2.imread(file)
        x = cv2.resize(x, img_size, interpolation=cv2.INTER_AREA)
        X.append(x / 255.0)
        Y.append(1)
        X = np.stack(X)
        interpreter.allocate_tensors()
        # Get input and output tensors.
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        X = X.astype(np.float32)
        # Test the model on random input data.
        input_shape = input_details[0]['shape']
        input_data = X
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()

        # The function `get_tensor()` returns a copy of the tensor data.
        # Use `tensor()` in order to get a pointer to the tensor.
        output_data = interpreter.get_tensor(output_details[0]['index'])
        return (output_data)

    print(testResult("/home/pi/Downloads/frame.jpg"))
    
    PORT_NUMBER = 65000
    SIZE = 1024
    hostName = gethostbyname('0.0.0.0')
    SERVER_IP = '192.168.1.159'
    mySocket = socket(AF_INET, SOCK_DGRAM)
    mySocket.bind((hostName, PORT_NUMBER))
    print("Test server listening on port {0}\n".format(PORT_NUMBER))
    mySocket = socket(AF_INET, SOCK_DGRAM)
    mySocket.connect((SERVER_IP, PORT_NUMBER))
    value = testResult("/home/pi/Downloads/frame.jpg")[0][0]
    byte = value.tobytes()
    mySocket.send(byte)
    time.sleep(.5)



    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()

#Clean Garbage
os.remove("/home/pi/Downloads/frame.jpg")

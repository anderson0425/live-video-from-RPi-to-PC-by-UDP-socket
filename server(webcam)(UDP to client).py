#我的server ip   是43.2

import cv2
import socket
import pickle
import numpy as np
import math

c_host = "192.168.43.246"
s_host = "192.168.43.2"
port = 5555
max_length = 60000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((s_host, port))

frame_info = None
buffer = None
frame = None

print("hi 1")
cap = cv2.VideoCapture(0)
ret, frame = cap.read()

#data, address = sock.recvfrom(max_length)

while ret:
#    print("hi 2")
    # compress frame
    print("Server encode img")
    retval, buffer = cv2.imencode(".jpg", frame)

    if retval:
#        print("hi 3")
        # convert to byte array
        buffer = buffer.tobytes()
        # get size of the frame
        buffer_size = len(buffer)

        num_of_packs = 1
        if buffer_size > max_length:
            num_of_packs = math.ceil(buffer_size/max_length)

        frame_info = {"packs":num_of_packs}

        # send the number of packs to be expected
        #print("Number of packs:", num_of_packs)
        sock.sendto(pickle.dumps(frame_info), (c_host, port))
        
        left = 0
        right = max_length

        for i in range(num_of_packs):
            #print("left:", left)
            #print("right:", right)

            # truncate data to send
            data = buffer[left:right]
            left = right
            right += max_length

            # send the frames accordingly
            sock.sendto(data, (c_host, port))
    print("Server send one img to client")
    
    ret, frame = cap.read()
print("done")
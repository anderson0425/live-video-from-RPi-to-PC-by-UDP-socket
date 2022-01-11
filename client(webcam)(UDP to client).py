#我的client ip   是43.246

import cv2
import socket
import math
import pickle
import numpy as np
s_host = "192.168.43.2"
c_host = "192.168.43.246"
max_length = 60000  #可傳送或讀取的bytes總長度
port = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((c_host, port))
while True:
    print("hi 1")
    
    data, address = sock.recvfrom(max_length)
    print(data)
    
    if len(data) < 100:
        print("hi 2")
        try:  #讓UDP丟包的時候，可以讓可能造成frame_info = pickle.loads(data)出現錯誤的情況被排除，以避免程式執行中斷(UDP傳輸中斷)。
            frame_info = pickle.loads(data)

            if frame_info:
                print("hi 3")
                nums_of_packs = frame_info["packs"]

                for i in range(nums_of_packs):
                    data, address = sock.recvfrom(max_length)

                    if i == 0:
                        buffer = data
                    else:
                        buffer += data

                frame = np.frombuffer(buffer, dtype=np.uint8)
                frame = frame.reshape(frame.shape[0], 1)

                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                
                #frame = cv2.flip(frame, 1)  
                # #FIXME:若是用PI CAMERA，這段可以註解調，
                # 若是WEBCAM則這段要加上去

                if frame is not None and type(frame) == np.ndarray:
                    cv2.imshow("Stream", frame)
                    print("hi 5")
                    cv2.waitKey(30)
                    if cv2.waitKey(1) == 27:
                        break
        except:
            print("error")
                
print("goodbye")

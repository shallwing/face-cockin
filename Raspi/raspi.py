#!/usr/bin/python3

import ImageProcess, codec
import PTZControl, PanControl
import socket as sock
import os, time


PORT = 9123
HOST = "47.99.113.188"
MSG_SIZE = 128

def sock_init():
    client = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    return client

'''Set by reality'''
def capture_process():
    PanControl.pan_tilt_up()
    PTZControl.pan_tilt_up()


if '__main__' == __name__:


    while True:

        #capture_process()
#### Set connection with server 47.99... ####
        try:
            client = sock_init()
            client.connect((HOST, PORT))
        except sock.error as msg:
            print(msg)
            continue

#### Send images from server ####
        pan = os.listdir("./camera_photo/panorama")
        ptz = os.listdir("./camera_photo/ptz")
        frame = codec.encode_send(count=len(pan)+len(ptz), type='count')
        client.send(frame.encode('utf-8'))
        frame = client.recv(MSG_SIZE)
        frame = bytes.decode(frame)
        if codec.decode(frame=frame):
            for filename in ptz+pan:
                fhead = ImageProcess.img_pack(filename)
                client.send(fhead)
                ImageProcess.img_send(filename, client)
#### ACK signal to server ####
        frame = client.recv(MSG_SIZE)
        frame = bytes.decode(frame)
        if codec.decode(frame=frame):
            client.close()
        time.sleep(60*15)

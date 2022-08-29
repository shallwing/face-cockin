#!/usr/bin/python3
import ImageProcess, codec
import socket as sock
import struct, time
import Detect

PORT = 9123
HOST = "47.99.113.188"
MSG_SIZE = 128

def sock_init():
    client = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    return client



if "__main__" == __name__:

    time.sleep(2)

#### Set connection with server 47.99... ####
    while True:
        try:
            client = sock_init()
            client.connect((HOST, PORT))
        except sock.error as msg:
            print(msg)
            continue

#### Set the recept request ####
        frame = codec.encode_send(type='recv')
        client.send(frame.encode('utf-8'))

        frame = client.recv(MSG_SIZE)
        frame = bytes.decode(frame)

        imgs = codec.decode(frame)
        frame = codec.encode_send(type='ok')
        client.send(frame.encode('utf-8'))
#### Receive the imgs pictures ####
        for num in range(imgs):
            filesize = struct.calcsize('128sq')
            buf = client.recv(filesize)
            if buf:
                filename, filesize = struct.unpack('128sq', buf)
                ImageProcess.img_get(client, filename, filesize)

#### Send the detection info to server ####
        time.sleep(1)
        person_count = 12
        frame = codec.encode_send(type='count', count=person_count)
        client.send(frame.encode('utf-8'))
        time.sleep(1)
        #### ACK signal from server ####
        frame = client.recv(MSG_SIZE)
        frame = bytes.decode(frame)
        if True == codec.decode(frame=frame):
            print("%s, GPU get %d images!" % (time.asctime(), imgs))
        client.close()
        time.sleep(15*60)

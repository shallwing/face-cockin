#!/usr/bin/python3

import socket as sock
import struct, os, time
import ImageProcess, codec

PORT = 9123
BACK_LOG = 32
MSG_SIZE = 128

def sock_init():
    server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    server.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
    hostname = sock.gethostname()
    server.bind((hostname, PORT))
    server.listen(BACK_LOG)
    return server


if "__main__" == __name__:

    server = sock_init()
    person_count, count = 0, 0

    while True:
        client, address = server.accept()
        frame = client.recv(MSG_SIZE)
        frame = bytes.decode(frame)
#### When Raspi connect the server, receive pictures from it ####
        if frame.find("Pi") >= 0:
            count = codec.decode(frame=frame)
            frame = codec.encode_send(type='ok')
            client.send(frame.encode('utf-8'))
            for num in range(count):
                filesize = struct.calcsize('128sq')
                buf = client.recv(filesize)
                if buf:
                    filename, filesize = struct.unpack('128sq', buf)
                    ImageProcess.img_get(client, filename, filesize)

            #### Send ACK signal to Raspi ####
            frame = codec.encode_send(type='ok')
            client.send(frame.encode('utf-8'))
            client.close()


#### When GPU connect the server, send pictures to GPU ####
        if frame.find("GPU") >= 0:
            if 'recv' == codec.decode(frame=frame):
                pan = os.listdir("./camera_photo/panorama")
                ptz = os.listdir("./camera_photo/ptz")
                frame = codec.encode_send(count=len(pan) + len(ptz), type='count')
                client.send(frame.encode('utf-8'))
                frame = client.recv(MSG_SIZE)
                frame = bytes.decode(frame)
                if codec.decode(frame=frame):
                    for filename in ptz+pan:
                        fhead = ImageProcess.img_pack(filename)
                        client.send(fhead)
                        ImageProcess.img_send(filename, client)
        #### After sending pictures to GPU, get the detection result from GPU ####
                #time.sleep(60)
                frame = client.recv(MSG_SIZE)
                frame = bytes.decode(frame)
                person_count = codec.decode(frame=frame)
                frame = codec.encode_send(type='ok')

        #### ACK signal to GPU ####
                client.send(frame.encode("utf-8"))
                client.close()

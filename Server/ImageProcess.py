import struct
import os
import re
import socket as sock


def img_pack(filename:str):
    if re.match('panorama', filename):
        fhead = struct.pack(b'128sq', bytes(filename, encoding='utf-8'),
                            os.stat("./camera_photo/panorama/" + filename).st_size)
    else:
        fhead = struct.pack(b'128sq', bytes(filename, encoding='utf-8'),
                            os.stat("./camera_photo/ptz/" + filename).st_size)
    # Pack xxx.jpg by 128sq
    return fhead


def img_send(filename:str, fd_sock):
    if re.match('panorama', filename):
        fp = open("./camera_photo/panorama/"+filename, 'rb')
    else:
        fp = open("./camera_photo/ptz/"+filename, 'rb')
    while True:
        data = fp.read(1024)
        if not data:
            break
        fd_sock.send(data)


def img_get(fd_sock, filename, filesize:int):
    filename = filename.decode().strip('\x00')
    if re.match('panorama', filename):
        new_filename = "./camera_photo/panorama/%s" % filename
    else:
        new_filename = "./camera_photo/ptz/%s" % filename
    recvd_size, fp = 0, open(new_filename, 'wb')

    while not recvd_size == filesize:
        if filesize - recvd_size > 1024:
            data = fd_sock.recv(1024)
            recvd_size += len(data)
        else:
            data = fd_sock.recv(filesize - recvd_size)
            recvd_size += len(data)
        fp.write(data)  # Write the image data into picture
    fp.close()

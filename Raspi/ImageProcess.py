import struct, os, re
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
        else:
            fd_sock.send(data)


'''
Frames from Aliyun:
(1) Aliyun_send_COUNT_12: "The GPU will receive 12 pictures"
(2) Aliyun_send_OK: "ACK signal from Aliyun"

Frames from GPU:
(1) GPU_send_RECV: "The GPU is going to receive pictures"
(2) GPU_send_OK: "ACK signal from GPU"

Frame from Raspi:
(1) Pi_send_OK: "The Raspi has accepted the signal successfully"
(2) Pi_send_COUNT_12: "The Raspi will send 12 pictures to server"
'''


def encode_send(type='ok', count=0):
    frame = "Aliyun_send_"
    if 'ok' == type:
        frame = frame + "OK"
    elif 'count' == type:
        frame = frame + "COUNT_" + str(count)
    else:
        frame = ""
    return frame


def decode(frame:str):
    if frame.find("Pi") >= 0:
        if frame.find("OK") >= 0:
            return True
        elif frame.find("COUNT") >= 0:
            count, pos = 0, frame.find("COUNT") + len("COUNT_")
            while pos < len(frame):
                count = count * 10 + int(frame[pos])
                pos += 1
            return count

    if frame.find("GPU") >= 0:
        if frame.find("OK") >= 0:
            return 'ok'
        elif frame.find("RECV") >= 0:
            return 'recv'


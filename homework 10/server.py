# echo-server.py

import socket
import binascii


def main():
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT = 55000  # Port to listen on (non-privileged ports are > 1023)
    MsgId1 = 1
    MsgId2 = 2
    MsgId3 = 3
    SeqCnt1 = 0
    SeqCnt2 = 0
    SeqCnt3 = 0
    payload = [0] * 500

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print('Waiting for connection')
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                inData = input("MsgId pe care il transmitem: ")
                if inData == "1":
                    msgId = MsgId1
                    SeqCnt = SeqCnt1
                    SeqCnt1 += 1
                if inData == "2":
                    msgId = MsgId2
                    SeqCnt = SeqCnt2
                    SeqCnt2 += 1
                if inData == "3":
                    msgId = MsgId3
                    SeqCnt = SeqCnt3
                    SeqCnt3 += 1
                if inData == "e":
                    break

                data = msgId.to_bytes(4, 'big')
                data += SeqCnt.to_bytes(4, 'big')
                data += bytes(payload)
                crc = binascii.crc32(data)
                data += crc.to_bytes(4, 'big')
                print(data)
                conn.sendall(data)


if __name__ == '__main__':
    main()

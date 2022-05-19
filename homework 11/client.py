import socket

HOST = '127.0.0.1'
PORT = 55000


class SynchronizedPackage:
    def __init__(self, frame_a, frame_b, frame_c):
        self.frame_a = frame_a
        self.frame_b = frame_b
        self.frame_c = frame_c


class FramesBuffer:
    def __init__(self):
        self.buffer = []

    def push_synchronized_package(self, package: SynchronizedPackage):
        self.buffer.append(package)

        if len(self.buffer) > 3:
            self.buffer.pop(0)

    def print(self):

        for package in self.buffer:

            frame = package.frame_a
            msgId = int.from_bytes(frame[:4], "big")
            msgCount = int.from_bytes(frame[4:8], "big")

            print(f'Msg id {msgId}. Msg count {msgCount}. Frame {package}')

            frame = package.frame_b
            msgId = int.from_bytes(frame[:4], "big")
            msgCount = int.from_bytes(frame[4:8], "big")

            print(f'Msg id {msgId}. Msg count {msgCount}. Frame {package}')

            frame = package.frame_c
            msgId = int.from_bytes(frame[:4], "big")
            msgCount = int.from_bytes(frame[4:8], "big")

            print(f'Msg id {msgId}. Msg count {msgCount}. Frame {package}')
            print()


class FrameManager:
    def __init__(self):
        self.count = [0, 0, 0]
        self.frames = {0: [], 1: [], 2: []}

    def push_frame(self, frame):
        msg_id = int.from_bytes(frame[:4], "big") - 1
        self.frames[msg_id].append(frame)
        self.count[msg_id] += 1

    def get_synchronized_package(self) -> [SynchronizedPackage]:
        synchronized_packages = min(self.count)

        if synchronized_packages == 0:
            return []

        self.count = [x - synchronized_packages for x in self.count]

        result = []

        for _ in range(synchronized_packages):
            frame_a = self.frames[0].pop(0)
            frame_b = self.frames[1].pop(0)
            frame_c = self.frames[2].pop(0)

            result.append(SynchronizedPackage(frame_a, frame_b, frame_c))

        return result


def main():

    fm = FrameManager()
    buffer = FramesBuffer()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        while True:
            frame = s.recv(512)
            print('Client reveived message')

            msg_id = int.from_bytes(frame[:4], "big")
            print(frame)
            print(f'Message id: {msg_id}')

            fm.push_frame(frame)

            packages = fm.get_synchronized_package()

            for package in packages:
                buffer.push_synchronized_package(package)

            print('Synchronized packages')
            buffer.print()
            print()


if __name__ == '__main__':
    main()

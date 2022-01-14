import socket, pyaudio, queue, threading

# HOST = "192.168.43.118"
from time import sleep

HOST = "localhost"
PORT = 5634
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
BUFFER = 10 * 1024


class Client:
    def __init__(self, server_hostname: str = HOST, port: int = PORT):
        self.server_hostname = server_hostname
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER)
        self.audio_manager = pyaudio.PyAudio()
        self.queue = queue.Queue()

    def __enter__(self):
        self.stream = self.audio_manager.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                                              input=True, frames_per_buffer=CHUNK)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client_socket.close()

    def start(self):
        queue_add_thread = threading.Thread(target=self.add_frame)
        queue_add_thread.start()
        self.send_frames()

    def add_frame(self):
        while True:
            self.queue.put(self.stream.read(CHUNK))

    def send_frames(self):
        while True:
            data = self.queue.get()
            self.client_socket.sendto(data, (HOST, PORT))


def main():
    with Client(HOST, PORT) as client:
        client.start()


if __name__ == "__main__":
    main()

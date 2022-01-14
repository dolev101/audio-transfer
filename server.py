import socket, pyaudio, wave, argparse, queue, threading

# HOST = "192.168.43.118"
HOST = "localhost"
PORT = 5634
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 10
WAVE_OUT_FILENAME = "output.wav"
BUFFER = 10 * 1024


class Server:
    def __init__(self, server_hostname: str = HOST, port: int = PORT):
        self.server_hostname = server_hostname
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.audio_manager = pyaudio.PyAudio()

    def __enter__(self):
        self.server_socket.bind((self.server_hostname, self.port))
        self.stream = self.audio_manager.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                                              input=True, frames_per_buffer=CHUNK)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server_socket.close()

    # def get_frames(self):
    #     frames = []
    #     total_chunks = RATE // CHUNK * RECORD_SECONDS
    #     for _ in range(total_chunks + 1):
    #         data = self.stream.read(CHUNK)
    #         frames.append(data)
    #     return frames
    def start(self):

        while True:
            msg, client_address = self.server_socket.recvfrom(BUFFER)
            print(msg)


def main():
    with Server(HOST, PORT) as server:
        server.start()


if __name__ == "__main__":
    main()

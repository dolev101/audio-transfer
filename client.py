import socket, pyaudio, wave, argparse

HOST = "192.168.43.118"
PORT = 5634
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 10
WAVE_OUT_FILENAME = "output.wav"


class Client:
    def __init__(self, server_hostname: str = HOST, port: int = PORT):
        self.server_hostname = server_hostname
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.audio_manager = pyaudio.PyAudio()

    def __enter__(self):
        # self.client_socket.connect((self.server_hostname, self.port))
        self.stream = self.audio_manager.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                                              input=True, frames_per_buffer=CHUNK)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client_socket.close()

    def get_frames(self):
        frames = []
        total_chunks = RATE // CHUNK * RECORD_SECONDS
        for _ in range(total_chunks + 1):
            data = self.stream.read(CHUNK)
            frames.append(data)


def main():
    with Client(HOST, PORT) as client:
        print(client.get_frames())


if __name__ == "__main__":
    main()

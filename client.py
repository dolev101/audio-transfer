import socket
import pyaudio
import asyncio
# HOST = "192.168.43.118"

HOST = "192.168.43.118"
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
        self.audio_manager = pyaudio.PyAudio()
        self.queue = asyncio.Queue()

    def __enter__(self):
        self.stream = self.audio_manager.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                                              input=True, frames_per_buffer=CHUNK)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client_socket.close()

    async def start(self):
        while True:
            await self.add_frame()
            await self.send_frame()

    async def add_frame(self):
        await self.queue.put(bytes([b % 256 for b in self.stream.read(CHUNK)]))

    async def send_frame(self):
        data = await self.queue.get()
        self.client_socket.sendto(data, (HOST, PORT))

    @staticmethod
    def clump(i: int, ceiling: int):
        if i >= ceiling:
            return ceiling
        return i


def main():
    with Client(HOST, PORT) as client:
        asyncio.run(client.start())


if __name__ == "__main__":
    main()

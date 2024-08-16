import socket
import random
import hashlib

# Parámetros básicos
CHUNK_SIZE = 512  # Tamaño del segmento en bytes

class Client:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port

    def read_file(self, filename):
        with open(filename, 'rb') as f:
            return f.read()

    def create_segments(self, data):
        segments = [data[i:i + CHUNK_SIZE] for i in range(0, len(data), CHUNK_SIZE)]
        return segments

    def introduce_errors(self, segments):
        # Enviar fuera de orden
        random.shuffle(segments)

        # Pérdida aleatoria de paquetes
        segments = [seg for seg in segments if random.random() > 0.1]  # 10% de pérdida

        # Corrupción de datos (cambio de bits)
        corrupted_segments = []
        for seg in segments:
            if random.random() < 0.1:  # 10% de probabilidad de corrupción
                seg = bytearray(seg)
                random_byte = random.randint(0, len(seg) - 1)
                seg[random_byte] ^= 0xFF  # Invertir los bits de un byte aleatorio
                seg = bytes(seg)
            corrupted_segments.append(seg)
        return corrupted_segments

    def send_segments(self, segments):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            for i, seg in enumerate(segments):
                checksum = hashlib.md5(seg).hexdigest()
                s.sendto(f"{i}|{checksum}".encode() + seg, (self.server_ip, self.server_port))

    def send_file(self, filename):
        data = self.read_file(filename)
        segments = self.create_segments(data)
        segments = self.introduce_errors(segments)
        self.send_segments(segments)
#### Servidor
# El servidor recibe los segmentos, los reordena, verifica la integridad y reconstruye el archivo.
import socket
import hashlib

class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.received_segments = {}

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((self.ip, self.port))
            print(f"Servidor escuchando en {self.ip}:{self.port}")

            while True:
                print("Esperando segmentos...")
                data, addr = s.recvfrom(1024)
                index, checksum = data.decode().split('|', 1)
                segment = data[len(index) + len(checksum) + 2:]
                print(f"Segmento {index} recibido")
                if hashlib.md5(segment).hexdigest() == checksum:
                    self.received_segments[int(index)] = segment
                    print(f"Segmento {index} recibido correctamente")
                else:
                    print(f"Segmento {index} corrupto recibido")

                # Simulación simple para terminar después de recibir un número específico de segmentos
                if len(self.received_segments) >= 10:  # Esto debe ajustarse según el tamaño del archivo
                    break

            self.reorder_segments()

    def reorder_segments(self):
        sorted_segments = [self.received_segments[i] for i in sorted(self.received_segments.keys())]
        self.save_file(b''.join(sorted_segments))

    def save_file(self, data):
        with open("received_file.txt", 'wb') as f:
            f.write(data)
        print("Archivo guardado como 'received_file.txt'")
"""
Testing Algorithm Socket Only - Not used in production.
"""
import socket

# from misc.config import FORMAT, ALGO_SOCKET_BUFFER_SIZE, WIFI_IP, PORT

# Wifi IP: RPI's ip address -> 192.168.12.12
# Port: 5050

FORMAT = "UTF-8"
ALGO_SOCKET_BUFFER_SIZE = 1024
# WIFI_IP = "192.168.68.110"
# WIFI_IP = "192.168.2.145"
WIFI_IP = "192.168.0.189"
# WIFI_IP = "localhost" # Use this for easier testing if server is in same environment
PORT = 5050


class AlgoClient:

    def __init__(self, server_ip=WIFI_IP, server_port=PORT) -> None:
        print("[Algo Client] Initilising Algo Client.")
        self.client_socket = None
        self.server_address = (server_ip, server_port)
        print("[Algo Client] Client has been initilised.")

    def connect(self) -> bool:
        while True:
            try:
                # Connect to RPI via TCP
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((WIFI_IP, PORT))
                return True
            except Exception as error:
                print(f'[Algo] Failed to connect to Algorithm Server at {self.server_address}')
                print(f"[Error Message]: {error}")
                return False

    def disconnect(self) -> bool:
        try:
            if self.client_socket is not None:
                self.client_socket.close()
                self.client_socket = None
        except Exception as error:
            print(f'[Algo] Failed to disconnect from Algorithm Server at {self.server_address}')
            print(f"[Error Message]: {error}")
            return False
        return True

    def recv(self) -> str:
        try:
            # Decode : Converting from Byte to UTF-8 format.
            message = self.client_socket.recv(ALGO_SOCKET_BUFFER_SIZE).strip().decode(FORMAT)
            if len(message) > 0:
                print(f'[Algo] Received Message from Algo Server: {message}')
                return message
            return None
        except Exception as error:
            print("[Algo] Failed to receive message from Algo Server.")
            print(f"[Error Message]: {error}")
            raise error

    def send(self, message) -> str:
        try:
            print(f'[Algo] Message to Algo Server: {message}')
            self.client_socket.send(message.encode(FORMAT))

        except Exception as error:
            print("[Algo] Failed to send to Algo Server.")
            print(f"[Error Message]: {error}")
            raise error


# Standalone testing.
if __name__ == '__main__':
    client = AlgoClient()
    client.connect()

    while True:
        message = input("[Client] Send Message to server: ")
        client.send(message)
        received = client.recv()
        if received is not None:
            print(f"[Server] Received message from client: {received}")

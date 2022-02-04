import queue
import socket
import threading

# Encoding / Decoding Format
FORMAT = "utf-8"
ALGO_SOCKET_BUFFER_SIZE = 1024


class Communication:
    def __init__(self):
        self.ip_address = "192.168.2.1"
        self.port = 5050
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = None
        self.addr = None
        self.message = "Connected"
        # self.s.connect((self.ip_address, self.port))
        self.message_sender = threading.Thread(target=self.message_sender_thread)
        self.message_receiver = threading.Thread(target=self.message_receiver_thread)
        # self.printer = threading.Thread(target=self.print_messages)
        print("[RPI] Receiver Thread started")
        self.message_receiver.start()
        print("[RPI] Sender Thread started")
        self.message_sender.start()

    def connect(self):
        # try:
        self.s.bind((self.ip_address, self.port))
        self.s.listen(10)
        self.client_socket, self.addr = self.s.accept()
        print(self.message)
        # except Exception as e:
        #     print(e)

    def message_sender_thread(self) -> None:
        # We want to encode into bytes.
        while True:
            try:
                msg = input("[RPI] Message to server: ")
                message = msg.encode(FORMAT)
                # Pad to Socket buffer size
                # message += (ALGO_SOCKET_BUFFER_SIZE - len(message)) * b' '
                self.s.send(message)
                print(f"[RPI] Message Sent: {msg}")
            except Exception as e:
                print(e)

    def message_receiver_thread(self) -> None:
        while True:
            try:
                message = self.s.recv(ALGO_SOCKET_BUFFER_SIZE).decode(FORMAT)
                print(message)
            except Exception as e:
                print(e)

    def print_messages(self) -> None:
        while True:
            try:
                # msg = self.incoming_message_queue.get_nowait()
                print("msg")
            except queue.Empty:
                pass


# Standalone testing.
if __name__ == '__main__':
    comms = Communication()
    comms.connect()

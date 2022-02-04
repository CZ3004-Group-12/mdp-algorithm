import queue
import socket
import threading

WIFI_IP = "192.168.2.145"
PORT = 5050

# Encoding / Decoding Format
FORMAT = "utf-8"
ALGO_SOCKET_BUFFER_SIZE = 1024


class Communication:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((WIFI_IP, PORT))
        self.message_sender = threading.Thread(target=self.message_sender_thread)
        self.message_receiver = threading.Thread(target=self.message_receiver_thread)
        # self.printer = threading.Thread(target=self.print_messages)
        print("[RPI] Receiver Thread started")
        self.message_receiver.start()
        print("[RPI] Sender Thread started")
        self.message_sender.start()

        def message_sender_thread(self) -> None:
            # We want to encode into bytes.
            while True:
                try:
                    msg = input("[RPI] Message to server: ")
                    message = msg.encode(FORMAT)
                    # Pad to Socket buffer size
                    # message += (ALGO_SOCKET_BUFFER_SIZE - len(message)) * b' '
                    self.client.send(message)
                    print(f"[RPI] Message Sent: {msg}")
                except Exception as e:
                    print(e)

        def message_receiver_thread(self) -> None:
            while True:
                try:
                    message = self.client.recv(ALGO_SOCKET_BUFFER_SIZE).decode(FORMAT)
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
    Communication()

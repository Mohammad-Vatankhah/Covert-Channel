import time
import threading

class Sender:
    def __init__(self):
        self.bits = ""

    def send_bit(self, bit):
        if bit == '1':
            time.sleep(0.1)
        else:
            time.sleep(0.05)

    def send_binary(self, binary_str, event):
        self.bits = binary_str
        self.start_time = time.time()
        for bit in self.bits:
            self.send_bit(bit)
            event.set()
            event.clear()
        self.end_time = time.time()

class Receiver:
    def __init__(self):
        self.received_bits = ""
        self.start_time = None
        self.end_time = None

    def receive_bit(self, event):
        start_time = time.time()
        event.wait(0.15)
        end_time = time.time()
        if end_time - start_time > 0.1:
            self.received_bits += '1'
        else:
            self.received_bits += '0'

    def receive_binary(self, event, bits_count):
        self.start_time = time.time()
        while len(self.received_bits) < bits_count:
            self.receive_bit(event)
        self.end_time = time.time()

    def get_speed(self):
        return len(self.received_bits) / (self.end_time - self.start_time)

sender = Sender()
receiver = Receiver()

binary_str = "11001010"
event = threading.Event()

sender_thread = threading.Thread(target=sender.send_binary, args=(binary_str, event))
receiver_thread = threading.Thread(target=receiver.receive_binary, args=(event, len(binary_str)))

sender_thread.start()
receiver_thread.start()

sender_thread.join()
receiver_thread.join()

print("Sent:", binary_str)
print("Received:", receiver.received_bits)
print("Receiver Speed (bits/second):", receiver.get_speed())

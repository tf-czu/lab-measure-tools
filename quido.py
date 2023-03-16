"""
    TODO
"""

import serial
import time

class Quido:
    def __init__(self, port, rate=115200, read_timeout=1):
        self.read_timeout = read_timeout
        self.ser = serial.Serial(port, rate, parity=serial.PARITY_NONE, timeout=0.1)
        assert self.ser.isOpen()
        time.sleep(0.5)
        self.open_relays()

    def sent_cmd(self, cmd, read_response=True):
        cmd = cmd+"\r"
        self.ser.write(cmd.encode())
        if read_response:
            return self.ser_read()
        return

    def ser_read(self):
        t0 = time.time()
        data = b""
        while True:
            d = self.ser.read(128)
            if len(d)>0:
                data += d
            if b"\r" in data:
                return data.decode()
            if time.time() - t0 > self.read_timeout:
                return None

    def relay_set(self, relay_id, instruction, task):
        prefix = "*B1"
        cmd = prefix+instruction+relay_id+task
        response = self.sent_cmd(cmd)
        assert "*B10" in response, response
        return

    def open_relays(self):
        for ii in range(1, 5):
            instruction = "OS"
            relay_id = str(ii)
            task = "L"
            self.relay_set(relay_id, instruction, task)
        return

    def snend_ack(self):
        response = self.sent_cmd("*B$IR1")
        assert response is not None


if __name__ == "__main__":
    pass

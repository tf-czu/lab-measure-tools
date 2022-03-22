"""
    TODO
"""
import time
import serial
from threading import Thread
from appJar import gui

PORT = "/dev/ttyUSB0"
RATE = 2_000_000

class Pendulum:
    def __init__(self):
        self.ser = None
        self.stop = False

    def init_ser(self):
        if self.ser is None:
            self.ser = serial.Serial(PORT, RATE, parity=serial.PARITY_NONE, timeout=0.02)
        return

    def record(self):
        self.data = []
        while not self.stop:
            raw_data = self.ser.read(32)
            print(raw_data)
            self.data.append(raw_data)
        self.ser = None
        return


def onButton_record(buttonName):
    pendulum.stop = False
    pendulum.init_ser()
    app.setMessage("mess", "Recording..")
    Thread(target=pendulum.record, daemon=True).start()

def onButton_stop(buttonName):
    pendulum.stop = True
    app.setMessage("mess", "")
    time.sleep(1)
    print(pendulum.data)
    print(pendulum.ser)

pendulum = Pendulum()
app = gui()
#app.setSticky("news")

app.setResizable(canResize=False)
app.addButton("Record", onButton_record, row=1, column=0)
app.addButton("Stop", onButton_stop, row=1, column=1)
app.addMessage("mess", "", row=2, column=0, colspan=2)
app.go()

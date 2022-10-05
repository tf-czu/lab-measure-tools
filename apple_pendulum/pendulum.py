"""
    TODO
"""
import time
import serial
from threading import Thread
from matplotlib import pyplot as plt
import datetime
import csv
import os

from appJar import gui
from launcher import Launch

PORT = "/dev/ttyUSB0"
RATE = 2000000

g_rate = "44100"  # 96000
g_arecord_command = ["arecord", "-r", g_rate, "tmp/test.wav"]
g_mic_recorder = None
g_measure_label = ""



class Pendulum:
    def __init__(self):
        self.ser = None
        self.stop = False
        self.buf = b''

    def init_ser(self):
        if self.ser is None:
            self.ser = serial.Serial(PORT, RATE, parity=serial.PARITY_NONE, timeout=0.02)
        return

    def record(self):
        self.buf = b''
        while not self.stop:
            raw_data = self.ser.read(32)
#            print(raw_data)
            self.buf = self.buf + raw_data
        self.ser = None
        return
        

def parse_rawdata(rawdata):
    ret = []
    numbers = rawdata.split(b'\r\n')
#    print(rawdata)
#    print(numbers)
    for num in numbers:
        num = num.decode()
        if num.replace("-","1").isnumeric():
            ret.append(int(num))
    return ret

def show_data(data):
    plt.plot(data)
    plt.show()

def onButton_record(buttonName):
    global g_mic_recorder
    global g_measure_label
    command = g_arecord_command
    g_measure_label = app.getEntry("label")
    print(g_measure_label)
    wav_name = datetime.datetime.now().strftime(f"apple_{g_measure_label}_%H%M%S.wav")
    wav_path = os.path.join("wav", wav_name)
    
    pendulum.stop = False
    pendulum.init_ser()
    if g_mic_recorder is None:
        command[3] = wav_path
        g_mic_recorder = Launch(command)
        
    time.sleep(1)
    app.setMessage("mess", f"Recording..\n{g_measure_label}")
    
    Thread(target=pendulum.record, daemon=True).start()
    g_mic_recorder.start()


def onButton_stop(buttonName):
    pendulum.stop = True
    g_mic_recorder.quit()
    app.setMessage("mess", "")
    time.sleep(1)
#    print(pendulum.data)
#    print(pendulum.ser)
    if len(pendulum.buf) > 0:
        data = parse_rawdata(pendulum.buf)
#        print(data)
        csv_name = datetime.datetime.now().strftime(os.path.join("data",f"pendulum_{g_measure_label}_%y%m%d_%H%M%S.csv"))
        with open(csv_name, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",")
            for num in data:
               csv_writer.writerow([num])
        show_data(data)
        pendulum.buf = b""
        
    return

pendulum = Pendulum()
app = gui()
#app.setSticky("news")

app.setResizable(canResize=False)
app.addButton("Record", onButton_record, row=1, column=0)
app.addButton("Stop", onButton_stop, row=1, column=1)
app.addEntry("label", row=2)
app.addMessage("mess", "", row=3, column=0, colspan=2)
app.go()


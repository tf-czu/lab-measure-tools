"""
    Dielectric properties measurement sequence via GW Instek LCR-8110G
        Usage: sudo python3 LCR_remote_control.py <swith> <label>
            switch: soil
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import os
import serial
import time
import datetime

PORT = "/dev/ttyUSB0"
RATE = 9600
MAJOR_FUNC = [ "C", "L", "X", "B", "Z", "Y" ]
MINOR_FUNC = [ "Q", "D", "R", "G" ]


class LCR_8110G:
    def __init__(self):
        self.ser = serial.Serial(PORT, RATE, parity = serial.PARITY_NONE, timeout = 0.2)
        print(self.ser.name)
        print( "Serial port is open: ", self.ser.isOpen())
        time.sleep(0.5)
        self.ser.write("*idn?\n".encode())
        time.sleep(0.5)
        outPut = None
        outPut = self.ser.read(128)
        outPut = outPut.decode("utf-8")
        if "GW INSTEK" not in outPut:
            print("LCR is not connected")
            self.ser.close()
            sys.exit()
        print(outPut)

    def sentCMD(self, cmd, timeout = 0.2):
        cmd = cmd+"\n"
        self.ser.write(cmd.encode())
        time.sleep(timeout)
        outPut = self.ser.read(128)
        if len(outPut) == 0:
            return None
        return outPut


    def setFreq(self, freq):
        if type(freq) != str:
            return False
        cmd = ":meas:freq "+freq
        outPut = self.sentCMD(cmd)
        return outPut


    def setFunc(self, major, minor = None):
        if (type(major) != str):
            return False
        if minor is not None:
            if (type(major) != str):
                return False
            cmd = ":meas:func:"+major+";"+minor
        else:
            cmd = ":meas:func:"+major
        outPut = self.sentCMD(cmd)
        return outPut


    def readFunc(self):
        majorF = None
        minorF = None
        cmd = ":meas:func:major?"
        major = self.sentCMD(cmd)
        if major is not None:
            majorF = MAJOR_FUNC[int(major)]
        cmd = ":meas:func:minor?"
        minor = self.sentCMD(cmd)
        if minor is not None:
            minorF = MINOR_FUNC[int(minor)]

        return majorF, minorF


    def readFreq(self):
        cmd = ":meas:freq?"
        outPut = self.sentCMD(cmd)
        if outPut is not None:
            return float(outPut)
        return None


    def trig(self):
        cmd = ":meas:trig"
        outPut = self.sentCMD(cmd, timeout = 3)
        if outPut is not None:
            outPut = outPut.split(b',')
            return [ float(x) for x in outPut ]
        return None


    def __del__(self):
        self.ser.close()


def soilSample(label):
    freq_list = [1e5, 2e5, 5e5, 1e6, 2e6, 5e6]
    #freq_list = [1e4]
    logDir = datetime.datetime.now().strftime("logs/soil_%y%m%d")
    if not os.path.isdir(logDir):
        os.mkdir(logDir)
    timeID = datetime.datetime.now().strftime("_%H%M%S")
    log_fileN = os.path.join(logDir, "soil_"+label+timeID+".txt")
    log = open(log_fileN, "w")

    # LCR seting
    lcr = LCR_8110G()
    log.write("Frequency [Hz], Capacitance [F], Dissipation factor [-], Impedance [ohm], Angle [deg]\r\n")
    log.flush()

    for f in freq_list:
        lcr.setFreq(str(f))
        set_freq = lcr.readFreq()
        lcr.setFunc("c", "d")
        C, D = lcr.trig()
        lcr.setFunc("z")
        Z, A = lcr.trig()
        print("f = %.1E Hz, C = %.4E F, D = %.4E, Z = %.4E, A = %f" %(set_freq, C, D, Z, A) )
        log.write("%.1E Hz, %.4E, %.4E, %.4E, %f\r\n" %(set_freq, C, D, Z, A) )
        log.flush()
    log.close()
    print("Measurement completed")


if __name__ == "__main__": 
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit()
    switch = sys.argv[1]
    label = sys.argv[2]
    if switch == "soil":
        soilSample(label)

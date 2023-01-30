"""
    Dielectric properties measurement sequence via GW Instek LCR-8110G
"""


import os
import serial
import time
import datetime
import csv


def get_log_path(label):
    log_dir = datetime.datetime.now().strftime("logs/lcr_%y%m%d")
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    timeID = datetime.datetime.now().strftime("_%H%M%S")

    return os.path.join(log_dir, f"{label}_{timeID}.csv")


class LCR_8110G:
    def __init__(self, port, rate = 9600, read_timeout = 5):
        self.read_timeout = read_timeout
        self.major_funcs = [ "C", "L", "X", "B", "Z", "Y" ]
        self.minor_funcs = [ "Q", "D", "R", "G" ]
        self.ser = serial.Serial(port, rate, parity = serial.PARITY_NONE, timeout = 0.05)
        assert self.ser.isOpen()
        time.sleep(0.5)
        output = self.sent_cmd("*idn?")
        assert "GW INSTEK" in output, f"LCR is not connected: {output}"


    def sent_cmd(self, cmd):
        cmd = cmd+"\n"
        self.ser.write(cmd.encode())

        return self.ser_read()


    def ser_read(self):
        t0 = time.time()
        data = b""
        while True:
            d = self.ser.read(128)
            if len(d)>0:
                data += d
            if b"\n" in data:
                return data.decode()
            if time.time() - t0 > self.read_timeout:
                return None


    def set_freq(self, freq):
        assert type(freq) == str, freq
        cmd = f":meas:freq {freq}"
        return self.sent_cmd(cmd)


    def set_func(self, major, minor = None):
        assert type(major) == str, major
        if minor is not None:
            assert type(minor) == str, minor
            cmd = ":meas:func:"+major+";"+minor
        else:
            cmd = ":meas:func:"+major

        return self.sent_cmd(cmd)


    def read_func(self):
        major_func = None
        minor_func = None
        cmd = ":meas:func:major?"
        major = self.sent_cmd(cmd)
        if major is not None:
            major_func = self.major_funcs[int(major)]
        cmd = ":meas:func:minor?"
        minor = self.sent_cmd(cmd)
        if minor is not None:
            minor_func = self.minor_funcs[int(minor)]

        return major_func, minor_func


    def read_freq(self):
        cmd = ":meas:freq?"
        output = self.sent_cmd(cmd)
        if output is not None:
            return float(output)
        return None


    def trig(self):
        cmd = ":meas:trig"
        output = self.sent_cmd(cmd)
        if output is not None:
            output = output.split(',')
            return [ float(x) for x in output ]
        return None


    def close(self):
        self.ser.close()

    # context manager functions
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def soilSample(label, port):
    freq_list = [1e5, 2e5, 5e5, 1e6, 2e6, 5e6]
    #freq_list = [1e4]
    logDir = datetime.datetime.now().strftime("logs/soil_%y%m%d")
    if not os.path.isdir(logDir):
        os.mkdir(logDir)
    timeID = datetime.datetime.now().strftime("_%H%M%S")
    log_fileN = os.path.join(logDir, "soil_"+label+timeID+".txt")
    log = open(log_fileN, "w")

    # LCR seting
    lcr = LCR_8110G(port)
    log.write("Frequency [Hz], Capacitance [F], Dissipation factor [-], Impedance [ohm], Angle [deg]\r\n")
    log.flush()

    for f in freq_list:
        lcr.set_freq(str(f))
        set_freq = lcr.read_freq()
        lcr.set_func("c", "d")
        C, D = lcr.trig()
        lcr.set_func("z")
        Z, A = lcr.trig()
        print("f = %.1E Hz, C = %.4E F, D = %.4E, Z = %.4E, A = %f" %(set_freq, C, D, Z, A) )
        log.write("%.1E Hz, %.4E, %.4E, %.4E, %f\r\n" %(set_freq, C, D, Z, A) )
        log.flush()
    log.close()
    print("Measurement completed")


def continuous_measurement(label, port, freq, major_func, minor_func):
    log_path = get_log_path(label)
    with LCR_8110G(port) as lcr:
        lcr.set_freq(freq)
        lcr.set_func(major_func, minor_func)
        with open(log_path, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerow(["time (ms)", major_func, minor_func])
            t0 = time.time()
            while True:
                data = lcr.trig()
                csv_writer.writerow([(time.time() - t0)*1000] + data)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='__doc__')
    parser.add_argument('task', help='Specify a type of measurement - available: soil, continuous')
    parser.add_argument('--port', help='Specify serial port', default="/dev/ttyUSB0")
    parser.add_argument('--label', help='Specify a measurement label', default="")
    parser.add_argument('--freq', help='Specify a measurement frequencies', default="1e5")
    parser.add_argument('--major_func', help='Specify a major function')
    parser.add_argument('--minor_func', help='Specify a minor function')


    args = parser.parse_args()

    label = args.label
    port = args.port
    if args.task == "soil":
        soilSample(label, port)

    elif args.task == "continuous":
        freq = args.freq
        major_func = args.major_func
        minor_func = args.minor_func
        continuous_measurement(label, port, freq, major_func, minor_func)

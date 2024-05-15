import sys
import datetime
import csv
import subprocess
import time

from LCR_gwinstek.LCR_remote_control import LCR_8110G
from quido import Quido

NUM_MEASUREMENTS = 3*24*10

def main():
    t1 = None
    for jj in range(NUM_MEASUREMENTS):
        if t1 is None:
            t1 = datetime.datetime.now() + datetime.timedelta(minutes=1)
        else:
            t1 += datetime.timedelta(minutes=10)
        relay = Quido(port="/dev/quido1")
        light = Quido(port="/dev/quido2")
        
        with open("data.csv", "a", newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",")
            with LCR_8110G("/dev/ttyS0") as lcr:
                lcr.set_freq("1e5")
                lcr.set_func("c", "d")
                for ii in range(1, 5):
                    relay_id = str(ii)
                    relay.relay_set(relay_id, "OS", "H")
                    C, D = lcr.trig()
                    time_id = datetime.datetime.now().strftime("%H%M%S")
                    print(time_id, C, D)
                    csv_writer.writerow([time_id, relay_id, C, D])
                    relay.relay_set(relay_id, "OS", "L")
                    
        # take picture
        light.relay_set("1", "OS", "H")
        light.relay_set("2", "OS", "H")
        subprocess.Popen(["gphoto2", "--capture-image-and-download", "--filename", f"seed_el/images/im_{jj:05d}.jpg"])
        time.sleep(5)
        light.relay_set("1", "OS", "L")
        light.relay_set("2", "OS", "L")
        
        while t1 > datetime.datetime.now():
            time.sleep(10)
            # keep communication
            relay.snend_ack()
            light.snend_ack()

    print("Measurement completed")


if __name__ == "__main__":
    main()

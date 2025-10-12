"""
    QR code dist detector
"""
import numpy as np

from osgar.node import Node

class QrDist(Node):
    def __init__(self, config, bus):
        super().__init__(config, bus)
        bus.register('qr_dist')
        self.bus = bus
        self.counter = 0
        self.verbose = False
        self.qr_pose = None

    def on_qr_data(self, data):
        print(data)

    def on_depth(self, depth):
        if self.qr_pose:
            print(depth[self.qr_pose])
            self.qr_pose = None

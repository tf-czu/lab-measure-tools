import os
import rosbag
import cv2
import numpy as np


def read_rosbag(bagfile, rgb_topic, out_dir):
    bag = rosbag.Bag(bagfile)
    topics = []
    subsample = 10
    ii = 0
    for topic, msg, t in bag.read_messages():
        if topic not in topics:
            topics.append(topic)
        if rgb_topic and topic == rgb_topic:
            image = np.ndarray(shape=(msg.height, msg.width, 3), dtype=np.uint8, buffer=msg.data)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if ii%subsample == 0:
                impath = os.path.join(out_dir, f"im_{ii:05d}.png")
                cv2.imwrite(impath, image)
            ii += 1

    bag.close()

    print("Seznam témat:")
    for topic in topics:
        print(topic)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='__doc__')
    parser.add_argument('bagfile', help='Path to rosbag')
    parser.add_argument('--rgb', help='Specify a rgb topic')
    parser.add_argument("--out", help="Out dir", default="tmp")
    args = parser.parse_args()

    read_rosbag(args.bagfile, args.rgb, args.out)

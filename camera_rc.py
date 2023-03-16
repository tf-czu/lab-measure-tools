"""
    Tools for camera remote control
"""

import logging
import os
import subprocess
import sys
import time

import gphoto2 as gp

PATH_PC = "logs_images"
ERR_FILE = "err.log"
errLog = None  # TODO


class Canon:
    def __init__(self):
        logging.basicConfig(
            format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
        gp.check_result(gp.use_python_logging())
        self.context = gp.gp_context_new()
        self.camera = gp.check_result(gp.gp_camera_new())
        gp.check_result(gp.gp_camera_init(self.camera, self.context))

    """
    def __del__(self):
        gp.check_result(gp.gp_camera_exit(self.camera, self.context))
    """

    def take_pic(self, fileName):

        for ii in range(5):
            try:
                # gp.check_result(gp.use_python_logging())
                # context = gp.gp_context_new()
                # camera = gp.check_result(gp.gp_camera_new())
                # gp.check_result(gp.gp_camera_init(camera, self.context))
                """
                camera_config = gp.check_result( gp.gp_camera_get_config(camera, context))
                shutterspeed = gp.check_result(gp.gp_widget_get_child_by_name(camera_config, 'shutterspeed'))
                value = gp.check_result(gp.gp_widget_get_choice(shutterspeed, shutterspeed_value))
                print('shutterspeed: ', value )#, type(value))
                gp.check_result(gp.gp_widget_set_value(shutterspeed, value))

                aperture = gp.check_result(gp.gp_widget_get_child_by_name(camera_config, 'aperture'))
                value = gp.check_result(gp.gp_widget_get_choice(aperture, aperture_value))
                print('aperture: ', value )#, type(value))
                gp.check_result(gp.gp_widget_set_value(aperture, value))

                gp.check_result(gp.gp_camera_set_config(camera, camera_config, context))
                """
                print('Capturing image')
                file_path = gp.check_result(gp.gp_camera_capture(
                    self.camera, gp.GP_CAPTURE_IMAGE, self.context))
                print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
                target = fileName + "." + file_path.name.split(".")[-1]
                print('Copying image to', target)
                camera_file = gp.check_result(gp.gp_camera_file_get(
                    self.camera, file_path.folder, file_path.name,
                    gp.GP_FILE_TYPE_NORMAL, self.context))
                gp.check_result(gp.gp_file_save(camera_file, target))
                # subprocess.call(['xdg-open', target])
                time.sleep(0.1)
                # gp.check_result(gp.gp_camera_exit(camera, self.context))
                break
            except Exception as e:
                print("error: " + str(e))
                time.sleep(1)
                # gp.check_result(gp.gp_camera_exit(camera, context))

    def set_camera(self, shutterspeed_value, aperture_value):
        for ii in range(5):
            try:
                # gp.check_result(gp.use_python_logging())
                # context = gp.gp_context_new()
                # camera = gp.check_result(gp.gp_camera_new())
                # gp.check_result(gp.gp_camera_init(camera, self.context))

                camera_config = gp.check_result(gp.gp_camera_get_config(self.camera, self.context))
                shutterspeed = gp.check_result(gp.gp_widget_get_child_by_name(camera_config, 'shutterspeed'))
                # value = gp.check_result(gp.gp_widget_get_choice(shutterspeed, shutterspeed_value)) ??
                print('shutterspeed: ', shutterspeed_value)  # , type(value))
                gp.check_result(gp.gp_widget_set_value(shutterspeed, shutterspeed_value))

                aperture = gp.check_result(gp.gp_widget_get_child_by_name(camera_config, 'aperture'))
                # value = gp.check_result(gp.gp_widget_get_choice(aperture, aperture_valu)) ??
                print('aperture: ', aperture_value)  # , type(value))
                gp.check_result(gp.gp_widget_set_value(aperture, aperture_value))

                gp.check_result(gp.gp_camera_set_config(self.camera, camera_config, self.context))
                time.sleep(0.1)
                # gp.check_result(gp.gp_camera_exit(camera, context))
                break
            except Exception as e:
                print("error: " + str(e))
                time.sleep(1)
                # gp.check_result(gp.gp_camera_exit(camera, context))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit()

    camera = Canon()
    if sys.argv[1] == "set":
        shutterspeed_value = sys.argv[2]
        aperture_value = sys.argv[3]
        camera.set_camera(shutterspeed_value, aperture_value)
    else:
        fileName = os.path.join(PATH_PC, sys.argv[1])
        camera.take_pic(fileName)

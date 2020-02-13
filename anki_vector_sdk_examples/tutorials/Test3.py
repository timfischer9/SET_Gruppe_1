#!/usr/bin/env python
import time

import anki_vector


def main():
    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial,
                           show_viewer=True,
                           show_3d_viewer=True,
                           enable_face_detection=True,
                           enable_custom_object_detection=True,
                           enable_nav_map_feed=True):
        print("Starting 3D Viewer. Use Ctrl+C to quit.")
        try:
            while True:
                time.sleep(0.5)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()

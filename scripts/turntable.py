#!/usr/bin/python

import sys
import fileinput
import subprocess
import os
import scene
import argparse


def turntable(name, step):
    name = 'finals/' + name
    frame = 0
    for r in range(0, 360, step):
        frame_name = name + str(frame).zfill(4)
        scene.main(frame_name, r, True)
        print('Finished frame ' + str(frame))
        frame += 1

    subprocess.call([
        'ffmpeg', '-framerate', '25', '-i', name + '%04d.tiff',
        '-vcodec', 'libx264', '-pix_fmt', 'yuv420p', 'finals/out.mp4'
        ])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--step', type=int, default=30,
                        help='The rate of change of rotation per frame')
    args = parser.parse_args()
    turntable(name="scene", step=args.step)


if __name__ == "__main__":

    sys.exit(main())

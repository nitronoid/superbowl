#!/usr/bin/python

import sys
import fileinput
import subprocess
import os
import scene
import argparse


def turntable(name, step, env, start_rot):
    name = 'finals/' + name
    frame = 0
    for r in range(0, 360, step):
        frame_name = name + str(frame).zfill(4)
        scene.scene(frame_name, (r + start_rot) % 360, 0, True)
        print('Finished frame ' + str(frame))
        frame += 1

    if env:
        for r in range(0, 360, step):
            frame_name = name + str(frame).zfill(4)
            scene.scene(frame_name, start_rot, r, True)
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
    parser.add_argument('-e', '--environment', type=bool, default=False,
                        help='Rotate the environment as well as the model')
    parser.add_argument('-i', '--initial', type=float, default=180,
                        help='Initial rotation')
    args = parser.parse_args()
    turntable(name="scene", step=args.step, env=args.environment, start_rot=args.initial)


if __name__ == "__main__":
    sys.exit(main())


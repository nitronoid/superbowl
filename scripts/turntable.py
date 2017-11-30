import sys
import fileinput
import subprocess
import os


def output(name, data):
    f = open(name, 'w')
    f.write(data)
    f.close()


def turntable(name, step, name_token, rotate_token):
    # Read in the file
    f = open(name, 'r')
    filedata = f.read()
    f.close()

    frame = 0
    for r in range(0, 360, step):
        # Replace the target string and write the file out again
        name_raw = os.path.splitext(name)[0]
        new_name = name_raw + str(frame).zfill(4)
        renderfile = filedata.replace(rotate_token, str(r)).replace(name_token, new_name)
        output(name, renderfile)
        subprocess.call(['render', name])
        print('Finished frame ' + new_name)
        frame += 1

    output(name, filedata)
    subprocess.call(['ffmpeg', '-framerate', '25', '-i', 'finals/' + name_raw + '%04d.tiff', '-vcodec', 'libx264', '-pix_fmt', 'yuv420p', 'out.mp4'])


def main():
    turntable(name="scene.rib", step=1, name_token='NAME', rotate_token='RX')


if __name__ == "__main__":

    sys.exit(main())
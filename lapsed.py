import cronus.beat as beat
import shutil
import os
import os.path
import subprocess
import sys
from datetime import datetime


date_format = "%Y-%m-%d"
timestamp_format = "%H:%M:%S"

scrot_quality = 75
screenshot_rate = 10

def capture(directory):

    if not os.path.exists(directory):
        os.makedirs(directory)

    print "Screenshotting every %d seconds..." % screenshot_rate
    beat.set_rate(1.0/screenshot_rate)
    index = 0
    while beat.true():
        try:
            now = datetime.now()
            timestamp = datetime.strftime(now, timestamp_format)
            filename = "%08d.jpg" % index
            path = os.path.join(directory, filename)
            subprocess.call(["scrot", "-q", str(scrot_quality), path])
            annotate_image(directory, filename, timestamp)
            index += 1
            beat.sleep()
        except KeyboardInterrupt:
            print "Encoding..."
            encode(directory)
            sys.exit(0)


def annotate_image(directory, filename, text):
    subprocess.call(["convert", os.path.join(directory, filename),
        "-pointsize", "48",
        "-fill", "white",
        "-undercolor", "#00000080",
        "-gravity", "SouthEast",
        "-annotate", "0", text,
        os.path.join(directory, filename)])


def encode(directory):
    subprocess.call(["ffmpeg", "-y",
                     "-r", "10.0",
                     "-f", "image2",
                     "-i", "%s/%%08d.jpg" % directory,
                     "-i", "epicsax.mp3",
                     "-shortest",
                     "-vcodec", "libx264",
                     "-qscale:v", "5",
                     "-vf", "scale=1024:768",
                     "%s.mp4" % directory])


if __name__ == '__main__':
    if len(sys.argv) == 2:
        capture(sys.argv[1])
    else:
        print("Usage: lapsed.py [filename]")


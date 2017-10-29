#!/bin/python
##################################
# Simple Raspberry Pi Photo Booth
##################################


# Imports
import datetime, os, time
from time import sleep
import RPi.GPIO as GPIO

# Variables
pin_camera_btn = 21  # pin that the button is attached to
screen_w = 800  # resolution of the photo booth display
screen_h = 480
REAL_PATH = os.path.dirname(os.path.realpath(__file__))

# Setup GPIO + Setup Camera
GPIO.setmode(GPIO.BCM)
SWITCH = 21
GPIO.setup(SWITCH, GPIO.IN)
RESET = 25
GPIO.setup(RESET, GPIO.IN)
PRINT_LED = 22
POSE_LED = 18
BUTTON_LED = 23
GPIO.setup(POSE_LED, GPIO.OUT)
GPIO.setup(BUTTON_LED, GPIO.OUT)
GPIO.setup(PRINT_LED, GPIO.OUT)
GPIO.output(BUTTON_LED, True)
GPIO.output(PRINT_LED, False)

#camera = picamera.PiCamera()
#camera.rotation = 270  # Change this value to set the correct rotation (depending on how your camera is mounted)
#camera.annotate_text_size = 80
#camera.resolution = (1920, 1152)  # take photos at this resolution
#camera.hflip = True  # When preparing for photos, the preview will be flipped horizontally.


# Helper functions ###
def get_filename_for_image():
    """
    This function determines which filename to use for each image, for example:
    ./photos/2017-12-31_23-59-59.jpg
    """
    filename = REAL_PATH + '/photos/' + str(datetime.datetime.now()).split('.')[0]
    filename = filename.replace(' ', '_')
    filename = filename.replace(':', '-')
    filename = filename + '.jpg'
    return filename


def count_down():
    """
    Display countdown clock
    """
    # display a "count down" on screen, starting from 3
    for counter in range(3, 0, -1):
        #camera.annotate_text = ("             ..." + str(counter))
        sleep(1)
    #camera.annotate_text = ''


####################
### Main Program ###
####################
def main():
    """
    Main program loop
    """
    # Start Program
    print("Welcome to the photo booth!")
    print("Press the button to take a photo")

    # Wait for someone to push the button
    while True:
        if (GPIO.input(SWITCH)):
            snap = 0
            while snap < 4:
                print("pose!")
                GPIO.output(BUTTON_LED, False)
                GPIO.output(POSE_LED, True)
                time.sleep(1.5)
                for i in range(5):
                    GPIO.output(POSE_LED, False)
                    time.sleep(0.4)
                    GPIO.output(POSE_LED, True)
                    time.sleep(0.4)
                for i in range(5):
                    GPIO.output(POSE_LED, False)
                    time.sleep(0.1)
                    GPIO.output(POSE_LED, True)
                    time.sleep(0.1)
                GPIO.output(POSE_LED, False)
                print("SNAP")
                gpout = subprocess.check_output(
                    "gphoto2 --capture-image-and-download --filename /home/pi/process_pix/photobooth%H%M%S.jpg",
                    stderr=subprocess.STDOUT, shell=True)
                print(gpout)
                if "ERROR" not in gpout:
                    snap += 1
                GPIO.output(POSE_LED, False)
                time.sleep(0.5)
            #print("please wait while your photos print...")
            GPIO.output(PRINT_LED, True)
            # build image and send to printer
            subprocess.call("sudo /home/pi/scripts/proces_image", shell=True)
            # TODO: implement a reboot button
            # Wait to ensure that print queue doesn't pile up
            # TODO: check status of printer instead of using this arbitrary wait time
            time.sleep(110)
            print("ready for next round")
            GPIO.output(PRINT_LED, False)
            GPIO.output(BUTTON_LED, True)
if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("goodbye")

    except Exception as exception:
        print("unexpected error: ", str(exception))

    finally:
        GPIO.cleanup()
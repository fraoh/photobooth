#!/bin/python
##################################
# Simple Raspberry Pi Photo Booth
##################################


# Imports
import datetime
from time import sleep
import os
import RPi.GPIO as GPIO

# Variables
pin_camera_btn = 21  # pin that the button is attached to
screen_w = 800  # resolution of the photo booth display
screen_h = 480
REAL_PATH = os.path.dirname(os.path.realpath(__file__))

# Setup GPIO + Setup Camera
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_camera_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # assign GPIO pin 21 to our "take photo" button
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

        # Check to see if button is pushed
        is_pressed = GPIO.wait_for_edge(pin_camera_btn, GPIO.FALLING, timeout=100)

        # Stay inside loop until button is pressed
        if is_pressed is None:
            continue

        # Button has been pressed!
        print("Button pressed!")
        #camera.start_preview(resolution=(screen_w, screen_h))  # Start camera preview
        sleep(2)
        count_down()  # Count down to image capture

        # Determine the filename to use when saving the image
        filename = get_filename_for_image()
        #camera.capture(filename)
        print("Photo saved: " + filename)

        # stop camera preview, and wait for the next button press
        #camera.stop_preview()
        is_pressed = False
        print("Press the button to take another photo")


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("goodbye")

    except Exception as exception:
        print("unexpected error: ", str(exception))

    finally:
        GPIO.cleanup()
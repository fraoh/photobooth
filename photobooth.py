#!/bin/python
import RPi.GPIO as GPIO
import time, os, datetime, subprocess

#GPIO.output(20,GPIO.HIGH)
#time.sleep(1)
#print "LED off"
#GPIO.output(20,GPIO.LOW)

from time import sleep

# Variables
BUTTON_LED = 20
SWITCH = 21

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH, GPIO.IN)
GPIO.setup(BUTTON_LED, GPIO.OUT)
GPIO.output(BUTTON_LED, True)

# Helper functions ###
def get_filename_for_image():
    """
    This function determines which filename to use for each image, for example:
    ./photos/2017-12-31_23-59-59.jpg
    """
   # filename = REAL_PATH + '/photos/' + str(datetime.datetime.now()).split('.')[0]
   # filename = filename.replace(' ', '_')
   # filename = filename.replace(':', '-')
   # filename = filename + '.jpg'
   # return filename


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
        GPIO.output(BUTTON_LED, True)
        if (GPIO.input(SWITCH)):
            snap = 0
            while snap < 4:
                print("pose!")
                GPIO.output(BUTTON_LED, False)
                #GPIO.output(POSE_LED, True)
                time.sleep(1.5)
                for i in range(5):
                    #GPIO.output(POSE_LED, False)
                    time.sleep(0.4)
                    #GPIO.output(POSE_LED, True)
                    time.sleep(0.4)
                for i in range(5):
                    #GPIO.output(POSE_LED, False)
                    time.sleep(0.1)
                    #GPIO.output(POSE_LED, True)
                    time.sleep(0.1)
                #GPIO.output(POSE_LED, False)
                print("SNAP")
                gpout = subprocess.check_output(
                    "gphoto2 --capture-image-and-download --filename /home/pi/process_pix/%H%M%S.jpg",
                    stderr=subprocess.STDOUT, shell=True)
                print(gpout)
                if "ERROR" not in gpout:
                    snap += 1
                #GPIO.output(POSE_LED, False)
                time.sleep(0.5)
            #print("please wait while your photos print...")
            #GPIO.output(PRINT_LED, True)
            # build image and send to printer
            subprocess.call("sudo /home/pi/scripts/process_image", shell=True)
            time.sleep(5)
            print("ready for next round")
            #GPIO.output(PRINT_LED, False)
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
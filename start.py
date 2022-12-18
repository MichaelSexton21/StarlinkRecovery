import RPi.GPIO as GPIO
import os
import time

def setup(PIN_GPIO):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_GPIO, GPIO.OUT)
    GPIO.output(PIN_GPIO, True)

def ping(hostname):
    response = os.system("ping -c 1 " + hostname)
    # and then check the response...
    if response == 0:
        return ("Network Active", 1)
    else:
        return ("Network Error", 0)

def reboot_outlet(sec_to_wait):
    GPIO.output(PIN_GPIO, False)
    time.sleep(sec_to_wait)
    GPIO.output(PIN_GPIO, True)

def run(failed_pings,secs_between_pings,secs_reboot,ping_website):
    failed_ping_count = 0
    while 1:
        if failed_ping_count > failed_pings:
            failed_ping_count = 0
            reboot_outlet(secs_reboot)
        if(ping(ping_website)[1] == 0):
            failed_ping_count+=1
        time.sleep(secs_between_pings)


if __name__ == "__main__":
    GUIDED_MODE = 0
    PIN_GPIO = 4
    secs_between_pings = 60
    failed_pings =  3
    secs_reboot =  120
    ping_website = "google.com"
    
    if GUIDED_MODE:
        print("Press enter to accept default values")
        PIN_GPIO = input("Enter pin (default {PIN_GPIO}): ".format(PIN_GPIO=PIN_GPIO)) or PIN_GPIO
        secs_between_pings = input("Seconds between pings (default {secs_between_pings}): ".format(secs_between_pings=secs_between_pings)) or 60
        failed_pings = input("Number of Failed pings (default {failed_pings}): ".format(failed_pings=failed_pings)) or 3
        secs_reboot = input("Seconds wating during reboot (default {secs_reboot}): ".format(secs_reboot=secs_reboot)) or 120
        ping_website = input("Website to ping (default {ping_website}): ".format(ping_website=ping_website)) or "google.com"
    else:
        print("OUTLET REBOOT SCRIPT EXECUTING")

    setup(PIN_GPIO)
    run(failed_pings, secs_between_pings, secs_reboot, ping_website)

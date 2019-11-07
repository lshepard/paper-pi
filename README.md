# paper-pi

This project generates a bitmap image displaying weather and calendar for today and tomorrow. I use this
in my kitchen to allow my family to see daily updates without requiring use of a traditional screen
or mobile phone.

# Hardware

It is intended for display on a 7.5" e-Paper screen such as the Waveshare E-ink display w/ Raspberry Pi HAT. 
Docs are available [here](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_(B)#Raspberry_Pi)

# Setup

Install the HAT on the Raspberry Pi and connect to the Waveshare e-Ink display. Follow the instructions on
Waveshare links to enable SPI, then run the install script which summarizes much of what was discussed
there:

    ./einkscripts/install.sh

Then, install the python dependencies:

    pip3 install -r python/src/requirements.txt

# Build the bitmap

You can run the script to build just the bitmap:


    python3 src/generator

This will query the relevant services and create a bitmap to disk. By default images are stored
in the bitmaps/ folder named by timestamp. You can build this to develop on a device that is not
connected to the e-Ink display.

You can use the ```--file``` option to select a different destination.

    python3 src/generator --file local.png


# Write to the display

When running on the Raspberry Pi with the e-Ink display connection, run the script
with the ```--display``` option:

    python3 src/generator --display

That will write the image to the actual display (as well as save it to disk).


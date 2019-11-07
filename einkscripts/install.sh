# This script should be run in sudo
# UNTESTED - these are the command lines to run.
# Note, this should probably be all done in Docker ... for now
# this is just a way to record the steps from this source
# https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_(B)#Raspberry_Pi

# Install BCM2835 libraries
cd bcm2835-1.60/
./configure
make
make check
make install


# Install wiringPi libraries
apt-get install wiringpi
cd /tmp
wget https://project-downloads.drogon.net/wiringpi-latest.deb
dpkg -i wiringpi-latest.deb


# Install Python libraries
apt-get update
apt-get install python3-pip
apt-get install python3-pil
apt-get install python3-numpy
pip3 install RPi.GPIO
pip3 install spidev

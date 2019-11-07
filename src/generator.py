#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
import click
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from datetime import date, timedelta, datetime
from pytz import timezone
    
import logging
import time
from PIL import Image,ImageDraw,ImageFont,ImageOps
import numpy as np

import traceback
import textwrap

from darksky import forecast

@click.command()
@click.option('--display/--no-display', default=False, help='Push the generated image to the e-Ink display')
@click.option('--out', default="image.png", help='Filename where the generated image should go.')
@click.option('--logfile', default="", help="Filename for logs")

def main(display, out, logfile):
    try:
        if logfile:
            logging.basicConfig(filename=logfile, level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.DEBUG)
            
        black, red = generate_image(640, 384)
        
        write_image_to_disk(black, red, out)

        if display:
            write_image_to_display(black, red)
            
    except IOError as e:
        logging.info(e)
    
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd7in5bc.epdconfig.module_exit()
        exit()

def generate_image(width, height):
    weather = get_weather()

    logging.info("Drawing")    
    font56 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 56)
    font36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
    
    # Drawing on the Horizontal image
    logging.info("1.Drawing on the Horizontal image...") 
    HBlackImage = Image.new('1', (width, height), 255)  # 298*126
    HRedImage = Image.new('1', (width, height), 255)  # 298*126  ryimage: red or yellow image
    
    drawblack = ImageDraw.Draw(HBlackImage)
    drawry = ImageDraw.Draw(HRedImage)

    # Border lines on the screen

    nowstring = datetime.now(tz=timezone("America/Chicago")).strftime('%b %d %-H:%M')
    drawblack.text((500, 350), f"Updated {nowstring}", font = font12, fill = 0)

    # Print out the weather
    thetime = datetime.now(tz=timezone("America/Chicago"))
    line = 1
    with get_weather() as weather:
        HRedImage.paste(icon_img(weather.currently.icon, 66), box=(20,line*30-4))
        drawry.text((100, line*30), f"Currently {int(weather.currently.temperature)}°", font = font56, fill = 0)

        line += 3
        for hour in weather.hourly[0:8]:
            hour = dict( hour = date.strftime(thetime, '%H:00'),
                         temp = str(int(hour.temperature)),
                         sum = hour.summary,
                         icon = hour.icon
            )
            
            HRedImage.paste(icon_img(hour["icon"], 33), box=(20,line*30-4))
            drawblack.text((60, line*30), '{hour}: {temp}° {sum}'.format(**hour), font = font18, fill = 0)
#            drawry.text((400, line*30), '{tempMin}-{tempMax}°'.format(**day), font = font24, fill = 0)

            thetime += timedelta(hours=1)
            line += 1
            
    return (HBlackImage, HRedImage)

def get_weather():
    """Connect to DarkSky and get local weather info for Chicago"""
    DARKSKYKEY="af20eaabf57d81ada9cebadf46b90b53"
    return forecast (DARKSKYKEY, 41.931259, -87.669975)

def icon_img(icon, width):
    """"Return the icon, resized, for a given weather - works for
    all darksky values of "icon". """
    img = Image.open(os.path.join(picdir, "weather/", icon + ".png"))
    return ImageOps.invert(img.resize((width,width)))

def write_image_to_disk(HBlackImage, HRedImage, out):
    """Write the image to disk. 
    For now just do black - figure out the red overlay later"""

    black_data = np.array(HBlackImage.convert("RGBA"))

    # Convert the red image
    red_data = np.array(HRedImage.convert("RGBA"))   # "data" is a height x width x 4 numpy array
    logging.info(f"red_data shape: {red_data.shape}")
    
    red, green, blue, alpha = red_data.T # Temporarily unpack the bands for readability

    # Replace black with red... (leaves alpha values alone...)
    white_areas = (red == 0) & (blue == 0) & (green == 0)
    red_data[..., :-1][white_areas.T] = (255, 0, 0) # Transpose back needed

    composed = Image.fromarray(np.minimum(black_data, red_data))
    composed.save(out)
    
def write_image_to_display(HBlackImage, HRedImage):
    from waveshare_epd import epd7in5bc
    
    """Takes two images - black and red - and writes them to the e-Ink display.
    Note that this may take several seconds in total."""
    epd = epd7in5bc.EPD()
    logging.info("init and Clear")
    epd.init()
#    epd.Clear()
    epd.display(epd.getbuffer(HBlackImage), epd.getbuffer(HRedImage))
    epd.sleep()



if __name__ == '__main__':
    main()


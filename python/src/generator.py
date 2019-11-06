#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
from datetime import date, timedelta, datetime
from pytz import timezone
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5bc
import time
from PIL import Image,ImageDraw,ImageFont,ImageOps
import traceback
import textwrap

from darksky import forecast
import requests
import json

logging.basicConfig(level=logging.DEBUG)
DARKSKYKEY="af20eaabf57d81ada9cebadf46b90b53"

def get_weather():
    return forecast (DARKSKYKEY, 41.931259, -87.669975)

def icon_img(icon, width):
    img = Image.open(os.path.join(picdir, "weather/", icon + ".png"))
    return ImageOps.invert(img.resize((width,width)))

try:
    logging.info("Generating Weather Image")

    weather = get_weather()
    logging.info("Weather " + ",".join([str(int(hour.temperature)) for hour in weather.hourly[:10]]))

    epd = epd7in5bc.EPD()
    logging.info("init and Clear")
    epd.init()
#    epd.Clear()
#    time.sleep(1)
    
    logging.info("Drawing")    
    font56 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 56)
    font36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
    
    # Drawing on the Horizontal image
    logging.info("1.Drawing on the Horizontal image...") 
    HBlackimage = Image.new('1', (epd.width, epd.height), 255)  # 298*126
    HRYimage = Image.new('1', (epd.width, epd.height), 255)  # 298*126  ryimage: red or yellow image  
    drawblack = ImageDraw.Draw(HBlackimage)
    drawry = ImageDraw.Draw(HRYimage)

    # Border lines on the screen

    nowstring = datetime.now(tz=timezone("America/Chicago")).strftime('%b %d %-H:%M')
    drawblack.text((500, 350), f"Updated {nowstring}", font = font12, fill = 0)

    # Print out the weather
    weekday = date.today()
    line = 1
    with get_weather() as weather:
        HRYimage.paste(icon_img(weather.daily.icon, 66), box=(20,line*30-4))
        drawry.text((100, line*30), f"Currently {int(weather.currently.temperature)}°", font = font56, fill = 0)

        line += 3
        for day in weather.daily[0:3]:
            day = dict(day = date.strftime(weekday, '%a'),
                       sum = day.summary,
                       tempMin = str(int(day.temperatureMin)),
                       tempMax = str(int(day.temperatureMax)),
                       icon = day.icon
            )
            
            HRYimage.paste(icon_img(day["icon"], 33), box=(20,line*30-4))
            drawblack.text((60, line*30), '{day}: {sum}'.format(**day), font = font18, fill = 0)
            drawry.text((400, line*30), '{tempMin}°-{tempMax}°'.format(**day), font = font24, fill = 0)

            weekday += timedelta(days=1)
            line += 1

    # display the date at the top
#    drawblack.text((20, 20), datetime.datetime.now().strftime("%A, %B %d, %Y"), font = font36, fill = 0)

#    drawblack.text((50, 100), str(int(weather.daily[1].temperatureMax)) + " degrees", font = font56, fill = 0)
#    drawblack.text((50, 200), weather.daily.summary, font = font24, fill = 0)

    # show the weather for today

    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))

    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5bc.epdconfig.module_exit()
    exit()

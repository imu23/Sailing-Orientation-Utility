# This script composes the display image
#
# Revised from a script included in the gratis repository available through
# the Pervasive Displays.
#
# Copyright 2013 Pervasive Displays, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#   http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.  See the License for the specific language
# governing permissions and limitations under the License.


import sys
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime
import time
from EPD import EPD
epd = None

WHITE = 1
BLACK = 0

TITLE_FONT_SIZE = 20

MAX_START = 0xffff

class EDisplay(object):    
    def __init__(self):
        global epd #bring it in scope
        self.screen = False
        self.pause = False
        epd = EPD()
        epd.clear()
    
    def display_startup(self):
        global epd

        # initially set all white background
        image = Image.new('1', epd.size, WHITE)

        # prepare for drawing
        draw = ImageDraw.Draw(image)
        width, height = image.size
        
        context_font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 20)
        title_font = ImageFont.truetype('/usr/share/fonts/truetype/roboto/RobotoCondensed-Bold.ttf', TITLE_FONT_SIZE)

        # clear the display buffer
        draw.rectangle((0, 0, width, height), fill=WHITE, outline=WHITE)
        
        #self.screenTwo(data)
        title_y = 2;
        draw.text((5,title_y), "SIS", fill=BLACK, font=title_font)
        line_y = title_y + TITLE_FONT_SIZE + 3
        draw.line([(0,line_y),(264,line_y)], fill=BLACK)
        new_y = 2 + line_y + 5
        draw.text((2,new_y), 'Press Button to Start', fill=BLACK, font=context_font)
        new_y = new_y + 25
        # display image on the panel
        epd.display(image)
        epd.update() 
        
	# passing in the array of the sensor information and the saving flag to indicate on the screen
    def display_data(self, data, saving):
        global epd
        
        # initially set all white background
        image = Image.new('1', epd.size, WHITE)

        # prepare for drawing
        draw = ImageDraw.Draw(image)
        width, height = image.size
        
        context_font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 20)
        title_font = ImageFont.truetype('/usr/share/fonts/truetype/roboto/RobotoCondensed-Bold.ttf', TITLE_FONT_SIZE)

        # clear the display buffer
        draw.rectangle((0, 0, width, height), fill=WHITE, outline=WHITE)
        previous_second = 0
        previous_day = 0
        
        # the screen width is 264 and the height is 176
        while True:
            now = datetime.today()
            if now.second % 5 == 0:
                break
            time.sleep(0.5)
        if self.screen:
            #self.screenTwo(data)
            title_y = 2;
            
            draw.text((5,title_y), "SIS", fill=BLACK, font=title_font)
            draw.text((100,title_y), str(data[0]) + '   ' + str(data[1]) [0:4], fill=BLACK, font=title_font)
            line_y = title_y + TITLE_FONT_SIZE + 3
            draw.line([(0,line_y),(264,line_y)], fill=BLACK)
            new_y = 2 + line_y + 5
            draw.text((2,new_y), 'Speed: ' + str(data[5]), fill=BLACK, font=context_font)
            new_y = new_y + 25
            draw.text((2, new_y), 'Temperature: ' + str(data[6]), fill=BLACK, font=context_font)       
            new_y = new_y + 25
            draw.text((2, new_y), 'Pressure: ' + str(data[7]), fill=BLACK, font=context_font)
            new_y = new_y + 25
            draw.text((2, new_y), 'Heading: ' + str(data[8]), fill=BLACK, font=context_font)
            new_y = new_y + 45
            draw.text((2, new_y), 'Saving: ' + saving, fill=BLACK, font=context_font)
            if self.pause == False:
                self.screen = False
        else:
            #self.screenOne(data)
            title_y = 2;
            draw.text((5,title_y), "SIS", fill=BLACK, font=title_font)
            draw.text((100,title_y), str(data[0]) + '   ' + str(data[1]) [0:4], fill=BLACK, font=title_font)
            line_y = title_y + TITLE_FONT_SIZE + 3
            draw.line([(0,line_y),(264,line_y)], fill=BLACK)
            new_y = 2 + line_y + 5
            draw.text((2,new_y), 'Speed: ' + str(data[5]), fill=BLACK, font=context_font)
            new_y = new_y + 25
            draw.text((2,new_y), 'Latitude: ' + str(data[2]), fill=BLACK, font=context_font)
            new_y = new_y + 25
            draw.text((2,new_y), 'Longitude: ' + str(data[3]), fill=BLACK, font=context_font)
            new_y = new_y + 25
            draw.text((2,new_y), 'Altitude: ' + str(data[4]), fill=BLACK, font=context_font)
            new_y = new_y + 45
            draw.text((2,new_y), 'Saving: ' + saving, fill=BLACK, font=context_font)
            if self.pause == False:
                self.screen = True
        # display image on the panel
        epd.display(image)
        if now.second < previous_second:
            epd.update()    # full update every minute
        else:
            epd.partial_update()
        previous_second = now.second
        
# main
if "__main__" == __name__:
    if len(sys.argv) < 1:
        sys.exit('usage: {p:s}'.format(p=sys.argv[0]))

    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit('interrupted')
        pass

import time
import sys
import threading
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime
from time import gmtime, strftime
import urllib2
import json
from PluginImageResult import PluginImageResult

class DarkSkyPlugin:
    def __init__(self, apiKey, forcastLocation):
        self.CurrentTemp = 0
        self.CurrentOverview = "Not Loaded"
        self._hasData = False
        self._apiKey = apiKey
        self._forcastLocation = forcastLocation
        self._wasError = False
        self._lock = threading.Lock()

    def GetIntervalSeconds(self):
        return 120 # 2 mins

    def Execute(self):
        self.Refresh()

    def Refresh(self):
        try:
            darkSkyForcast = json.loads(urllib2.urlopen("https://api.darksky.net/forecast/" + self._apiKey + "/" + self._forcastLocation).read())
            outdoorTemp = float(darkSkyForcast["currently"]["temperature"])
            todayHighTemp = float(darkSkyForcast["daily"]["data"][0]["temperatureHigh"])
            todayLowTemp = float(darkSkyForcast["daily"]["data"][0]["temperatureLow"])
            
            with self._lock:
                self._mins = darkSkyForcast["minutely"]["data"]
                self._icon = darkSkyForcast["minutely"]["icon"] + ".png"
                self._currentTemp = round((outdoorTemp - 32) / 1.8, 0)
                self._currentOverview = darkSkyForcast["minutely"]["summary"]
                self._highTemp = round((todayHighTemp - 32) / 1.8, 0)
                self._lowTemp = round((todayLowTemp - 32) / 1.8, 0)
                self._hasData = True
                self._wasError = False
                print(self._currentOverview)
        except:
            self._wasError = True
            e = sys.exc_info()
            print ("Failed to load DarkSky data - " + str(e))

    def _writeToImageInternal(self, inkyColours):
        image = Image.new("P", (400, 130))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, 400, 130), fill=inkyColours.White)

        font = ImageFont.truetype ("Nunito-ExtraLight.ttf", 16)
        font3 = ImageFont.truetype ("Nunito-ExtraLight.ttf", 12)
        font2 = ImageFont.truetype("Nunito-ExtraLight.ttf", 32)
        font4 = ImageFont.truetype ("Nunito-ExtraLight.ttf", 10)

        if self._hasData and not self._wasError:
            draw.text((55, -5), str(self._currentTemp) + "c", inkyColours.Black, font2)
            draw.text((55, 30), self._currentOverview, inkyColours.Black, font)

            draw.text((140, 1), "H: " + str.format("{:.0f}", self._highTemp), inkyColours.Black, font3)
            draw.text((140, 15), "L:  " + str.format("{:.0f}", self._lowTemp), inkyColours.Black, font3)

            # Rain Graph
            left = 10
            top = 110
            draw.line((left - 2, top - 12, left, top - 12), fill=inkyColours.Black)
            draw.line((left - 2, top - 27, left, top - 27), fill=inkyColours.Black)
            draw.line((left - 2, top - 40, left, top - 40), fill=inkyColours.Black)

            draw.line((left + 240, top - 12, left + 244, top - 12), fill=inkyColours.Black)
            draw.line((left + 240, top - 27, left + 244, top - 27), fill=inkyColours.Black)
            draw.line((left + 240, top - 40, left + 244, top - 40), fill=inkyColours.Black)

            # Draw the Y axis headings
            draw.text((left + 253 - 3, top -12), "Low", inkyColours.Black, font4)
            draw.text((left + 253 - 3, top -25), "Med", inkyColours.Black, font4)
            draw.text((left + 253 - 3, top -40), "High", inkyColours.Black, font4)
            
            # Draw the X axis headings
            draw.line((left, top, left + 160, top), fill=inkyColours.Black)
            draw.text((left - 6, top + 5), "Now", inkyColours.Black, font4)
            draw.text((left + 60 - 3, top + 5), "15", inkyColours.Black, font4)
            draw.text((left + 120 - 3, top + 5), "30", inkyColours.Black, font4)
            draw.text((left + 180 - 3, top + 5), "45", inkyColours.Black, font4)
            draw.text((left + 240 - 3, top + 5), "60", inkyColours.Black, font4)

            showGraph = False
            for r in self._mins:
                precipIntensity = r["precipIntensity"]

                max = 0.18
                size = ((precipIntensity) / max) * 40
                
                size = round(size)
                size = min(size, 40)

                showGraph = showGraph or size > 0

                draw.line((left,top, left, top - size), fill=inkyColours.Black)
                draw.line((left + 1, top, left + 1, top - size), fill=inkyColours.Black)
                draw.line((left + 2, top, left + 2, top - size), fill=inkyColours.Black)
                draw.line((left + 3, top, left + 3, top - size), fill=inkyColours.Black)
                left = left + 4
            
            if not showGraph:
                image = image.crop((0, 0, 400, 50))

            icon = Image.open("icons/" + self._icon)   
            pal_img = Image.new("P", (1, 1))
            pal_img.putpalette((255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252)
            icon = icon.convert("RGB").quantize(palette=pal_img)          
            image.paste(icon,(0,0))
       
        elif self._wasError:
            draw.text((0, 5), "Forcast unavilable", inkyColours.Black, font)

        else:
            draw.text((0, 5), "Forcast loading...", inkyColours.Black, font)

        return PluginImageResult(image, False)

    def WriteToImage(self, inkyColours):
        with self._lock:
            return self._writeToImageInternal(inkyColours)

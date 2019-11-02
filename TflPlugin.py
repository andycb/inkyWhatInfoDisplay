import time
import threading
import sys
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime
from time import gmtime, strftime
import urllib2
import json
from PluginImageResult import PluginImageResult

class LineStatus:
    def __init__(self, name, statusText, isGood):
        self.Name = name
        self.IsGood = isGood
        self.StatusText = statusText

class TflPlugin:
    def __init__(self, appId, appKey, lines):
        self._hasData = False
        self._appId = appId
        self._appKey = appKey
        self._lines = lines
        self._wasError = False
        self._statuses = [ ]
        self._lock = threading.Lock()

    def GetIntervalSeconds(_):
        return 120 # 2 mins

    def Execute(self):
        self.Refresh()


    def _ExtractTflData(self, json):
        result = {}
        for line in json:
            result[line["id"]] = line["lineStatuses"][0]
        
        return result


    def Refresh(self):
        try:
            linesString = ""
            for lineName in self._lines:
                linesString = linesString + lineName.lower() + "%2C"
                
            tflJson = json.loads(urllib2.urlopen("https://api.tfl.gov.uk/Line/" + linesString + "/Status?detail=false&app_id=" + self._appId + "&app_key=" + self._appKey).read())
            tflStatus = self._ExtractTflData(tflJson)

            with self._lock:
                self._statuses = []

                for lineName in self._lines:
                    statusText = tflStatus[lineName.lower()]["statusSeverityDescription"]
                    isGood = tflStatus[lineName.lower()]["statusSeverity"] == 10
                    self._statuses.append(LineStatus(lineName, statusText, isGood))

                self._hasData = True
                self._wasError = False
            
        except:
            self._wasError = True
            e = sys.exc_info()
            print("Failed to load TfL data - " + str(e))

    def _writeToImageInternal(self, inkyColours):
        image = Image.new("P", (400, 300))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, 400, 300), fill=inkyColours.White)
        font = ImageFont.truetype ("Nunito-ExtraLight.ttf", 16)

        requiresColour = False
        if self._hasData and not self._wasError:
            offset = 0
            for status in self._statuses:
                draw.text((0, offset), status.Name, inkyColours.Black, font)
                draw.text((100, offset), status.StatusText, inkyColours.Black, font)
                offset = offset + 20

            # Crop the image down to show only the space it needs
            image = image.crop((0, 0, 400, offset))

        elif self._wasError:
            draw.text((0, 15), "TfL data unavailable", inkyColours.Black, font)
        else:
            draw.text((0, 15), "TfL data loading...", inkyColours.Black, font)

        return PluginImageResult(image, False)

    def WriteToImage(self, inkyColours):
        with self._lock:
            return self._writeToImageInternal(inkyColours)
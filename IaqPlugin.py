from Adafruit_IO import Client, Data
import sys

class IagPlugin:
    def __init__(self, username, key):
        self.IndoorTemp = 0
        self._hasData = False
        self._aio = Client(username, key)

    def GetIntervalSeconds(_):
        return 60 # 1 min

    def Execute(self):
        self.Refresh()

    def Refresh(self):
        try:
            self.IndoorTemp = round(float(self._aio.data('temp')[0].value))
        except:
            e = sys.exc_info()
            print ("Failed to load IAQ data - " + str(e))
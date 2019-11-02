class ScreenUpdatePlugin:
    def __init__(self, callback, isDebugMode):
        self._callback = callback
        self._isDebugMode = isDebugMode

    def GetIntervalSeconds(self):
        return 5 if self._isDebugMode else 60

    def Execute(self):
        self._callback()
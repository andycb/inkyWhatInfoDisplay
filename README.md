# Inky What Info Display
A Python script for displaying weather and travel information on a Pimoroni Inky wHAT display. For the full write up of this project, see https://andybradford.dev/2019/11/03/living-room-eink-display.

This repo is intended as a reference for how I built my information display, so is a little specific to what I did. If you want to build something similar, feel free to use this as is or add / change your own stuff. If you do something cool, I'd love to hear about it, you can tweet me at [@devandyb](https://twitter.com/andycb) or leave a comment on the above blog post

## Setup
1) Make sure you have Python 2 instaled (the inky library doesn't yet support Pyhton 3)
1) Install the Inky library using these instructions: https://github.com/pimoroni/inky
1) Install the [Adafruit IO library](https://github.com/adafruit/Adafruit_IO_Python) for Python 2 by running `pip install adafruit-io`.
1) Get some API keys:
    * TFL: https://api.tfl.gov.uk/
    * Dark Sky: https://darksky.net/dev
    * Adafruit IO: https://io.adafruit.com/api/docs/#authentication
1) Paste your API keys into [AuthTokens.py](AuthTokens.py)
1) Find your longitude and latitude (It'll look something like this `51.5013673,-0.1440787`) and paste it into the `DARKSKY_FORCAST_LOCATION` section of [AuthTokens.py](AuthTokens.py)
1) In the `TFL_LINES` section of [AuthTokens.py](AuthTokens.py) add a list of TfL service to track for example `["Metropolitan", "Bakerloo", "DLR"]`

## Run
Run `python Main.py` to run the script. Your screen should refresh and show a loading screen before showing some data.

## Third Party Work Included 

### Font
The Nunito font used is Nunito by Vernon Adams, check it out on Google Fonts: https://fonts.google.com/specimen/Nunito

### Icons
The weather icons used are Climacons by Adam Whitcroft, check them out here: http://adamwhitcroft.com/climacons/

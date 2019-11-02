import time
from inky import InkyPHAT, InkyWHAT
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime
from time import gmtime, strftime

from LibScheduler import Scheduler
from DarkSkyPlugin import DarkSkyPlugin
from TflPlugin import TflPlugin
from ScreenUpdatePlugin import ScreenUpdatePlugin
from IaqPlugin import IagPlugin
import AuthTokens
from DebugInky import DebugInky
from InkyColours import InkyColours

# Enabling debug will write the image to a PNG rather than the actual screen
DEBUG = False

# Enabling warm refresh means that the eInk display is not flashed
# to black & white when updating what is shown. This is prettyier when little
# data has changed on screen, but comes at the cost of visual quality. Therefore every
# so many refreshes (defined by WARM_REFRESH_CLEAN_FREQUENCY) the screen will fully blank anyway.
# Note: At the moment this needs a fork of the inky library to work.
# TURNING THIS ON MAY CAUSE DAMAGE TO YOUR DISPLAY.
# DO SO AT YOUR OWN RISK.
ENABLE_WARM_REFRESH = False
WARM_REFRESH_CLEAN_FREQUENCY = 5

darkSky = DarkSkyPlugin(AuthTokens.DARKSKY_KEY, AuthTokens.DARKSKY_FORCAST_LOCATION)
tfl = TflPlugin(AuthTokens.TFL_APP_ID, AuthTokens.TFL_APP_KEY, AuthTokens.TFL_LINES)
iaq = IagPlugin(AuthTokens.ADAFRUIT_IO_USERNAME, AuthTokens.ADAFRUIT_IO_KEY)
refreshCount = 0.0

# Create all the screen types once rather than
# switching between black and red screens in each update
# because the inky library doesn't close the connections to the 
# SPI or I2C bus when collected, and the app will crash after around 1025 refreshes 
inky_display_black = InkyWHAT("black") if not DEBUG else DebugInky()
inky_display_red = InkyWHAT("red") if not DEBUG else DebugInky()

if ENABLE_WARM_REFRESH:
    inky_display_black_fast = InkyWHAT("black_fast") if not DEBUG else DebugInky()
    inky_display_red_fast = InkyWHAT("red_fast") if not DEBUG else DebugInky()

def _updateScreen():
    global refreshCount

    print("Screen is being updated")
    
    requiresColourRefresh = False
    image = Image.new("P", (400, 300))
    draw = ImageDraw.Draw(image)

    inkyColours = InkyColours(1,0,2) if not DEBUG else InkyColours("#000000","#ffffff","#ff000000")

    fontSmall = ImageFont.truetype ("Nunito-ExtraLight.ttf", 16)
    fontVerySmall = ImageFont.truetype("Nunito-ExtraLight.ttf", 10)

    # Draw the top bar
    draw.rectangle((0, 0, 400, 300), fill=inkyColours.White)
    draw.rectangle((400, 40, 0, 0), fill=inkyColours.Black)

    # Add the clock
    timeStr = strftime("%-I:%M %p", time.localtime())
    draw.text((10, 10), timeStr, inkyColours.White, fontSmall)

    # Add indoor tempriture
    draw.text((350, 10), str(str.format("{:.0f}c",iaq.IndoorTemp)), inkyColours.White, fontSmall)

    # Generate weather forcast image and add
    darkSkyImageResult = darkSky.WriteToImage(inkyColours)
    image.paste(darkSkyImageResult.Image, (10, 50))
    requiresColourRefresh = requiresColourRefresh or darkSkyImageResult.RequiresColour
    draw.text((10, 285), "Powered by Dark Sky", inkyColours.Black, fontVerySmall)
    
    # Generate TfL status image and add
    tflImageResult = tfl.WriteToImage(inkyColours)
    image.paste(tflImageResult.Image, (10, darkSkyImageResult.Image.height + 10 + 50))
    requiresColourRefresh = requiresColourRefresh or tflImageResult.RequiresColour
    
    # Create the display 
    inky_display = inky_display_red if requiresColourRefresh else inky_display_black
    
    if ENABLE_WARM_REFRESH:
        refreshCount = refreshCount + 1
        if (refreshCount < WARM_REFRESH_CLEAN_FREQUENCY):
            inky_display = inky_display_red_fast if requiresColourRefresh else inky_display_black_fast
        else:
            refreshCount = 0

    inky_display.set_border("white")

    inky_display.set_image(image)
    inky_display.show()
    
scheduler = Scheduler()
screenUpdate = ScreenUpdatePlugin(_updateScreen, DEBUG)
scheduler.RegisterWorkItem(darkSky)
scheduler.RegisterWorkItem(tfl)
scheduler.RegisterWorkItem(screenUpdate)
scheduler.RegisterWorkItem(iaq)

scheduler.Run()

if DEBUG:
    while True:
        x = raw_input()


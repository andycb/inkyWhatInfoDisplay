import time
from inky_fork import InkyPHAT, InkyWHAT
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime
from time import gmtime, strftime

inky_display = InkyWHAT("black_fast")

font = ImageFont.truetype("Nunito-ExtraLight.ttf", 130)

i = 10
while True:
    image = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
    draw = ImageDraw.Draw(image)
    draw.rectangle((400, 300, 0, 0), fill=inky_display.WHITE)
    draw.text((100, 100), str(i), inky_display.BLACK, font)

    inky_display.set_image(image)
    inky_display.show()
    i = i + 1
    time.sleep(1)


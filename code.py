# https://learn.adafruit.com/making-a-pyportal-user-interface-displayio/display
# https://circuitpython.readthedocs.io/en/latest/shared-bindings/displayio/#displayio.Display
# https://circuitpython.readthedocs.io/projects/touchscreen/en/latest/api.html
# https://www.devdungeon.com/content/pyportal-circuitpy-tutorial-adabox-011#toc-21

import time
import json
import board
import terminalio
import busio
from digitalio import DigitalInOut
from analogio import AnalogIn
import adafruit_touchscreen
import displayio
import rfm69_i2c
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.rect import Rect
from adafruit_button import Button
from adafruit_pyportal import PyPortal
  
# ESP32 SPI
from adafruit_esp32spi import adafruit_esp32spi, adafruit_esp32spi_wifimanager

# Import NeoPixel Library
import neopixel

# Import Adafruit IO HTTP Client
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError


# Import ADT7410 Library
import adafruit_adt7410

# Timeout between sending data to Adafruit IO, in seconds
IO_DELAY = 30

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# PyPortal ESP32 Setup
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
status_light = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light)

# Set your Adafruit IO Username and Key in secrets.py
# (visit io.adafruit.com if you need to create an account,
# or if you need your Adafruit IO key.)
ADAFRUIT_IO_USER = secrets['aio_username']
ADAFRUIT_IO_KEY = secrets['aio_key']


# Create an instance of the Adafruit IO HTTP client
io = IO_HTTP(ADAFRUIT_IO_USER, ADAFRUIT_IO_KEY, wifi)

# for i in range(128,168):
#     print(i,' = ', chr(i))
 
 
# Set up ADT7410 sensor
i2c = board.I2C()   #busio.I2C(board.SCL, board.SDA)
#adt = adafruit_adt7410.ADT7410(i2c, address=0x48)
#adt.high_resolution = True
print('i2c initialized')
rfm69i2c = rfm69_i2c.RFM69_I2C(i2c,address= 0x20)

#while not i2c.try_lock():
#    pass
   
try:
    print('RFM69 available=',rfm69i2c.rfm69_data_avail)
except:
    print('RFM69 I2C problem')
    
while 1:
    if rfm69i2c.rfm69_data_avail > 0:
        msg_len = rfm69i2c.rfm69_load_msg()
        print('Message length=',msg_len)
        msg_1 = rfm69i2c.rfm69_get_data(1)
        print(msg_1)
        msg_2 = rfm69i2c.rfm69_get_data(2)
        print(msg_2)
        msg = msg_1 + msg_2
        print(msg)
        msg_str = msg.decode()
        print(msg_str)
        d = json.loads(msg_str)
        print(d)
    time.sleep(5.0)
    
# Set up an analog light sensor on the PyPortal
adc = AnalogIn(board.LIGHT)
display = board.DISPLAY
  
MIN_UPLOAD_INTERVAL  = 60.0*5
    
rfm69_out_buf    = [0]*2
rfm69_inp_buf    = [0]*32

aio_dict = {'Dock_T_Water': {'feed':'villaastrid.water-temp','available': False, 'timeto': 0.0, 'value':0.0},
            'Dock_T_bmp180': {'feed':'villaastrid.dock-temp','available': False, 'timeto': 0.0, 'value':0.0},
            'Dock_P_bmp180': {'feed':'villaastrid.dock-pres','available': False, 'timeto': 0.0, 'value':0.0},
            'Dock_T_dht22': {'feed':'villaastrid.outdoor1-temp-dht22','available': False, 'timeto': 0.0, 'value':0.0},
            'Dock_H_dht22': {'feed':'villaastrid.dock-hum-dht22','available': False, 'timeto': 0.0, 'value':0.0},
            'OD_1_Temp':  {'feed':'villaastrid.outdoor1-temp','available': False, 'timeto': 0.0, 'value':0.0},
            'OD_1_Hum':  {'feed':'villaastrid.outdoor1-hum-dht22','available': False, 'timeto': 0.0, 'value':0.0},
            'OD_1_P_mb':  {'feed':'villaastrid.outdoor1-pmb','available': False, 'timeto': 0.0, 'value':0.0},
            'OD_1_Light1':  {'feed':'villaastrid.outdoor1-ldr1','available': False, 'timeto': 0.0, 'value':0.0},
            'OD_1_Temp2': {'feed':'villaastrid.outdoor1-temp-dht22','available': False, 'timeto': 0.0,  'value':0.0}}
for key in aio_dict:
    aio_dict[key]['timeto'] = time.monotonic()

while not i2c.try_lock():
    pass
try:
    pass
    #print("I2C addresses found:", [hex(device_address)
    #    for device_address in i2c.scan()])
    #time.sleep(2)

    # https://circuitpython.readthedocs.io/en/6.3.x/shared-bindings/busio/index.html#busio.I2C
    #rfm69_out_buf[0] = RFM69_RX_AVAIL
    #i2c.writeto_then_readfrom(RFM69_I2C_ADDRESS, rfm69_out_buf, rfm69_inp_buf)
    #print(rfm69_out_buf)
    #print(rfm69_inp_buf)

    #print('RFM69 available=',rfm69i2c.rfm69_data_avail)
except:
    print('RFM69 I2C problem')
    
finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
    i2c.unlock()

while 1:
    pass

# Backlight function
# Value between 0 and 1 where 0 is OFF, 0.5 is 50% and 1 is 100% brightness.
def set_backlight(val):
    val = max(0, min(1.0, val))
    display.auto_brightness = False
    display.brightness = val



# print(dir(board))
display.rotation=0


set_backlight(1.0)
# Touchscreen setup
# ------Rotate 270:
screen_width = 240
screen_height = 320
ts = adafruit_touchscreen.Touchscreen(board.TOUCH_XL, board.TOUCH_XR,
                                      board.TOUCH_YD, board.TOUCH_YU,
                                      calibration=((5200, 59000), (5800, 57000)),
                                      size=(screen_width, screen_height))


try:
    temperature_feed = io.get_feed('villaastrid.tupa-bme680-temp')
except AdafruitIO_RequestError:
    print("temperature_feed, failed")


try:
    ldr_feed = io.get_feed('home-tampere.esp32test-ldr')
except AdafruitIO_RequestError:
    print("ldr_feed, failed")


try:
    water_temp_feed = io.get_feed('villaastrid.water-temp')
except AdafruitIO_RequestError:
    print("water temp feed, failed")

try:
    outdoor_temp_feed = io.get_feed('villaastrid.outdoor1-temp')
except AdafruitIO_RequestError:
    print("outdoor temp feed, failed")



# ------------- Display Groups ------------- #
splash = displayio.Group(max_size=10) # The Main Display Group
view1 = displayio.Group(max_size=15, x=0, y=40) # Group for View 1 objects
view2 = displayio.Group(max_size=15, x=0, y=40) # Group for View 2 objects
view3 = displayio.Group(max_size=15, x=0, y=40) # Group for View 3 objects

# splash.append(view1)
# splash.append(view2)
# splash.append(view3)

text = "hello hello"
color = 0x0000FF
font = terminalio.FONT
color = 0x03AD31

# Set the font and preload letters
font = bitmap_font.load_font("/fonts/Junction-regular-24.bdf")
# font = bitmap_font.load_font("/fonts/Arial-ItalicMT-17.bdf")
# font = bitmap_font.load_font("/fonts/LeagueSpartan-Bold-16.bdf")
font.load_glyphs(b'abcdefghjiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890- ()')
# Used to calculate vertical text height for Top Alignment
text_hight = Label(font, text="M", color=0x03AD31, max_glyphs=10)

# Create the text label
text_area = Label(font, text=text, color=color, max_glyphs= 200)

# Set the location
text_area.x = 100
text_area.y = 180

# Show it
cntr = 0
while True:
    # text = str(cntr)
    cntr = cntr + 1

    received_data = io.receive_data(temperature_feed["key"])
    tupa_temp = float(received_data['value'])
    text = "Tupa {0:.1f} C".format(tupa_temp)
    text_area1 = Label(font, text=text, x=20, y=30,color=color, max_glyphs= 200)

    received_data = io.receive_data(ldr_feed["key"])
    ldr_value = float(received_data['value'])
    text = "LDR {0:.0f}".format(ldr_value)
    text_area2 = Label(font, text=text, x=20, y=70,color=color, max_glyphs= 200)

    received_data = io.receive_data(water_temp_feed["key"])
    water_temp_value = float(received_data['value'])
    text = "Water {0:.1f}".format(water_temp_value)
    text_area3 = Label(font, text=text, x=20, y=110,color=color, max_glyphs= 200)

    received_data = io.receive_data(outdoor_temp_feed["key"])
    outdoor_temp_value = float(received_data['value'])
    text = "Outdoor {0:.1f} C".format(outdoor_temp_value)
    text_area4 = Label(font, text=text, x=20, y=150,color=color, max_glyphs= 200)

    splash.append(text_area1)
    splash.append(text_area2)
    splash.append(text_area3)
    splash.append(text_area4)

    # text_area.x = 100
    # text_area.y = 80     # + (cntr *10)
    display.show(splash)
    time.sleep(10.0)
    #text_area1 = Label(font, text="puppu", x=20, y=30,color=color, max_glyphs= 200)
    #display.show(text_area1)
    #time.sleep(10.0)

    splash.remove(text_area1)
    splash.remove(text_area2)
    splash.remove(text_area3)
    splash.remove(text_area4)


while True:
    pass

# Default Label styling:
TABS_X = 0
TABS_Y = 0

group = displayio.Group(max_size=4)
group.x = 20
group.y = 20
set_backlight(1.0)

display.show()

while 1:
    pass

def show_values(name, value):
    sensors_label = Label(font, text=name, color=0x03AD31, max_glyphs=200)
    sensors_label.x = TABS_X
    sensors_label.y = TABS_Y + 100
    view2.append(sensors_label)

    sensor_data = Label(font, text=value, color=0x03AD31, max_glyphs=100)
    sensor_data.x = TABS_X
    sensor_data.y = TABS_Y + 150
    view3.append(sensor_data)
    board.DISPLAY.show(group)

set_backlight(1.0)



while 1:
    print("Retrieving data from temperature feed tupa-bme680-temp")
    print(chr(176))
    received_data = io.receive_data(temperature_feed["key"])
    tupa_temp = float(received_data['value'])
    v = "Tupa {0:.1f} C".format(tupa_temp)
    print(v)
    show_values(v,'xyz')
    time.sleep(60.0)



# Print out all the results.
#for d in data:
#    print('Data value: {0}'.format(d.value))





# ------------- Layer Functions ------------- #
# Hide a given Group by removing it from the main display Group.
def hideLayer(i):
    try:
        splash.remove(i)
    except ValueError:
        pass
# Show a given Group by adding it to the main display Group.
def showLayer(i):
    try:
        splash.append(i)
    except ValueError:
        pass


group = displayio.Group(max_size=4)
group.x = 20
group.y = 20

'''
image_file = open("/images/ZerioAvatar_60x60.bmp", "rb")
image = displayio.OnDiskBitmap(image_file)
image_sprite = displayio.TileGrid(image, pixel_shader=displayio.ColorConverter())

group.append(image_sprite)
'''
group.append(splash)
board.DISPLAY.show(group)


#icon_group = displayio.Group(max_size=1)
#icon_group.x = 180
#icon_group.y = 120
#icon_group.scale = 1
# view2.append(icon_group)

# Set the font and preload letters
font = bitmap_font.load_font("/fonts/Junction-regular-24.bdf")
# font = bitmap_font.load_font("/fonts/Arial-ItalicMT-17.bdf")
# font = bitmap_font.load_font("/fonts/LeagueSpartan-Bold-16.bdf")
font.load_glyphs(b'abcdefghjiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890- ()')
# Used to calculate vertical text height for Top Alignment
text_hight = Label(font, text="M", color=0x03AD31, max_glyphs=10)

# Default Label styling:
TABS_X = 0
TABS_Y = 0

# Text Label Objects
feed1_label = Label(font, text="Text Window 1", color=0xE39300, max_glyphs=100)
feed1_label.x = TABS_X
feed1_label.y = TABS_Y + 10
splash.append(feed1_label)

feed2_label = Label(font, text="Text Window 2", color=0xFF80FF, max_glyphs=200)
feed2_label.x = TABS_X
feed2_label.y = TABS_Y + 50
splash.append(feed2_label)

sensors_label = Label(font, text="Data View 1", color=0x03AD31, max_glyphs=200)
sensors_label.x = TABS_X
sensors_label.y = TABS_Y + 100
splash.append(sensors_label)

sensor_data = Label(font, text="Data View 2", color=0x03AD31, max_glyphs=100)
sensor_data.x = TABS_X
sensor_data.y =  TABS_Y + 150
view3.append(sensor_data)



board.DISPLAY.show(group)

while 1:
    pass

# return a string with word wrapping using PyPortal.wrap_nicely
def text_box(target, top, max_chars, string):
    text = pyportal.wrap_nicely(string, max_chars)
    new_text = ""
    test = ""
    for w in text:
        new_text += '\n'+w
        test += 'M\n'
    text_hight.text = test
    glyph_box = text_hight.bounding_box
    print(glyph_box[3])
    target.text = "" # Odd things happen without this
    target.y = round(glyph_box[3]/2)+top
    target.text = new_text

while True:
    pass

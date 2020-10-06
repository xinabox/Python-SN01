# First: sudo pigpiod
# Python3!

from time import sleep
import requests
import pigpio
import pynmea2

# Get a token here: http://www.u-blox.com/services-form.html
token="insert_token_here"

pi = pigpio.pi()
addr    = 0x42
bus     = 1
getlen  = 0xFD
getdata = 0xFF

def getAlamanac():
    url=f'http://online-live1.services.u-blox.com/GetOnlineData.ashx?token={token};gnss=gps;datatype=eph,alm,aux,pos;filteronpos;format=aid'
    r = requests.get(url)
    handle = pi.i2c_open(bus, addr)
    pi.i2c_write_device(handle, r.content)
    pi.i2c_close(handle)

def SN01_data():
    rl =0
    handle = pi.i2c_open(bus, addr)
    try:
        dl = pi.i2c_read_word_data(handle, getlen)//256
        if dl>0:
            (rl,data) = pi.i2c_zip(handle,[4,addr, 7,1,getdata, 6,dl, 0])
    except:
        pass
    pi.i2c_close(handle) 
    if rl>0:
        return data.decode(encoding='UTF-8',errors='ignore').splitlines()
    return None

def loop():
    data = SN01_data()
    if data:
        for t in data:
            try:
                msg = pynmea2.parse(t,check=True)
                print(msg.timestamp, msg.latitude, msg.longitude)
            except:
                pass
    sleep(0.1)

getAlamanac()
print("Almanac downloaded")

while(True):
    loop()


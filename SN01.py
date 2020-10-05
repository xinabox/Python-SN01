# First: sudo pigpiod

from time import sleep
import pigpio
import pynmea2

pi = pigpio.pi()
addr    = 0x42
bus     = 1
getlen  = 0xFD
getdata = 0xFF

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

while(True):
    data = SN01_data()
    if data:
        for t in data:
            try:
                msg = pynmea2.parse(t,check=True)
                print(msg.timestamp, msg.latitude, msg.longitude)
            except:
                pass
    sleep(0.1)

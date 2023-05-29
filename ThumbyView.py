import micropython
import select
import time
import thumby
import sys
import machine

machine.freq(240000000)

def text(string):
    thumby.display.fill(0)
    thumby.display.drawText(string, 0, 15, 1)
    thumby.display.update()

@micropython.viper
def display(disp:ptr8):
    thumby.display.fill(0)
    buf = ptr8(thumby.display.display.buffer)
    for y in range(40):
        o = (y >> 3) * 72
        for x in range(72):
            m = 1 << (y & 7)
            if disp[y*72+x]:
                buf[o] |= m
            o += 1
    thumby.display.update()

text("ThumbyView")

# micropython.kbd_intr(-1)

disp_bytes = []
thres = 127

def write_thres(t):
    sys.stdout.write("c".encode("ascii", "ignore"))
    sys.stdout.write(t.to_bytes(1, 'big'))

while True:
    if sys.stdin.read(1) == "d":
        disp_bytes = sys.stdin.read(2880)
        display(disp_bytes)
    disp_bytes = []
    
    if thumby.buttonU.justPressed():
        thres += 1
        if thres > 255:
            thres = 255
        write_thres(t)
    if thumby.buttonL.justPressed():
        thres -= 1
        if thres < 0:
            thres = 0
        write_thres(t)
'''
    ThumbyView! Use your Thumby as a computer monitor.
    By SuperRiley64
'''
from time import sleep
import itertools, math, serial, datetime, io, dxcam, time, numpy, cv2, keyboard
from PIL import Image

print(dxcam.output_info())
print(dxcam.device_info())

cam = dxcam.create()
cam.start()

def get_thumby_screen(disp, thres):
    frame = cam.get_latest_frame()
    if frame is not None:
        frame = cv2.resize(frame, dsize=(72, 40), interpolation=cv2.INTER_NEAREST)
        return rgb_to_bits(frame, thres)
    else:
        return None

def rgb_to_bits(frame, thres):
    disp = [["\0" for i in range(scr_w)] for j in range(scr_h)]
    for y in range(0, len(frame)):
        for x in range(0, len(frame[y])):
            #print(frame[y][x])
            if (frame[y][x][0] + frame[y][x][1] + frame[y][x][2])/3 > thres:
                disp[y][x] = "1"
    return disp

def avg(arr):
    if len(arr) != 0:
        return sum(arr)/len(arr)
    else:
        return 0

ser = serial.Serial("COM6", 115200)

scr_w = 72
scr_h = 40
scr_arr = [["\0" for i in range(scr_w)] for j in range(scr_h)]
fr_no = 0
thres = 15
fpses = []

while(1):
    a = datetime.datetime.now()
    if keyboard.is_pressed("q"):
        cam.stop()
        print("Avg. FPS: " + str(avg(fpses)))
        break
    
    if keyboard.is_pressed("i"):
        thres += 1
        if thres > 255:
            thres = 255
        print("Thres: " + str(thres) + ", FPS: " + str(avg(fpses)))
        fpses = []
    
    if keyboard.is_pressed("o"):
        thres -= 1
        if thres < 1:
            thres = 1
        print("Thres: " + str(thres) + ", FPS: " + str(avg(fpses)))
        fpses = []
    
    if ser.in_waiting > 0:
        in_byte = ser.read()
        if in_byte == "c":
            thres = int(ser.read())
            print(thres)

    scr_arr = get_thumby_screen(scr_arr, thres)
    if scr_arr is not None:
        #print(scr_arr)
        tb_data = "".join(itertools.chain(*scr_arr))
        tb_data = ("d" + tb_data).encode("ascii", "ignore")
        ser.write(tb_data)
        fr_no += 1
        b = datetime.datetime.now()
        c = b - a
        #fpses.append(1000000 / c.microseconds)
        #print("FPS: " + str(1000000 / c.microseconds))

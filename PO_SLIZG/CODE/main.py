import machine
from machine import Pin
import st7789
import time
import math
import screen
import buttons
import greeks as rd
from machine import ADC, PWM
tft=screen.SCREEN()
potentiometer = ADC(28)
sensor = Pin(0, Pin.IN, Pin.PULL_DOWN)
btn = Pin(15, Pin.IN, Pin.PULL_UP)
start=0
obwod=11*2.54*3.14/100
speed=0

ii=1

def speed_(Pin):
    
    global stop
    global start
    global speed
    global ii
    
    stop=start
    start=time.ticks_ms()   
    raz=time.ticks_diff(start,stop)
    if raz>0:
     
        
        speed=(obwod*3.6*1000/raz)/15
        
oo=['sensor','btn']        

sensor.irq(handler=speed_,trigger=Pin.IRQ_RISING,oo,1)
#btn.irq(handler=speed_,trigger=Pin.IRQ_RISING,priority=2)

  

while True:
    time.sleep(1)
    #tft.screen_select(1,speed)
    potentiometer_value = potentiometer.read_u16() * 3.3 / 65536
    print(potentiometer_value)
    
   






























# spi = machine.SPI(0, baudrate=40000000, polarity=1, sck=machine.Pin(6), mosi=machine.Pin(7))
# tft = st7789.ST7789(spi, 240, 320, reset=machine.Pin(12, machine.Pin.OUT), dc=machine.Pin(11, machine.Pin.OUT),rotation=3, inversion=False)
# tft.init()
# button_L = Pin(15, Pin.IN, Pin.PULL_UP)
# button_P = Pin(14, Pin.IN, Pin.PULL_UP)
# 
# a=0
# sx=120
# sy=120
# r=3
# 
# 
# 
# 
# 
# def pointer_poly(length, radius):
#     return [
#         (0, 0),
#         (-radius, radius),
#         (-radius, int(length * 0.3)),
#         (-1, length),
#         (1, length),
#         (radius, int(length * 0.3)),
#         (radius, radius),
#         (0,0)
#     ]
# 
# 
# def angles(sx,sy,r,a):
#    
#     x=r*math.cos(math.radians(a))+sx
#     y=r*math.sin(math.radians(a))+sy
#     x2=(r-20)*math.cos(math.radians(a))+sx
#     y2=(r-20)*math.sin(math.radians(a))+sy
#     return [
#         (1,1),
#         (1,1),
#         (10,10),
#         (15,15)
#         ]
#     
# def angles1(sx,sy,r,a):
#    
#     x=r*math.cos(math.radians(a))+sx
#     y=r*math.sin(math.radians(a))+sy
#     x2=(r-20)*math.cos(math.radians(a))+sx
#     y2=(r-20)*math.sin(math.radians(a))+sy
#     return [
#         int(x),int(y)]
# 
# y_=100
# x_=100
# r_=100
# r_1=90
# tft.fill(st7789.BLACK)
# 
# 
# pi=math.pi*2
# 
# 
# start = time.ticks_ms()
# for i in range (pi*r_):
#     t=i/r_
#     a=(int(math.sin((t)-pi)) + x_)
#     b=(-int(math.cos((t)-pi)) + y_)
#     for x in range(r_1,r_):
#         tft.pixel(a*x, b*x,st7789.BLUE)
#         tft.pixel(a*x,b*x-1 ,st7789.BLUE)
# 
# 
#   
#         
# 
# 
# 
# 
# 
# delta = time.ticks_diff(time.ticks_ms(), start)                
# print(delta)
# 
# import gc
# import os
# 
# def df():
#   s = os.statvfs('//')
#   return ('{0} MB'.format((s[0]*s[3])/1048576))
# 
# def free(full=False):
#   F = gc.mem_free()
#   A = gc.mem_alloc()
#   T = F+A
#   P = '{0:.2f}%'.format(F/T*100)
#   if not full: return P
#   else : return ('Total:{0} Free:{1} ({2})'.format(T,F,P))
# 
# print(free(0))
#tft.fill_polygon([(0,0),(10,10),(10,10),(2,20)],100,100,st7789.BLUE)
#tft.fill_polygon(angles(sx,sy,r,2),angles1(sx,sy,r,2)[0],angles1(sx,sy,r,2)[1],st7789.BLUE)
# 
# print(math.pi/30)
# 
# tft.fill_polygon(pointer_poly(70,1),120,120,st7789.RED,math.pi/30)
# tft.fill_circle(120,120,5,st7789.BLACK)
# tft.polygon(pointer_poly(70,1),120,120,st7789.RED)
# tft.fill_polygon(pointer_poly(70,1),120,120,st7789.RED,math.pi/30)
# tft.fill_circle(120,120,5,st7789.BLACK)
# while True:
#     #start = time.ticks_us() 
#     #tft.text(font_16,"aaa",256,200,st7789.color565(89,90,89),st7789.WHITE)
#     #delta = time.ticks_diff(time.ticks_us(), start)                
#     #print(delta)
#     if button_L.value()==0:
#         
#         tft.fill_polygon(pointer_poly(70,1),120,120,st7789.RED,math.pi/30*angl)
#         tft.fill_circle(120,120,5,st7789.BLACK)
#         angl+=1
#         time.sleep(0.3)
#     if button_P.value()==0:
#         tft.fill_polygon(pointer_poly(70,1),120,120,st7789.RED,math.pi/30*angl)
#         tft.fill_circle(120,120,5,st7789.BLACK)
#         angl=angle-1
#         time.sleep(0.3)
#         
# 
# 



# 
# from machine import Pin, PWM
# from machine import Timer
# from machine import ADC
# import time
# 
# 
# 
# potentiometer = ADC(28)
# #500us bo po +-140us sa drgania
# 
# val=0
# start=0
# sensor = Pin(13, Pin.IN, Pin.PULL_UP)
# button_L = Pin(15, Pin.IN, Pin.PULL_UP)
# button_P = Pin(14, Pin.IN, Pin.PULL_UP)
# obwod=11*2.54*3.14/100
# speed=0
# def speed_(Pin):
#     global stop
#     global start
#     global speed
#     stop=start
#     start=time.ticks_ms()   
#     raz=time.ticks_diff(start,stop)
#     if time.ticks_diff(start,stop)>15:
#         
#         speed=obwod*3.6*1000/time.ticks_diff(start,stop)
#         print(speed,"aaaa",time.ticks_diff(start,stop))
#         
#    
# 
# sensor.irq(handler=speed_,trigger=Pin.IRQ_FALLING)
# 
# while True:
#     # potentiometer_value = potentiometer.read_u16() * 3.3 / 65536
#     #     if sensor.value()==0:
#     #         print(1)
#     #         sleep(0.01)
#     #     elif sensor.value()!=0:
#     #         print(0)
#     #if button_L.value()==0:
#     
#     time.sleep(1)

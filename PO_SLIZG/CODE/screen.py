import machine
import st7789
import time
import math
import vga1_bold_16x32 as font_32
import vga1_bold_16x16 as font_16
import greeks as font_vect

spi = machine.SPI(0, baudrate=40000000, polarity=1, sck=machine.Pin(6), mosi=machine.Pin(7))
display = st7789.ST7789(spi, 240, 320, reset=machine.Pin(12, machine.Pin.OUT), dc=machine.Pin(11, machine.Pin.OUT),rotation=1, inversion=False)
display.init()


import gc
import os

def df():
  s = os.statvfs('//')
  return ('{0} MB'.format((s[0]*s[3])/1048576))

def free(full=False):
  F = gc.mem_free()
  A = gc.mem_alloc()
  T = F+A
  P = '{0:.2f}%'.format(F/T*100)
  if not full: return P
  else : return ('Total:{0} Free:{1} ({2})'.format(T,F,P))



def pointer_poly(length, radius):
    return [
        (0, 0),
        (-radius, radius),
        (-radius, int(length * 0.3)),
        (-1, length),
        (1, length),
        (radius, int(length * 0.3)),
        (radius, radius),
        (0,0)
    ]

class SCREEN:
    prev_screen=0
    screen=1
    vel_prev=0
    vel_act=0
    scale_color=st7789.color565(89,90,89) 
    def __init__(self):
        return
    def screen_main(self):
        if self.prev_screen != 1:
            display.fill(st7789.BLACK)
            r=90
            step=math.pi*r*(3/2)/10
            vel=0
            for i in range(10):
                a=step*i *1.1               
                a+=math.pi*r
                s=int(r*math.sin(a/r))+105
                c=-int(r*math.cos(a/r ))+105
                display.text(font_32,str(vel),s,c,st7789.color565(89,90,89),st7789.BLACK)
                vel+=10
            
            
            
            r=110
            r2=52
            r3=121
         
            for i in range(math.pi*r*(3/2)):
                    i += math.pi * r    
                    s=int(r*math.sin(i/r))
                    c=-int(r*math.cos(i/r ))
                    display.polygon(pointer_poly(-10,1),
                                s + 120,
                                c + 120,
                                self.scale_color,i/r)
                    display.polygon(pointer_poly(-10,1),
                                s + 120 +1,
                                c + 120,
                                self.scale_color,i/r)
                    
            for i in range(math.pi*r3*(3/2)):
                i += math.pi * r3
                display.pixel(int(r3*math.sin(i/r3))+120,-int(r3*math.cos(i/r3 ))+120,st7789.WHITE)
           
            
            for i in range(math.pi*r2*(3/2)):
                    i += math.pi * r2   
                    s2=int(r2*math.sin(i/r2))
                    c2=-int(r2*math.cos(i/r2))
                    display.polygon(pointer_poly(-9,1),
                                s2 + 255 ,
                                c2 + 180 ,
                                self.scale_color,(i)/(r2) )
                    display.polygon(pointer_poly(-9,1),
                                s2 + 255 +1,
                                c2 + 180 ,
                                self.scale_color,(i)/(r2) )

            display.text(font_32,"Km/h",125,160,st7789.color565(89,90,89),st7789.BLACK)
            display.text(font_16,"P(%)",256,200,st7789.color565(89,90,89),st7789.BLACK)
            
        y_=120
        x_=120
        r=111
            
#         while True:
        if  self.vel_prev != self.vel_act:   
            if self.vel_prev< 10:
                display.draw(font_vect,str(int(self.vel_prev)),90,120,st7789.BLACK,3)
            else:
                display.draw(font_vect,str(int(self.vel_prev)),60,120,st7789.BLACK,3)
            if self.vel_act < 10:
                
                display.draw(font_vect,str(int(self.vel_act)),90,120,st7789.WHITE,3) 
            else:          
                display.draw(font_vect,str(int(self.vel_act)),60,120,st7789.WHITE,3) 
            if self.vel_act>self.vel_prev:
                for i in range((math.pi*r*(3/2)-3)*(self.vel_prev/90),(math.pi*r*(3/2)-3)*(self.vel_act/90)):
                        kolor_zmienna = int(i*255/(math.pi*r*(3/2)))
                        kolor = st7789.color565( 0+kolor_zmienna  ,10,      255 - kolor_zmienna)
                        i += math.pi * r
                        i=i+3
                        s_w=int(r*math.sin(i/r)) +x_ 
                        c_w=-int(r*math.cos(i/r )) + y_
                        
                        display.polygon(pointer_poly(-10,1),
                                    s_w,
                                    c_w ,
                                    st7789.WHITE,(i)/(r) )
                        display.polygon(pointer_poly(-10,1),
                                    s_w +1,
                                    c_w ,
                                    st7789.WHITE,(i)/(r) )
                        i=i-3
                        s_s=int(r*math.sin(i/r)) +x_ 
                        c_s=-int(r*math.cos(i/r )) + y_
                        display.polygon(pointer_poly(-9,1),
                                    s_s,
                                    c_s ,
                                    kolor,(i)/(r) )
                        display.polygon(pointer_poly(-9,1),
                                    s_s +1,
                                    c_s,
                                    kolor,(i)/(r) )
                        self.vel_prev=self.vel_act
                
            elif self.vel_act<self.vel_prev:
                 
                for i in range((math.pi*r*(3/2)-3)*(self.vel_prev/90),(math.pi*r*(3/2)-3)*(self.vel_act/90),-1):
                           
                            i += math.pi * r     
                            s_w=int(r*math.sin(i/r)) +x_ 
                            c_w=-int(r*math.cos(i/r )) + y_
                            display.polygon(pointer_poly(-10,1),
                                    s_w,
                                    c_w ,
                                    st7789.WHITE,(i)/(r) )
                            display.polygon(pointer_poly(-10,1),
                                    s_w +1,
                                    c_w ,
                                    st7789.WHITE,(i)/(r) )
                            
                            i=i+3
                            s_s=int(r*math.sin(i/r)) +x_ 
                            c_s=-int(r*math.cos(i/r )) + y_
                            display.polygon(pointer_poly(-9,1),
                                        s_s ,
                                        c_s ,
                                        self.scale_color,(i)/(r) )
                            display.polygon(pointer_poly(-9,1),
                                        s_s +1,
                                        c_s,
                                        self.scale_color,(i)/(r) )
                            self.vel_prev=self.vel_act
                
#                 for i in range(math.pi*r*(3/2)-3):                    
#                     kolor_zmienna = int(i*255/(math.pi*r*(3/2)))
#                     kolor = st7789.color565( 0+kolor_zmienna  ,10,      255 - kolor_zmienna)
#                     i += math.pi * r
#                     i=i+3
#                     s_w=int(r*math.sin(i/r)) +x_ 
#                     c_w=-int(r*math.cos(i/r )) + y_
#                     
#                     display.polygon(pointer_poly(-10,1),
#                                 s_w,
#                                 c_w ,
#                                 st7789.WHITE,(i)/(r) )
#                     display.polygon(pointer_poly(-10,1),
#                                 s_w +1,
#                                 c_w ,
#                                 st7789.WHITE,(i)/(r) )
#                     i=i-3
#                     s_s=int(r*math.sin(i/r)) +x_ 
#                     c_s=-int(r*math.cos(i/r )) + y_
#                     display.polygon(pointer_poly(-9,1),
#                                 s_s,
#                                 c_s ,
#                                 kolor,(i)/(r) )
#                     display.polygon(pointer_poly(-9,1),
#                                 s_s +1,
#                                 c_s,
#                                 kolor,(i)/(r) )
#                   
#                     
#                         
#                 for i in range(math.pi*r*(3/2)-3,0,-1):
#                         i += math.pi * r     
#                         s_w=int(r*math.sin(i/r)) +x_ 
#                         c_w=-int(r*math.cos(i/r )) + y_
#                         display.polygon(pointer_poly(-10,1),
#                                 s_w,
#                                 c_w ,
#                                 st7789.WHITE,(i)/(r) )
#                         display.polygon(pointer_poly(-10,1),
#                                 s_w +1,
#                                 c_w ,
#                                 st7789.WHITE,(i)/(r) )
#                         
#                         i=i+3
#                         s_s=int(r*math.sin(i/r)) +x_ 
#                         c_s=-int(r*math.cos(i/r )) + y_
#                         display.polygon(pointer_poly(-9,1),
#                                     s_s ,
#                                     c_s ,
#                                     self.scale_color,(i)/(r) )
#                         display.polygon(pointer_poly(-9,1),
#                                     s_s +1,
#                                     c_s,
#                                     self.scale_color,(i)/(r) )
#                         
#                 for i in range(math.pi*r2*(3/2)):
#                         kolor_zmienna = int(i*255/(math.pi*r2*(3/2)))
#                   
#                         kolor = st7789.color565( 0+kolor_zmienna  ,0,      255 - kolor_zmienna)
#                         i += math.pi * r2   
#                         s2=int(r2*math.sin(i/r2))
#                         c2=-int(r2*math.cos(i/r2))
#                         display.polygon(pointer_poly(-9,1),
#                                     s2 + 255 ,
#                                     c2 + 180 ,
#                                     kolor,(i)/(r2) )
#                         display.polygon(pointer_poly(-9,1),
#                                     s2 + 255 +1,
#                                     c2 + 180 ,
#                                     kolor,(i)/(r2) )
#                         time.sleep(0.01)
#                 for i in range(math.pi*r2*(3/2),0,-1):
#                         i += math.pi * r2   
#                         s2=int(r2*math.sin(i/r2))
#                         c2=-int(r2*math.cos(i/r2))
#                         display.polygon(pointer_poly(-9,1),
#                                     s2 + 255 ,
#                                     c2 + 180 ,
#                                     self.scale_color,(i)/(r2) )
#                         display.polygon(pointer_poly(-9,1),
#                                     s2 + 255 +1,
#                                     c2 + 180 ,
#                                     self.scale_color,(i)/(r2) )
#                             
        self.prev_screen=1
        
    def screen_stats(self):
        if self.prev_screen != 2:
            display.fill(st7789.WHITE)
          
            display.text(font_32,"Voltage: ",10,10,st7789.color565(89,90,89),st7789.WHITE)
            display.text(font_32,"Current: ",10,42,st7789.color565(89,90,89),st7789.WHITE)
            display.text(font_32,"Power: ",10,74,st7789.color565(89,90,89),st7789.WHITE)
            display.text(font_32,"Motor temp: ",10,106,st7789.color565(89,90,89),st7789.WHITE)
            display.hline(0,9,320,st7789.RED)
            display.rect(11,11,143,38,st7789.RED)
            self.prev_screen=2
        
        
    def screen_select(self,screen,vel):
        self.vel_act=vel
        if screen==1:
            self.screen_main()
        elif screen==2:
            self.screen_stats()





# 
# 
# 
y_=120
x_=120
r=110
# r1=100
# display.fill(st7789.WHITE)
# 
# pi=math.pi*2
# 
# start = time.ticks_ms()
 
# for i in range(math.pi*r*(4/3)):
#      
#         kolor_zmienna = int(i*255/(math.pi*r*(4/3)))
#         print(kolor_zmienna)
#         kolor = st7789.color565( 0+ kolor_zmienna   ,20,      255 - kolor_zmienna)
#         i += math.pi * r   
#  
#         display.polygon(pointer_poly(-9,1),
#                     int(r*math.sin(i/r)) +x_ ,
#                     -int(r*math.cos(i/r )) + y_ ,
#                     kolor,(i)/(r) )
#         display.polygon(pointer_poly(-9,1),
#                     int(r*math.sin(i/r)) +x_ +1,
#                     -int(r*math.cos(i/r )) + y_ ,
#                     kolor,(i)/(r) )
        
#         
# for i in range(math.pi*r*(4/3),0,-1):
#         i += math.pi * r     
# 
#         display.polygon(pointer_poly(-9,1),
#                     int(r*math.sin(i/r)) +x_ ,
#                     -int(r*math.cos(i/r )) + y_ ,
#                     st7789.BLACK,(i)/(r) )
#         display.polygon(pointer_poly(-9,1),
#                     int(r*math.sin(i/r)) +x_ +1,
#                     -int(r*math.cos(i/r )) + y_ ,
#                     st7789.BLACK,(i)/(r) )
#         




#delta = time.ticks_diff(time.ticks_ms(), start)                
#print(delta)


# tft=SCREEN()        
# while True:
#     tft.screen_select(1,40)
#     
#     time.sleep(3)
#     tft.screen_select(1,60)
#     
#     time.sleep(3)
#     tft.screen_select(1,40)
#     
#     time.sleep(3)
#     tft.screen_select(1,80)
#     
#     time.sleep(3)
#    
#     
#     

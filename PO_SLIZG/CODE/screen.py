import machine
import st7789
import time
import math
import vga1_bold_16x32 as font_32
import vga1_bold_16x16 as font_16
import greeks as font_vect
import romant as font_vect_1


spi = machine.SPI(0, baudrate=40000000, polarity=1, sck=machine.Pin(6), mosi=machine.Pin(7))
display = st7789.ST7789(spi, 240, 320, reset=machine.Pin(12, machine.Pin.OUT), dc=machine.Pin(11, machine.Pin.OUT),rotation=3, inversion=False)
display.init()

######################### testy
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
  
  
  
from machine import ADC, PWM 
potentiometer = ADC(28)
potentiometer_1= ADC(27)
potentiometer_2 = ADC(26)

#################################


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
    ### Deklaracja zmiennych klasy
    prev_screen=prev_velocity=prev_voltage=prev_current=prev_throttle=0
    screen=1       
    scale_color=st7789.color565(89,90,89) 
    def __init__(self):
        return

###--------------------------------------------------### Ekran 1
    def screen_main(self,velocity):
        if self.prev_screen != 1:
            display.fill(st7789.BLACK)
            r=90
            step=math.pi*r*(3/2)/10
            vel=0
            ### Rysowanie znaczników od prędkości
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
            ### Rysowanie licznika prędkości
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
           
            ### Rysowanie wskaźnika baterii
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
            
#        while True:

        ### 
        if  self.prev_velocity != velocity:
            
            ### Wyświetlanie prędkości cyfrowej 
            if self.prev_velocity< 10:
                display.draw(font_vect,str(int(self.prev_velocity)),90,120,st7789.BLACK,3)
            else:
                display.draw(font_vect,str(int(self.prev_velocity)),60,120,st7789.BLACK,3)
            if self.act_velocity < 10:                
                display.draw(font_vect,str(int(self.act_velocity)),90,120,st7789.WHITE,3) 
            else:          
                display.draw(font_vect,str(int(self.act_velocity)),60,120,st7789.WHITE,3)
            
                
            ### Rysowanie smugi na prędkościomierzu
            if self.act_velocity>self.prev_velocity:
                for i in range((math.pi*r*(3/2)-3)*(self.prev_velocity/90),(math.pi*r*(3/2)-3)*(self.act_velocity/90)):
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
                        self.prev_velocity=self.act_velocity
                
            elif self.act_velocity<self.prev_velocity:
                 
                for i in range((math.pi*r*(3/2)-3)*(self.prev_velocity/90),(math.pi*r*(3/2)-3)*(self.act_velocity/90),-1):
                           
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
                            self.prev_velocity=self.act_velocity
                

        self.prev_screen=1


###--------------------------------------------------### Ekran 2
    def screen_stats(self,current,voltage,throttle):
        y_t=90
        y_p=150
        current=int((current-1.9)*240/1.3)
        voltage=int((voltage-1.9)*240/1.3)
        throttle=int((throttle-1.9)*240/1.3)
        
        prev_power=int(self.prev_current*self.prev_voltage)
        power=int(current*voltage)
        
        
        
        
        if self.prev_screen != 2:
            display.fill(st7789.BLACK)
#             for n in "THROTTLE":
#                 display.text(font_16,n,274,y_t,st7789.WHITE,st7789.BLACK)
#                 y_t+=16
#             for n in "POWER":
#                 display.draw(font_vect_1,n,0,y_p,st7789.WHITE,0.6) 
#                 y_p+=20
            self.prev_screen=2
            
        ### Usuniecie falowania wskaźnika   ##------- do poprawy  
#         if v1-int((current-1.9)*240/1.3)>10: 
#             v1=int((current-1.9)*240/1.3)
#         elif int((current-1.9)*240/1.3)-v1>10:
#             v1=int((current-1.9)*240/1.3)

        ### Rysowanie wskaźnika od mocy/gazu  ##------- do rozdzielenia na dwa w zależności od dwóch parametrów
    
            
          
  
            
#             for n in "POWER":
#                 display.draw(font_vect_1,n,0,y_p,st7789.WHITE,0.7) 
#                 y_p+=20
#             for n in "THROTTLE":
#                 display.draw(font_vect_1,n,305,y_t,st7789.WHITE,0.7) 
#                 y_t+=20

        print(int(current))
        print(int(voltage))
        time.sleep(1)
        if int(throttle)>self.prev_throttle:
            for i in range(240-self.prev_throttle,240-int(throttle),-1):
                display.hline(290,i,30,st7789.color565(240-i,0+i,0))
                display.hline(290,i-1,30,st7789.color565(240-i,0+i,0))
            
        if int(throttle)<self.prev_throttle:
            for i in range(240-self.prev_throttle,240-int(throttle)):
                 display.hline(290,i,30,st7789.color565(0,0,0))
                 display.hline(290,i+1,30,st7789.color565(0,0,0))
            
        if power>prev_power:
            for i in range(240-prev_power,240-power,-1):
                display.hline(0,i,30,st7789.color565(240-i,0+i,0))
                display.hline(0,i-1,30,st7789.color565(240-i,0+i,0))
        
        if power<prev_power:
            for i in range(240-prev_power,240-power):
                 display.hline(0,i,30,st7789.color565(0,0,0))
                 display.hline(0,i+1,30,st7789.color565(0,0,0))
            
       
           
             
            
        prev_power=power
        self.prev_current=current
        self.prev_voltage=voltage
        self.prev_throttle=int(throttle)
#             display.fill(st7789.WHITE)
#           
#             display.text(font_32,"Voltage: ",10,10,st7789.color565(89,90,89),st7789.WHITE)
#             display.text(font_32,"Current: ",10,42,st7789.color565(89,90,89),st7789.WHITE)
#             display.text(font_32,"Power: ",10,74,st7789.color565(89,90,89),st7789.WHITE)
#             display.text(font_32,"Motor temp: ",10,106,st7789.color565(89,90,89),st7789.WHITE)
#             display.hline(0,9,320,st7789.RED)
#             display.rect(11,11,143,38,st7789.RED)
#             self.prev_screen=2
#         display.text(font_32,str(current),160,42,st7789.color565(89,90,89),st7789.WHITE)
#         power= (current -1.60)/0.0264
#         display.text(font_32,str(power),160,74,st7789.color565(89,90,89),st7789.WHITE)
        
   
   
###-------------------------------------------### Wybór wyświetlanego ekranu   
    def screen_select(self,screen,velocity,current,voltage,throttle):
       
        if screen==1:
            self.screen_main(velocity)
        elif screen==2:
            self.screen_stats(current,voltage,throttle)



### pętla testowa
tft=SCREEN()        
while True:
    potentiometer_value = potentiometer.read_u16() * 3.3 / 65536
    value_1 = potentiometer_1.read_u16() * 3.3 / 65536
    value_2 = potentiometer_2.read_u16() * 3.3 / 65536
    
    tft.screen_select(2,40,value_1,value_2,potentiometer_value)
 
   
#########
    
    ###
    
    ###
    
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

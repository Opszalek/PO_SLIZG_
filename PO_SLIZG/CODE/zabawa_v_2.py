import  time, st7789,math
from machine import Pin, SPI

############## TUTAJ STWÓRZ OBEIKT SPI ###############

spi = machine.SPI(0, baudrate=40000000, polarity=1, sck=machine.Pin(6), mosi=machine.Pin(7))
IPS = st7789.ST7789(spi, 240, 320, reset=machine.Pin(12, machine.Pin.OUT), dc=machine.Pin(11, machine.Pin.OUT),rotation=3, inversion=False)
IPS.init()

##################=====================################
def obrecz_sinusy(r,ym,xm,kolor):
    for i in  range(math.pi *r):      
        i += math.pi * r/2       #Zrotowanie rysowania koła
        IPS.pixel(-int(r*math.sin(i/r)) +xm ,int(r*math.cos(i/r)) + ym , kolor)

def obrecz_bez_sinusow(r,ym,xm,kolor):
    for i in range(2):      
        f, ddF_x ,ddF_y, x,y =  1 - r, 1, -2* r, 0 ,r 
        while (y > 0):
            
            if x < y:
                if (f >= 0) :
                    y -= 1
                    ddF_y += 2
                    f += ddF_y           
                x += 1;
                ddF_x += 2;
                f += ddF_x;
                rysowanie(ym,xm,kolor,y,x, 1+(i*2))
                                
            elif x >= y : 
                if (f >= 0) :
                    x += 1;
                    ddF_y -= 2
                    f += ddF_y 
                y -= 1
                ddF_x -= 2;
                f += ddF_x
                rysowanie(ym,xm,kolor,y,x, 2+(i*2))

def rysowanie(ym,xm,kolor,y,x, cwiartka):
    if cwiartka == 1:
        IPS.pixel(xm-y, ym -x  ,kolor)
    elif cwiartka == 2:
        IPS.pixel(xm-y ,ym-x   ,kolor)
    elif cwiartka == 3:
        IPS.pixel(xm +x,ym-y   ,kolor)
    elif cwiartka == 4:
        IPS.pixel(xm +x,ym-y  ,kolor)


ym = 145                            # Środek po y
xm= 160                             # Środek po x 
r = 140                             # Promień obręczy 
kolor = st7789.color565(200,50,50)  # Kolor obręczy

start = time.ticks_us()                          # Czas start 
obrecz_sinusy(r,ym,xm,kolor)                     # Wywołanie funkcji 
delta = time.ticks_diff(time.ticks_us(), start)  # Policzenie upłyniętego czasu w nano-sekundach
print('Obrecz Z uzyciem trygonometrii:        ' + str(delta/1000) + ' ms')

start2 = time.ticks_us()
obrecz_bez_sinusow(r,ym+65,xm,kolor)
delta2 = time.ticks_diff(time.ticks_us(), start2)
print('Obrecz BEZ uzycia trygonometrii:      ' + str(delta2/1000) + ' ms')
print('Bez uzycia trygonometrii szybciej o:   ' + str(round(100*delta/delta2))+'%') 


################## Przy użyciu @micropython.native ###########################

@micropython.native
def obrecz_sinusy_native(r,ym,xm,kolor):
    for i in  range(math.pi *r):      
        i += math.pi * r/2       #Zrotowanie rysowania koła
        IPS.pixel(-int(r*math.sin(i/r)) +xm ,int(r*math.cos(i/r)) + ym , kolor)
        
@micropython.native
def obrecz_bez_sinusow_native(r,ym,xm,kolor):
    for i in range(2):      
        f, ddF_x ,ddF_y, x,y =  1 - r, 1, -2* r, 0 ,r 
        while (y > 0):
            
            if x < y:
                if (f >= 0) :
                    y -= 1
                    ddF_y += 2
                    f += ddF_y           
                x += 1;
                ddF_x += 2;
                f += ddF_x;
                rysowanie(ym,xm,kolor,y,x, 1+(i*2))
                                
            elif x >= y : 
                if (f >= 0) :
                    x += 1;
                    ddF_y -= 2
                    f += ddF_y 
                y -= 1
                ddF_x -= 2;
                f += ddF_x
                rysowanie(ym,xm,kolor,y,x, 2+(i*2))
                
@micropython.native
def rysowanie_native(ym,xm,kolor,y,x, cwiartka):
    if cwiartka == 1:
        IPS.pixel(xm-y, ym -x  ,kolor)
    elif cwiartka == 2:
        IPS.pixel(xm-y ,ym-x   ,kolor)
    elif cwiartka == 3:
        IPS.pixel(xm +x,ym-y   ,kolor)
    elif cwiartka == 4:
        IPS.pixel(xm +x,ym-y  ,kolor)


ym_native = 145                     # Środek po y
xm_native= 160                      # Środek po x 
r = 140                             # Promień obręczy 
kolor_native = st7789.color565(50,200,50)  # Kolor obręczy

start3 = time.ticks_us()                                     # Czas start 
obrecz_sinusy_native(r,ym_native+30,xm_native,kolor_native)  # Wywołanie funkcji 
delta3 = time.ticks_diff(time.ticks_us(), start3)            # Policzenie upłyniętego czasu w nano-sekundach
print('Obrecz Z uzyciem trygonometri NATIVE:           ' + str(delta3/1000) + ' ms')

start4 = time.ticks_us()
obrecz_bez_sinusow_native(r,ym_native+90,xm_native,kolor_native)
delta4 = time.ticks_diff(time.ticks_us(), start4)
print('Obrecz BEZ uzycia trygonometrii z NATIVE:     '  + str(delta4/1000) + ' ms')
print('Bez uzycia trygonometrii  szybciej o:                 ' + str(round(100*delta/delta4))+'%') 


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
# 
# ym = 150         #środek po y
# xm= 160          #środek po x 
# r = 140          #Zewnętrzny promień pierścienia 
# odcinek = 20     #Długość pierścienia (Rysowana do Wewnątrz)
# wskazowka = 20   #Długość wskazówki 
# # 
# # @micropython.native
# def speedometer_plus():
#     for i in range(math.pi*r):
#         kolor_zmienna = int(i*81/(r))           #Konwertowanie ilości iteracji, aby zawsze k było w przedzaile [0-255]
#         kolor = st7789.color565( 0+ kolor_zmienna   ,20,      255 - kolor_zmienna)
#         
#         #Ta część musi być po obliczeniu koloru 
#         i += math.pi * r/2       #Zrotowanie rysowania koła (Pozmieniaj wartości i zobacz co się dzieje) 
#         math.sqrt((1 - math.cos((i)/r))/2)
#   
#   
#         ####### POLYGON #####
#         IPS.polygon(pointer_poly(-wskazowka,1),
#                     -int(r*math.sin((i+3)/r)) +xm + int(2 * math.sin(i/r)),
#                     int(r*math.cos((i+3)/r)) + ym - int(2*math.cos(i/r)) ,
#                     st7789.GREEN,
#                     (i)/(r) )
#         
# 
#         #Rysowanie lini pomiędzy 2 obręczami 
#         IPS.line(-int(r*math.sin(i/r)) +xm        ,
#              int(r*math.cos(i/r)) + ym ,
#              -int(r*math.sin(i/r)) +xm + int(odcinek * math.sin(i/r)) ,
#              int(r*math.cos(i/r)) + ym - int(odcinek*math.cos(i/r)), kolor)
#         #Rysowanie 2 lini pomiędzy obręczami jeden pixel na y niżej aby wypełnić całość 
# #         IPS.line(-int(r*math.sin((i)/r)) +xm        ,
# #          int(r*math.cos(i/r)) + ym-1  ,
# #          -int(r*math.sin(i/r)) +xm + int(odcinek * math.sin((i)/r)) ,
# #          int(r*math.cos(i/r)) + ym - int(odcinek*math.cos((i)/r))-1, kolor)
#         #Rysowanie 2 lini pomiędzy obręczami jeden pixel na y niżej aby wypełnić całość 
#         IPS.line(-int(r*math.sin((i)/r)) +xm-1        ,
#          int(r*math.cos(i/r)) + ym  ,
#          -int(r*math.sin(i/r)) +xm + int(odcinek * math.sin((i)/r)-1) ,
#          int(r*math.cos(i/r)) + ym - int(odcinek*math.cos((i)/r)), kolor)
#         
#         
#         #Czyszczenie po wskazówce
# #         IPS.line(-int(r*math.sin((i-2)/r)) +xm + int(odcinek * math.sin((i-2)/r))  ,
# #              int(r*math.cos((i-2)/r)) + ym - int(odcinek*math.cos((i-2)/r)) ,
# #              -int(r*math.sin((i-2)/r)) +xm + int(odcinek * math.sin((i-2)/r)) + int((wskazowka -odcinek+5) * math.sin((i-2)/r)) ,
# #              int(r*math.cos((i-2)/r)) + ym - int(odcinek*math.cos((i-2)/r))- int((wskazowka -odcinek+5)*math.cos((i-2)/r)),
# #                  st7789.BLACK)
#         
# #         IPS.line(-int(r*math.sin(i/r)) +xm + int(odcinek * math.sin(i/r))  ,
# #              int(r*math.cos(i/r)) + ym - int(odcinek*math.cos(i/r)) -1,
# #              -int(r*math.sin(i/r)) +xm + int(odcinek * math.sin(i/r)) + int((wskazowka -odcinek+5) * math.sin(i/r)) ,
# #              int(r*math.cos(i/r)) + ym - int(odcinek*math.cos(i/r))- int((wskazowka -odcinek+5)*math.cos(i/r)) -1,
# #                  st7789.BLACK)
# #         
# #         IPS.line(-int(r*math.sin(i/r)) +xm + int(odcinek * math.sin(i/r)) -1 ,
# #              int(r*math.cos(i/r)) + ym - int(odcinek*math.cos(i/r)) ,
# #              -int(r*math.sin(i/r)) +xm + int(odcinek * math.sin(i/r)) + int((wskazowka -odcinek+5) * math.sin(i/r))-1 ,
# #              int(r*math.cos(i/r)) + ym - int(odcinek*math.cos(i/r))- int((wskazowka -odcinek+5)*math.cos(i/r)) ,
# #                  st7789.BLACK)        
# 
# 
# 
# 
# def speedometer_minus():
#     for i in range(math.pi*r):
#         kolor_zmienna = int(i*81/(r))     #Konwertowanie ilości iteracji, aby zawsze k było w przedzaile [0-255]
#         kolor = st7789.BLACK
#         
#         #Ta część musi być po obliczeniu koloru 
#         i -= math.pi * r/2       #Zrotowanie rysowania koła (Pozmieniaj wartości i zobacz co się dzieje) 
#         math.sqrt((1 - math.cos((i)/r))/2)
#   
#         rotacja =(-i)/(r)   
#         if rotacja <0:
#             rotacja += 2*math.pi 
#         ####### POLYGON #####
#         IPS.polygon(pointer_poly(+wskazowka,1),
#                     -int(r*math.sin((i+3)/r)) +xm + int(2 * math.sin(i/r)),
#                     -int(r*math.cos((i+3)/r)) + ym +int(2* math.cos(i/r)) ,
#                     st7789.GREEN,
#                     rotacja )
#       
#         
#         #Rysowanie lini pomiędzy 2 obręczami 
#         IPS.line(-int(r*math.sin(i/r)) +xm,
#              -int(r*math.cos(i/r)) + ym ,
#              -int(r*math.sin(i/r)) +xm + int(odcinek * math.sin(i/r)) ,
#              -int(r*math.cos(i/r)) + ym + int(odcinek*math.cos(i/r)), kolor)
#         #Rysowanie 2 lini pomiędzy obręczami jeden pixel na y niżej aby wypełnić całość 
#         IPS.line(-int(r*math.sin((i)/r)) +xm        ,
#          -int(r*math.cos(i/r)) + ym  ,
#          -int(r*math.sin(i/r)) +xm + int(odcinek * math.sin((i)/r)) ,
#          -int(r*math.cos(i/r)) + ym + int(odcinek*math.cos((i)/r))+1, kolor)
#         #Rysowanie 2 lini pomiędzy obręczami jeden pixel na y niżej aby wypełnić całość 
#         IPS.line(-int(r*math.sin((i)/r)) +xm+1       ,
#          -int(r*math.cos(i/r)) + ym  ,
#          -int(r*math.sin(i/r)) +xm + int(odcinek * math.sin((i)/r)+1) ,
#          -int(r*math.cos(i/r)) + ym + int(odcinek*math.cos((i)/r)), kolor)
#         
#         
#         #Czyszczenie po wskazówce
#         IPS.line(-int(r*math.sin((i-3)/r)) +xm + int(odcinek * math.sin((i-3)/r))  ,
#              -int(r*math.cos((i-3)/r)) + ym + int(odcinek*math.cos((i-3)/r)) ,
#              -int(r*math.sin((i-3)/r)) +xm + int(odcinek * math.sin((i-3)/r)) + int((wskazowka -odcinek+5) * math.sin((i-3)/r)) ,
#              -int(r*math.cos((i-3)/r)) + ym + int(odcinek*math.cos((i-3)/r))+ int((wskazowka -odcinek+5)*math.cos((i-3)/r)),
#                  st7789.BLACK)
#         
#         IPS.line(-int(r*math.sin(i/r)) +xm + int(odcinek * math.sin(i/r))   ,
#             -int(r*math.cos(i/r)) + ym + int(odcinek*math.cos(i/r)),
#             -int(r*math.sin(i/r)) +xm + int(odcinek * math.sin(i/r)) + int((wskazowka -odcinek+5) * math.sin(i/r)) ,
#             -int(r*math.cos(i/r)) + ym +int(odcinek*math.cos(i/r))+ int((wskazowka -odcinek+5)*math.cos(i/r))+1 ,
#                  st7789.BLACK)
#         
#         IPS.line(-int(r*math.sin(i/r)) +xm + int(odcinek * math.sin(i/r)) +1 ,
#              -int(r*math.cos(i/r)) + ym +int(odcinek*math.cos(i/r)) ,
#              -int(r*math.sin(i/r)) +xm + int(odcinek * math.sin(i/r)) + int((wskazowka -odcinek+5) * math.sin(i/r))+1 ,
#              -int(r*math.cos(i/r)) +ym + int(odcinek*math.cos(i/r))+int((wskazowka -odcinek+5)*math.cos(i/r)) ,
#                  st7789.BLACK)        
# 
# 
# for i in range(4):       
#     start = time.ticks_us()
#     speedometer_plus()
#     delta = time.ticks_diff(time.ticks_us(), start)                
#     print('Zamkniecie licznika w: '+ str(delta/1000000)+ ' s')
#     start = time.ticks_us()
#     speedometer_minus()
#     delta = time.ticks_diff(time.ticks_us(), start)                
#     print('Zwolnienie do 0 w: '+ str(delta/1000000)+ ' s')
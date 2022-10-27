from machine import Pin
import time
button_1 = Pin(15, Pin.IN, Pin.PULL_UP)
button_2 = Pin(14, Pin.IN, Pin.PULL_UP)

class button:
    def __init__(self):
        if btn==0:
            self.name="lewy"
        elif btn==1:
            self.name="prawy"
        return
    def raz(self):
        print(12)
    def click(self):
        if button_1.value()==0:
            return
        if button_2.value()==0:
            return
from machine import Pin, PWM
from time import sleep

class Controller:
     ON = 0
     MID = 256
     OFF = 1023
     def __init__(self, r, g, b, f=5000, anode=False):
          if not anode:
            self.ON = 0
            self.MID = 768
            self.OFF = 1023
          self.frequency = f
          self.anode=anode
          self.RED = PWM(Pin(r, pull=Pin.PULL_UP), self.frequency)
          self.GREEN = PWM(Pin(g, pull=Pin.PULL_UP), self.frequency)
          self.BLUE = PWM(Pin(b, pull=Pin.PULL_UP), self.frequency)
          self.COLOR={"black":[self.OFF,self.OFF,self.OFF], "red":[self.ON,self.OFF,self.OFF],
                         "green":[self.OFF,self.ON,self.OFF],"blue":[self.OFF,self.OFF,self.ON],
                         "yellow":[self.ON,self.ON,self.OFF],"orange":[self.ON,self.MID,self.OFF],
                         "pink":[self.ON,self.OFF,self.MID],"purple":[self.ON,self.OFF,self.ON],
                         "cyan":[self.OFF,self.ON,self.ON],"white":[self.ON,self.ON,self.ON]}
          self.boot()

     def set(self,c):
          if c in self.COLOR.keys():
               self.RED.duty(self.COLOR[c][0])
               self.GREEN.duty(self.COLOR[c][1])
               self.BLUE.duty(self.COLOR[c][2])
               return True
          return False
        
     def man(self,r,g,b):
          if r < 0 or r > 1023 or g < 0 or g > 1023 or b < 0 or b > 1023:
               return False
          self.RED.duty(r)
          self.GREEN.duty(g)
          self.BLUE.duty(b)
          return True

     def boot(self):
          for i in self.COLOR.keys():
               if "black" not in i:
                    self.set(i)
                    sleep(0.2)
          self.set('white')

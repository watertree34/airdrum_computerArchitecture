import RPi.GPIO as GPIO
import pygame
import time
import smbus

address = 0x48

AIN0 = 0x40    #photodiode
AIN1 = 0x41    #thermister
AIN2 = 0x42  
AIN3 = 0x43    #potentiometer

bus = smbus.SMBus(1)

    
GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT)
GPIO.setup(25, GPIO.IN)
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

kick=pygame.mixer.Sound("kickdrum.ogg")
snare=pygame.mixer.Sound("snaredrum.ogg")

beforeKick=100
beforeSnare=0

ledTime=0

score=0
kickBool=False
handBool=False

try:
    while True:
        bus.write_byte(address, AIN2)
        
        nowKick = bus.read_byte(address)
        nowSnare = GPIO.input(25)
        
        
        if(nowKick-beforeKick > 50):
            kick.set_volume(1)
            kick.play(0)
            #time.sleep(0.1)
            kickBool=True
        else:
            kickBool=False
            
        if(beforeSnare-nowSnare ==1 ):  
            snare.set_volume(0.5)
            snare.play(0)
            handBool=True
            #time.sleep(0.1)
        else:
            handBool=False
        
        
        ledTime += 1
        
        if(ledTime>=50):
            GPIO.output(23,True)
            if(ledTime>=100):
                ledTime=0
            elif(handBool or kickBool):
                score+=1
                print("score: "+str(score) )
                
                
        else:
            GPIO.output(23,False)
        
        #print(nowKick)
        #print(nowSnare)
        
        beforeKick = nowKick
        beforeSnare = nowSnare
        clock.tick(50)
        
        
except KeyboardInterrupt: 
    GPIO.cleanup()
    pygame.quit()
    
import RPi.GPIO as GPIO   # 라즈베리 파이 gpio임포트
import pygame   # 소리를 내기위해 pygame 임포트
import time       # 시간을 재주는 time임포트 
import smbus     # ad컨버터 사용을 위한 smbus임포트

address = 0x48   # ad컨버터 주소

AIN0 = 0x40    #photodiode
AIN1 = 0x41    #thermister
AIN2 = 0x42     # 외부센서 - 조도센서
AIN3 = 0x43    #potentiometer

bus = smbus.SMBus(1)  # ad컨버터에 사용

    
GPIO.setmode(GPIO.BCM)   # gpio셋팅

GPIO.setup(23, GPIO.OUT)  # 23번 핀 gpio 출력으로 설정 - led
GPIO.setup(25, GPIO.IN)   # 25번 핀 gpio 입력으로 설정 - 기울기 센서
pygame.init()  # pygame초기화
pygame.mixer.init()  # pygame mixer초기화
clock = pygame.time.Clock() # pygame clock 변수

kick=pygame.mixer.Sound("kickdrum.ogg")  # kick드럼(다리) 소리 저장 
snare=pygame.mixer.Sound("snaredrum.ogg")  # snare드럼(팔) 소리 저장

beforeKick=100   # 이전 프레임 조도센서 값 변수
beforeSnare=0    # 이전 프레임 기울기센서 값 변수

ledTime=0    # 프레임을 카운트할 led변수


score=0   # 점수 변수
kickBool=False   # 다리 드럼밟았는지 체크하는 변수
handBool=False  # 팔 드럼쳤는지 체크하는 변수

try:
    while True:
        bus.write_byte(address, AIN2)   #외부 조도센서 값 읽어오기 
        
        nowKick = bus.read_byte(address)  # 현재 조도센서 값 저장 
        nowSnare = GPIO.input(25)  # 현재 기울기센서 값 저장
        
        
        if(nowKick-beforeKick > 50):   # 만약 현재 조도센서 값이 이전 조도센서 값보다 50이상 크다면(=어두워졌다면)
            kick.set_volume(1)
            kick.play(0)		# 킥 드럼 소리 재생
            #time.sleep(0.1)
            kickBool=True
        else:
            kickBool=False
            
        if(beforeSnare-nowSnare ==1 ):  # 만약 기울기 센서 값이 1에서 0으로 바뀌었다면(=기울기가 지면과 수직에서 수평이 되었다면)  
            snare.set_volume(0.5)
            snare.play(0)                 # 스네어 드럼 소리 재생
            handBool=True
            #time.sleep(0.1)
        else:
            handBool=False
        
        
        ledTime += 1  # 매 프레임 ledTime 1씩 증가
        
        if(ledTime>=50):   # 만약 ledTime이 50이상이 되었다면
            GPIO.output(23,True)   # 50~100동안 led켜기
            if(ledTime>=100):    # 100이상이 되었다면
                ledTime=0       # 다시 0으로 초기화
            elif(handBool or kickBool):    #만약 ledTime 50~100일때 손이나 다리 드럼을 쳤다면
                score+=1   # 점수 증가
                print("score: "+str(score) )
                
                
        else:
            GPIO.output(23,False)   # ledTime 0~50은 led끄기
        
        #print(nowKick)
        #print(nowSnare)
        
        beforeKick = nowKick		# 프레임 마지막에 현재 상태를 이전 상태로 저장함
        beforeSnare = nowSnare
        clock.tick(50)
        
        
except KeyboardInterrupt:   # ctrl+c를 누르면 종료
    GPIO.cleanup()
    pygame.quit()
    
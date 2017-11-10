import subprocess#Dat is voor het pingen
import socket#Zorgt voor verbinding tussen client en server.
import RPi.GPIO as GPIO#Is voor verbinding de knopjes en lampjes.
import time
from threading import Thread#Twee while-loops tegelijkertijd te runnen.
import os

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
GPIO.output(11,False)#Geel
GPIO.setup(13,GPIO.OUT)
GPIO.output(13,False)#Rood
GPIO.setup(7,GPIO.OUT)
GPIO.output(7,False)#Groen
GPIO.setup(16,GPIO.IN)#Knop Links(Alarm uitzetten)
GPIO.setup(12,GPIO.IN)#Knop Rechts(Sensor)

sockConnectie = socket.socket()#maakt verbinding tussen server en client
sockConnectie.connect(('192.168.42.9', 12369))#Connecteert client met server
sockConnectie.sendall(b'Welkom bij het alarmsysteem')
time.sleep(3)
host = "192.168.42.9"

def knopjes():
    while True:
        Pingen = subprocess.call(["ping", "192.168.42.9", "-c1", "-W2", "-q"], stdout=open(os.devnull,'w'))
        if (GPIO.input(16)):
            if (GPIO.input(12)):

                GPIO.output(11,False)
                GPIO.output(13,False)
                GPIO.output(7,False)

            Geel = GPIO.output(11, False)
            Rood = GPIO.output(13, False)
            Groen = GPIO.output(7, True)

        if (GPIO.input(12)): #Als knop rechts is ingedrukt, gaat geel aan 
            print('Sensor is afgegaan')
            Geel = GPIO.output(11, True) #Geel gaat aan
            Rood = GPIO.output(13, False)
            Groen = GPIO.output(7, False)
            time.sleep(4)

            if (GPIO.input(16)): #Als knop links is ingedrukt, gaat groen aan
                print('Code ingevoerd om alarm uit te schakelen')
                Geel = GPIO.output(11, False)
                Groen = GPIO.output(7, True)#Groen gaat aan
            else:
                Geel = GPIO.output(11, False)
                Rood = GPIO.output(13, True) #Rood gaat aan als linker knop niet wordt ingedrukt 
                Groen = GPIO.output(7, False)
                sockConnectie.send(b'Alarm is afgegaan') #'Alarm is afgegaan' wordt naar server gestuurd 
                print('Alarm is afgegaan')
        if (Pingen != 0): # Ping met server 192.168.42.9
            print("Het alarmsysteem is niet meer connected met de server")
            GPIO.output(13, True) # Rood gaat aan, alarm is ingeschakeld client is niet meer verbonden met server
            GPIO.output(7, False)
            GPIO.output(11, False)

def aanEnUitAlarmsysteem():
    while True:
        info = sockConnectie.recv(1024)
        if info == b'aan': #Als cliënt 'aan' ontvangt van de server, dan gaat groene licht aan 
            GPIO.output(7, True) # Groen gaat aan 
            GPIO.output(13, False)

        if info == b'uit': #Als cliënt 'uit' ontvangt van de server, gaan alle lichten uit
            GPIO.output(7, False)
            GPIO.output(11, False)
            GPIO.output(13, False)

        if info == b'shutdown': # Als cliënt 'shutdown' van de server ontvangt wordt de connectie verbroken
            print('Client uitgeschakeld vanuit de server')
            sockConnectie.close()

threadKnop = Thread(target=knopjes)
threadAlarmsysteem = Thread(target=aanEnUitAlarmsysteem)
threadKnop.start()
threadAlarmsysteem.start()
threadKnop.join()
threadAlarmsysteem.join()

sockConnectie.close()

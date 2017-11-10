import subprocess
import socket
import time
from threading import Thread
import RPi.GPIO as GPIO
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

sockConnectie = socket.socket()#Maakt verbinding tussen server en client
sockConnectie.bind(('', 12369))#Verbind client tussen server en client


hostname = "192.168.42.8"
c, addr = sockConnectie.accept()
def userInterface():
    while True:

        sockConnectie.listen(1)#Wacht op connectie van de client
        c, addr = sockConnectie.accept()#Connectie maken met de client



        print(c.recv(1024)) #Hetgeen wat server ontvangt, aan/uit.
        test = input('aan of uit? ') 
        print(test)
        if test == 'aan':
            c.send(b'aan') #Server stuurt 'aan' naar cliënt om functie uit te voeren
        if test == 'uit':
            c.send(b'uit') #Server stuurt 'uit' naar cliënt om functie uit te voeren
        if test == 'shutdown':
            c.send(b'shutdown')# Server stuurt 'shutdown' naar client om connectie uit te schakelen
        print(c.recv(1024)) #Ontvangt als client niet meer vebonden is, door bijv. UTP weg te halen.
        test = input('aan of uit? ')
        print(test)
        if test == 'aan':
            c.send(b'aan')
        if test == 'uit':
            c.send(b'uit')
        if test == 'shutdown':
            c.send(b'shutdown')
        print(c.recv(1024))

def pingen():
    while True:
        Pingen = subprocess.call(['ping','192.168.42.8','-c1','-W2','-q'],stdout=open(os.devnull,'w'))
        if(Pingen != 0): #Ping met client 192.168.42.8
            print("Het alarmsysteem is niet meer connected met de server")

threadUserInterface = Thread(target=userInterface)
threadPing = Thread(target=pingen)
threadUserInterface.start()
threadPing.start()
threadUserInterface.join()
threadPing.join()



c.close()

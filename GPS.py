#!/usr/bin/python
# -*-coding:Latin-1 -*

# GPS.py v5.1
# pour relancer dans un screen
# su - pi -c "screen -dm -S raspi103 ~/GPS/start"

# importation pour le GPS
import os
import serial
import time
import subprocess
from decimal import *
from subprocess import call

from datetime import datetime
from os import path

# fix message d'erreur lié a pygame (placer avant "import pygame")
os.environ['SDL_AUDIODRIVER'] = 'dsp' 

# Affiche pygame sur le pitft
os.environ["SDL_FBDEV"] = "/dev/fb1"

# importation pour pygame
import pygame

# Serial Communication
port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=1)

# creation des couleurs
BLANC = (255,255,255)
NOIR = (0,0,0)
ROUGE = (255,0,0)
JAUNE = (255,255,0)
VERT = (0,255,0) 
BLEU = (0,0,255)
PURPLE = (255, 0, 255)

# pigame init + fond NOIR + font 1 et 2
pygame.init()
screen = pygame.display.set_mode((320, 240), pygame.FULLSCREEN) #Setting Full Screen
#screen = pygame.display.set_mode((320, 240))                   #Setting windows Screen
pygame.display.set_caption('Compteur RASPI 103 (build 2)')      # Window Name
pygame.mouse.set_visible(0)
screen.fill(NOIR) # backgroud color
# font et size
font_1 = pygame.font.Font(pygame.font.get_default_font(), 35)
font_2 = pygame.font.Font(pygame.font.get_default_font(), 200)


def statut_HAT():
    # chargement
    text_load = "CHARGEMENT"
    data_load = font_1.render(text_load, True, JAUNE)
    screen.blit(data_load, dest=(10,2))
    pygame.draw.rect(screen, ROUGE, (2,40,316,30), 4) #Barre de chargement
    pygame.display.flip()
    time.sleep(.5)

    # Donne le statut de la carte HAT + activation
    print "--- statut carte HAT ---"
    HAT = True
    while HAT:
        print "Carte HAT:  TEST"
        port.write(('AT'+'\r\n').encode('ascii'))
        rcv = port.read(650).decode('ascii')
        if 'OK' in rcv:
            print "Carte HAT:  OK"
            HAT = False
        else:
            print "Acivation ..."
            os.system("sudo python /home/pi/GPS/GSM_PWRKEY.py")
            time.sleep(1)
    # Chargemnt 1/4
    text_load1 = "Carte HAT :  OK"
    data_load1 = font_1.render(text_load1, True, JAUNE)
    screen.blit(data_load1, dest=(10,70))
    pygame.draw.rect(screen, ROUGE, (2,40,79,30), 0)
    pygame.display.flip()
    time.sleep(.1)

    # Donne le statut du GPS + activation
    print "--- statut GPS ---"
    PWR = True
    while PWR:
        print "GPS PWR:    TEST"
        port.write(('AT+CGNSPWR?'+'\r\n').encode('ascii'))
        rcv = port.read(650).decode('ascii')
        if rcv.find("+CGNSPWR: 1") > 0:
            print "GPS PWR:    OK"
            PWR = False
        if rcv.find("+CGNSPWR: 0") > 0:
            print "GPS PWR:    NOK"
            print "Acivation ..."
            port.write(('AT+CGNSPWR=1'+'\r\n').encode('ascii'))
            time.sleep(1)
    # Chargemnt 2/4
    text_load2 = "GPS PWR  :  OK"
    data_load2 = font_1.render(text_load2, True, JAUNE)
    screen.blit(data_load2, dest=(10,100))
    pygame.draw.rect(screen, ROUGE, (2,40,158,30), 0)
    pygame.display.flip()
    time.sleep(.1)

    while 1:
        print "GPS B/S:    TEST"
        port.write(('AT+CGNSIPR?'+'\r\n').encode('ascii'))
        rcv = port.read(650).decode('ascii')
        if rcv.find("+CGNSIPR: 115200") > 0:
            print "GPS B/S:    OK"
            break
        else:
            print "GPS B/S:    NOK"
            print "Modification a 115200 b/s ..."
            port.write(('AT+CGNSIPR=115200'+'\r\n').encode('ascii'))
            time.sleep(1)
    # Chargemnt 3/4
    text_load3 = "GPS B/S    :  OK"
    data_load3 = font_1.render(text_load3, True, JAUNE)
    screen.blit(data_load3, dest=(10,130))
    pygame.draw.rect(screen, ROUGE, (2,40,237,30), 0)
    pygame.display.flip()
    time.sleep(.1)
 
    while 1:
        print "GPS TST:    TEST"
        port.write(('AT+CGNSTST?'+'\r\n').encode('ascii'))
        rcv = port.read(650).decode('ascii')
        if rcv.find("+CGNSTST: 1") > 0:
            print "GPS TST:    OK"
            break
        if rcv.find("+CGNSTST: 0") > 0:
            print "GPS TST:    NOK"
            print "Acivation ..."
            port.write(('AT+CGNSTST=1'+'\r\n').encode('ascii'))
            time.sleep(1)
    # Chargemnt 4/4
    text_load4 = "GPS TST   :  OK"
    data_load4 = font_1.render(text_load4, True, JAUNE)
    screen.blit(data_load4, dest=(10,160))
    pygame.draw.rect(screen, ROUGE, (2,40,316,30), 0)
    pygame.display.flip()
    time.sleep(.1)

def draw():
    # actualisation de la fenetre
    pygame.draw.rect(screen, NOIR, (0,0,320,240), 0)

    # cadre
    pygame.draw.rect(screen, ROUGE, (2,2,316,42), 4) #Rect du haut 
    pygame.draw.rect(screen, ROUGE, (2,50,316,188), 4) #Rect du bas 

    # affiche icone satelite 
    sat_ico = pygame.image.load("sat.png")
    screen.blit(sat_ico, (10, 6))

    # affiche nombre de satelite
    text_sat = nb_sat
    data_sat = font_1.render(text_sat, True, JAUNE)
    screen.blit(data_sat, dest=(50,4))

    # affiche icone wifi
    try:
        output = subprocess.check_output(['sudo', 'iwgetid'])
        if output.split('"')[1] == "Livebox-6A0C":
            wifi_ico = pygame.image.load("wifi.png")
            screen.blit(wifi_ico, (90, 6))
    except Exception, e:
        print ""

    # affiche icone montre
    time_ico = pygame.image.load("time.png")
    screen.blit(time_ico, (140, 6))
    
    # affiche l heure
    text_time = heure
    data_time = font_1.render(text_time, True, JAUNE)
    screen.blit(data_time, dest=(180,4))

    # affiche la vitesse
    text_vit = vit
    # ------------------------------------------
    # NE FONCTIONNE PAS, a réparer dans la prochaine build
    if text_vit > 9:
        x_vit = (6,30)
    if text_vit < 10:
        x_vit = (60,30)
    # ------------------------------------------
    data_vit = font_2.render(text_vit, True, JAUNE)
    screen.blit(data_vit, dest=x_vit)

    # affiche km/h a droite de la vitesse
    text_kmh = "km/h"
    data_kmh = font_1.render(text_kmh, True, JAUNE)
    screen.blit(data_kmh, dest=(230,60))
    
    # affiche la vitesse max
    text_vitmax_t = "MAX"
    data_vitmax_t = font_1.render(text_vitmax_t, True, JAUNE)
    screen.blit(data_vitmax_t, dest=(230,90))
    
    text_vitmax = vit_max
    data_vitmax = font_1.render(text_vitmax, True, JAUNE)
    screen.blit(data_vitmax, dest=(250,120))


port.reset_input_buffer()
statut_HAT()
continuer = True
nb_sat = "#"
vit = "0"
vit_max = "0"
date = "00/00/00"
heure_UTC = "00:00:00"
s1 = "#"
s2 = "#"

# Creation du fichier .csv
dt = datetime.now()
dt_split = dt.strftime('-%Y-%m-%d-%H-%M-%S')
dt_path = path.splitext('/home/pi/GPS/DATA/gps_data.csv')
dt_csv = dt_path[0] + dt_split + dt_path[1]

#Condition de creation du .csv
with open(dt_csv, 'w') as h:
    h.write("Heure,Latitude,Longitude,Vitesse km/h")

try:
    while continuer:
        fd = port.read(650).decode('ascii')  
        heure = time.strftime('%X',time.localtime())        
        if port.inWaiting() > 0:
            if '$GNGGA' in fd:
                ps_GGA=fd.find('$GNGGA')
                data_GAA=fd[ps_GGA:(ps_GGA+66)]
                sdata_GAA = data_GAA.split(",")
                #print "data_GAA     ", data_GAA
                # satelite en vue
                try: 
                    nb_sat = sdata_GAA[7]
                except (IndexError, ValueError):
                    nb_sat = "#"

            if '$GNRMC' in fd:
                ps_RMC=fd.find('$GNRMC')
                data_RMC=fd[ps_RMC:(ps_RMC+66)]
                sdata_RMC = data_RMC.split(",")
                #print "data_RMC     ", data_RMC
                # vitesse
                try:
                    vit = sdata_RMC[7];                  # la vitesse (en noeud marin)
                    vit = str(int(float(vit)*1.609))     #convertion  de mph to kph
                    if vit > vit_max:
                        vit_max = vit
                except (IndexError, ValueError):
                    vit = "#"

                # date GPS
                try:
                    date = sdata_RMC[9][0:2] + "/" + sdata_RMC[9][2:4] + "/" + sdata_RMC[9][4:6]
                except IndexError:
                    date = "ERROR"
                
                # heure UTC
                try:
                    heure_UTC = sdata_RMC[1][0:2] + ":" + sdata_RMC[1][2:4] + ":" + sdata_RMC[1][4:6]
                except IndexError:
                    heure_UTC = "ERROR"

                try:
                    lat=sdata_RMC[3]       # la latitude
                    lon=sdata_RMC[5]       # la longitude
  
                    s1=lat[2:len(lat)]
                    s1=Decimal(s1)
                    s1=s1/60
                    s11=int(lat[0:2])
                    s1 = s11+s1        # latitude convertie
                    s1 = float(s1)
 
                    s2=lon[3:len(lon)]
                    s2=Decimal(s2)
                    s2=s2/60
                    s22=int(lon[0:3])
                    s2 = s22+s2        # longitude convertie
                    s2 = float(s2)

                    s1_dir = sdata_RMC[4]  # direction pour la latitude
                    s2_dir = sdata_RMC[6]  # direction pour la longitude
                except (IndexError, InvalidOperation):
                    s1 = "ERROR"
                    s2 = "ERROR"

                #ecriture dans le .cvs
                if s1 != "ERROR":
                    h = open(dt_csv, 'a')
                    h.write("\n%s,%s,%s,%s" % (heure, s1 ,s2 ,vit))

                #ecriture dans le .url
                p = open("/home/pi/GPS/DATA/gps_data.url", 'w+')
                p.write(
                    "[{000214A0-0000-0000-C000-000000000046}] \n"
                    "Prop3=19,2 \n"
                    "[InternetShortcut] \n"
                    "URL=http://maps.google.fr/maps?f=q&hl=fr&q=%s,%s \n" % (s1, s2))


        draw()
        os.system('clear')
        print "Nb Satelite  ", nb_sat
        print "Date GPS     ", date
        print "Heure UTC    ", heure_UTC
        print "Heure Paris  ", heure
        print "Vitesse km/h ", vit
        print "Vitesse Max  ", vit_max
        print "Latitude     ", s1
        print "Longitude    ", s2
        print ""
        print "#########-data-#########"
        print (fd)
        print "########################"

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                continuer = False
                port.close
        pygame.display.flip()
    pygame.quit()

except (KeyboardInterrupt, SystemExit):
    print "ctrl-c ..."
    port.close
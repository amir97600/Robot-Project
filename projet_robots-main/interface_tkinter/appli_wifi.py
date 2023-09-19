# -*- coding: utf-8 -*-
"""
Created on Fri May  5 10:27:33 2023

@author: raphael tranchot
"""
import threading
import keyboard
import cv2
import tkinter as tk
import serial
from PIL import Image,ImageTk

import time
import wifi 
import subprocess
import socket
import paho.mqtt.client as mqtt

'''
sock = socket.create_connection(('localhost', 80), timeout=10)

'''






    
#______________________CONTROLLER__________________________
class Controller:
    
    
    def __init__(self,portA):
        self.pressed = {}
        self.prevPressed = {}
        self._initPresses()
        self._create_ui()
        self.ser = serial.Serial(
            port= portA, # penser a changer le nom du port selon l'utilisateur 
            baudrate=115200,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS
        )
        self.ser.isOpen()
        

    def _initPresses(self):
        #initialise la position des touches en faux pour que le robot reste immobile 
        self.pressed["z"] = False # avant 
        self.pressed["q"] = False # gauche 
        self.pressed["s"] = False #arriere 
        self.pressed["d"] = False #droite 
        self.prevPressed["z"] = False
        self.prevPressed["q"] = False
        self.prevPressed["s"] = False
        self.prevPressed["d"] = False
        

    def start(self):
        self._check_key_press()
        self.root.mainloop()

    def _check_for_press(self, key, command):
        if self._is_pressed(key):
            self.prevPressed[key] = True
            self.ser.write(command)
            print(key + " pressed")

    def _check_for_release(self, key, command):
        if self._is_released(key):
            self.prevPressed[key] = False
            self.ser.write(command)
            print(key + " released")


    def _check_key_press(self):
        self._check_for_press("z", b"\x01")
        self._check_for_release("z", b"\x02")
        self._check_for_press("s", b"\x03")
        self._check_for_release("s", b"\x04")
        self._check_for_press("d", b"\x05")
        self._check_for_release("d", b"\x06")
        self._check_for_press("q", b"\x07")
        self._check_for_release("q", b"\x08")

        self.root.after(10, self._check_key_press)

        if keyboard.is_pressed('y'):  # si la touche 'r' est pressée
            print("y est presse : \n choregraphie enclenché")
            run_for_chore(choreography)
        

    def _is_pressed(self, key):
        return self.pressed[key] and self.prevPressed[key] == False


    def _is_released(self, key):
        return self.pressed[key] == False and self.prevPressed[key]

    

    def _set_bindings(self):
        for char in ["z","s","d", "q"]:
            self.root.bind("<KeyPress-%s>" % char, self._pressed)
            self.root.bind("<KeyRelease-%s>" % char, self._released)
            self.pressed[char] = False

    def _pressed(self, event):
        self.pressed[event.char] = True

    def _released(self, event):
        self.pressed[event.char] = False
    
    
    def _create_ui(self):
        
        self.root = _set_windows()
        #self.root.geometry('400x300')
        self._set_bindings()

#______________________CHOREGRAPHIE__________________________

choreography = [('z', 1),('q', 2),('s', 1),('d', 2)]

def run_choreography(choreography):
    '''
    Execute une chorégraphie, qui est une liste de tuples (t, note) où t est le temps en secondes
    à partir du début de la chorégraphie et note est une chaîne de caractères représentant une note
    à jouer sur le clavier.
    '''
    start_time = time.monotonic()
    
    for char,t in choreography:
        
        #time.sleep(0.1)
        keyboard.press(char)
        time.sleep(t)
        keyboard.release(char)
        time.sleep(5)
        print("condition for validé")
    print("fin de la choregraphie")

def chore2():
        text = "szqd"
        duration_down = 2  # duration to hold key down in seconds
        duration_up = 1  # duration to wait before releasing key in seconds

        for char in text:
            
            keyboard.press(char)
            print(char)
            time.sleep(duration_down)
            keyboard.release(char)
            time.sleep(duration_up) 

def pressz():  
    
    for char in "zqsd":
        keyboard.press(char)
        time.sleep(2)
        keyboard.release(char)
        
    
def execute_command():
    # Mettez ici votre commande à exécuter
    keyboard.press('s')
    pass

def run_command(char,t):
    keyboard.press(char)
    time.sleep(t)
    keyboard.release(char)
    #time.sleep(3)

def run_for_chore(choreography):
    # Créer un thread pour exécuter la commande
    step=0
    for char, t in choreography: 
        command_thread = threading.Thread(target=run_command, args=(char,t))
        command_thread.start()

        # Attendre la fin de la commande avant de passer à la suivante
        command_thread.join()

        # Attendre pendant la durée spécifiée
        threading.Timer(t, run_command, args=(char,t)).start()
        step+=1
        
        print ("step %d executé" %step, char)
    print("fin de la choregraphie")


def run_for_duration(duration):
    # Créer un thread pour exécuter la commande
    command_thread = threading.Thread(target=execute_command)
    command_thread.start()

    # Attendre pendant la durée spécifiée
    threading.Timer(duration, command_thread.stop).start()

#____________________________ INTERFACE _________________________________
def _set_windows():
    #create windows 
    window = tk.Tk()
    # set window title
    window.title("Controller arduino leonardo bot ")
    # set window width and height
    window.configure(width=500, height=200)
    # set window background color
    window.configure(bg='lightgray')
    #LabelFrame
    
    stopBtn = tk.Button(window, text="Stop", fg='blue', command= window.destroy)
    stopBtn.place(x=150, y=100)
          
      
    def f_Start():
        newWindow = tk.Toplevel()
        # set window title
        newWindow.title("Camera ")
        # set window width and height
        newWindow.configure(width=1000, height=600)
        # set window background color
        newWindow.configure(bg='lightgray')
        
        F1 = tk.LabelFrame(newWindow,bg='red')
        F1.pack()
        l1 = tk.Label(F1,bg="red")
        l1.pack()
        cap = cv2.VideoCapture(0) # 0 webcam, 1 camera
        
        F2 = tk.LabelFrame(newWindow,bg='blue')
        F2.pack()
        l2 = tk.Label(F2,bg="blue")
        l2.pack()
        
        while True:
            img = cap.read()[1]
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(img))
            l1['image'] = img
            newWindow.update()
        
        #newWindow.mainloop()
    
    
    startLbl=tk.Label(window, text="Pressez start pour retour image", fg='red', font=("Helvetica", 16))
    startLbl.place(x=60, y=50)
    
    startBtn = tk.Button(window, text="Start", fg='blue', command= f_Start)
    startBtn.place(x=80, y=100)
    
    chorBtn = tk.Button(window, text="chorée", fg='blue', command=keyboard.press('y'))
    chorBtn.place(x=120, y=150)
    
    '''
    # Configuration des événements clavier
    window.bind("z", move_forward)
    window.bind("s", move_backward)
    window.bind("q", move_left)
    window.bind("d", move_right)
    window.bind("<KeyRelease>", lambda event: send_command("stop"))
    '''
    
    

   
    # move window center
    winWidth = window.winfo_reqwidth()
    winwHeight = window.winfo_reqheight()
    posRight = int(window.winfo_screenwidth() / 2 - winWidth / 2)
    posDown = int(window.winfo_screenheight() / 2 - winwHeight / 2)
    window.geometry("+{}+{}".format(posRight, posDown))
    
    '''
    # Connexion au broker MQTT
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT)
    '''
    

    
    return window


#__________________ CONNECTION WIFI (Spécifique windows) _________________________

def wifi_scanner():
    output = subprocess.check_output(["netsh", "wlan", "show", "network", "mode=Bssid"])
    output = output.decode("iso-8859-1")  
    networks = output.replace("\r","").split("\n")
    networks = networks[4:]
    networks = [x for x in networks if x]
    wifi_networks = []
    for index, network in enumerate(networks):
        if index % 5 == 0:
            wifi_networks.append(network)
    print("Available Wi-Fi Networks:")
    print("========================")
    print("\n".join(wifi_networks))
    
    
wifi_scanner()


def get_ip_address():
    # Récupère le nom de l'interface WiFi
    interface_name = "yourAP"

    # Obtient l'adresse IP de l'interface WiFi
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]

    return ip_address



def connection_wifi():
    ssid = "yourAP"
    #password = "yourPassword"
    interface = get_ip_address()
    # Commande pour établir la connexion Wi-Fi
    connect_cmd = f'netsh wlan connect name="{ssid}" ssid="{ssid}" interface="{interface}"'
    
    # Connexion au réseau Wi-Fi de l'objet à l'aide de la commande netsh
    subprocess.call(connect_cmd, shell=True)
    
    # Vérification de la connexion en imprimant l'adresse IP
    print(f"Adresse IP attribuée: {print(interface)}")


'''
# Configuration MQTT
MQTT_BROKER = "192.168.4.2"  # Adresse IP de l'ESP32
MQTT_PORT = 3444
MQTT_TOPIC = "robot/commands"

# Fonction pour envoyer des commandes MQTT
def send_command(command):
    client.publish(MQTT_TOPIC, command)


# Fonction pour envoyer une commande à l'ESP32 via MQTT
def send_command(command):
    mqtt_client.publish("robot/command", command)

#mouvement directionnel 
def move_forward(event):
    send_command("forward")

def move_backward(event):
    send_command("backward")

def move_left(event):
    send_command("left")

def move_right(event):
    send_command("right")


'''






    
#__________________ MAIN _______________________________________


portA='COM9'
p = Controller(portA)
p.start()



# -*- coding: utf-8 -*-
"""
Created on Mon May 15 15:37:02 2023

@author: raphael tranchot
"""

import time 
import keyboard
import cv2
import tkinter as tk
import serial
import bluetooth
from PIL import Image,ImageTk

#______________________CONTROLLER__________________________
class Controller:
    
    
    def __init__(self,portA):
        self.pressed = {}
        self.prevPressed = {}
        self._initPresses()
        self._create_ui()
        baud_rate = 9600  # Adapté à votre configuration
        try: 
            self.ser = serial.Serial(
                port= portA, # penser a changer le nom du port selon l'utilisateur 
                baudrate=9600) #,
                #parity=serial.PARITY_ODD,
                #stopbits=serial.STOPBITS_TWO,
                #bytesize=serial.SEVENBITS
            
            print("connexion réussie")
        except: 
            print("connexion ratée")

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
            
            if isinstance(command, bytes):
                self.ser.write(command)
            else:
                print("encode")
                self.ser.write(command.encode())
            
            print(key + " pressed")

                
    def _check_for_release(self, key, command):
        if self._is_released(key):
            self.prevPressed[key] = False
            
            if isinstance(command, bytes):
                self.ser.write(command)
            else:
                self.ser.write(command.encode())
            
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
            #run_for_chore(choreography)
       

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
    
    # move window center
    winWidth = window.winfo_reqwidth()
    winwHeight = window.winfo_reqheight()
    posRight = int(window.winfo_screenwidth() / 2 - winWidth / 2)
    posDown = int(window.winfo_screenheight() / 2 - winwHeight / 2)
    window.geometry("+{}+{}".format(posRight, posDown))
    
    
    return window


#__________ BLUETOOTH SCANNER __________________

import bluetooth as bt
def bluetooth_scanner():
    print("Looking for nearby devices...")
    nearby_devices = bluetooth.discover_devices(lookup_names=True, flush_cache=True, duration=20)
    print("Found %d devices." % len(nearby_devices))

    for addr, name in nearby_devices:
        print(" %s - %s" % (addr, name))


bluetooth_scanner()



 #remplacer portA et macAdress dans le controller en fonction du mode fil ou bluetooth 
portA='COM6'
p = Controller(portA)
p.start()
'''
sock.close()
port.close()
'''
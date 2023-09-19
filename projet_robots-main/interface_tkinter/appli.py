
import tkinter as tk
import serial
import sys


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



def _set_windows():
    #create windows 
    window = tk.Tk()
    # set window title
    window.title("Controller arduino leonardo bot ")
    # set window width and height
    window.configure(width=1000, height=600)
    # set window background color
    window.configure(bg='lightgray')
    
    
    #set option window 
    #startBtn = tk.Button(window, text="Start", fg='blue', command= "x")
    #startBtn.place(x=80, y=100)
    
    stopBtn = tk.Button(window, text="Stop", fg='blue', command= window.destroy)
    stopBtn.place(x=150, y=100)
    
    startLbl=tk.Label(window, text="Commencer a controler le robot", fg='red', font=("Helvetica", 16))
    startLbl.place(x=60, y=50)
    
    
    # move window center
    winWidth = window.winfo_reqwidth()
    winwHeight = window.winfo_reqheight()
    posRight = int(window.winfo_screenwidth() / 2 - winWidth / 2)
    posDown = int(window.winfo_screenheight() / 2 - winwHeight / 2)
    window.geometry("+{}+{}".format(posRight, posDown))
    
    
    return window
        
 
    
    


portA='COM3'
p = Controller(portA)
p.start()


    


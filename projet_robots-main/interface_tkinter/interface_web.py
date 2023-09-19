import cv2
import tkinter as tk
import serial

import webbrowser
from PIL import Image,ImageTk

import time 
from selenium import webdriver
from selenium.webdriver.common.by import By
def _set_windows():

    window = tk.Tk()
    window.title("Controller Arduino Leonardo Bot")
    window.configure(width=500, height=200)
    window.configure(bg='lightgray')
    
    stopBtn = tk.Button(window, text="S", fg='blue', command=window.destroy)
    stopBtn.place(x=320, y=100)

    def f_Start(): #modifier la fonction pour ajouter les fonctions liés au marqueurs aruco
        newWindow = tk.Toplevel()
        newWindow.title("Camera")
        newWindow.configure(width=1000, height=600)
        newWindow.configure(bg='lightgray')

        F1 = tk.LabelFrame(newWindow, bg='red')
        F1.pack()
        l1 = tk.Label(F1, bg="red")
        l1.pack()
        cap = cv2.VideoCapture(0)

        F2 = tk.LabelFrame(newWindow, bg='blue')
        F2.pack()
        l2 = tk.Label(F2, bg="blue")
        l2.pack()

        while True:
            img = cap.read()[1]
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(img))
            l1['image'] = img
            newWindow.update()

    lien = "http://192.168.4.1/" #remplacer par lien de l'ESP32 
    def browserop():
        webbrowser.open(lien)

        
    startLbl = tk.Label(window, text="D = mode drive \n C = mode chorée \n S = Stop \n F = acquisition caméra", fg='red', font=("Helvetica", 16))
    startLbl.place(x=0, y=0)

    startBtn = tk.Button(window, text="F", fg='blue', command=f_Start)
    startBtn.place(x=80, y=100)

    ctrlBtn = tk.Button(window, text="D", fg='blue', command=browserop)
    ctrlBtn.place(x=160, y=100)

    chorBtn = tk.Button(window, text="C", fg='blue', command=_choree)
    chorBtn.place(x=240, y=100)

    winWidth = window.winfo_reqwidth()
    winwHeight = window.winfo_reqheight()
    posRight = int(window.winfo_screenwidth() / 2 - winWidth / 2)
    posDown = int(window.winfo_screenheight() / 2 - winwHeight / 2)
    window.geometry("+{}+{}".format(posRight, posDown))

    window.mainloop()

    return window



def _choree():
    # Initialiser le navigateur
    
    danse= [("A", 5), ("D", 5), ("A", 2), ("R", 1)]

    driver = webdriver.Firefox()
    driver.get("http://192.168.4.1/")
    #driver.find_element_by_id("nav-search").send_keys("Selenium")

    # Attendre 2 secondes
    time.sleep(2)

    forward = driver.find_element(By.LINK_TEXT, "AVANCER")
    backward = driver.find_element(By.LINK_TEXT, "RECULER")
    right = driver.find_element(By.LINK_TEXT, "DROITE")
    left = driver.find_element(By.LINK_TEXT, "GAUCHE")
    stop = driver.find_element(By.LINK_TEXT, "STOP")
    # Trouver et cliquer sur le deuxième bouton
    for bouton, delai in danse:
        if bouton=="A":
            #forward.click()
            driver.get("http://192.168.4.1/A")
            time.sleep(delai)
        elif bouton=="R":
            #backward.click()
            driver.get("http://192.168.4.1/R")
            time.sleep(delai)
        elif bouton=="D":
            #right.click()
            driver.get("http://192.168.4.1/D")
            time.sleep(delai)
        elif bouton=="G":
            #left.click()
            driver.get("http://192.168.4.1/G")
            time.sleep(delai)
    #stop.click() # ON STOPPE LE ROBOT PDT 1 SEC APRES CHAQUE INSTRUCTION 
    driver.get("http://192.168.4.1/S")
    time.sleep(1)

    # Fermer le navigateur
    driver.quit()
    

_set_windows()
    

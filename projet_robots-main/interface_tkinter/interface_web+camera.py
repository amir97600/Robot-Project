import cv2
import tkinter as tk
import serial
import cv2.aruco as aruco
import numpy as np

import webbrowser
from PIL import Image,ImageTk

import time 
from selenium import webdriver
from selenium.webdriver.common.by import By

# ID des marqueurs ArUco à suivre
marker_id1 = 0
marker_id2 = 1
camera_matrix = np.array([[1.0589396883450509e+03, 0., 9.8093408357478017e+02],
                         [ 0.,
       1.0600746647943295e+03, 5.5303806715260475e+02],
                         [0., 0., 1.]])
distortion_coefficients = np.array([[9.8419703498486173e-03, 4.3314045679447709e-02,
       1.1842155805489934e-03, -7.5153040970705207e-04,
       -4.0209432045899024e-02]])

# Dictionnaire des marqueurs ArUco
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)

# Paramètres du détecteur ArUco
parameters = aruco.DetectorParameters_create()


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
        cap.set(3, 1280) # longeur 
        cap.set(4, 720) #largeur 

        F2 = tk.LabelFrame(newWindow, bg='blue')
        F2.pack()
        l2 = tk.Label(F2, bg="blue")
        l2.pack()

        # Boucle principale
        while True:
    	# Lecture de la frame suivante
            ret, frame = cap.read()
            
            if ret:
        	# Conversion de la frame en niveaux de gris
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        	# Détection des marqueurs ArUco
                corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        	# Vérification si les marqueurs spécifiques sont présents
                if marker_id1 in ids and marker_id2 in ids:
            	# Indices des marqueurs spécifiques dans la liste des IDs
                    marker_index1 = np.where(ids == marker_id1)[0][0]
                    marker_index2 = np.where(ids == marker_id2)[0][0]

            	# Coins des marqueurs spécifiques
                    marker_corners1 = corners[marker_index1][0]
                    marker_corners2 = corners[marker_index2][0]

            	# Calcul du vecteur de translation entre les marqueurs
                    tvec = marker_corners2.mean(axis=0) - marker_corners1.mean(axis=0)

            	# Calcul de la rotation entre les marqueurs
                    _, rvec, _ = aruco.estimatePoseSingleMarkers([marker_corners1, marker_corners2], 1, camera_matrix, distortion_coefficients)

            	# Affichage des résultats
                    print("Vecteur de translation :", tvec)
                    print("Vecteur de rotation :", rvec)

        	# Affichage des marqueurs détectés sur la frame
                frame = aruco.drawDetectedMarkers(frame, corners, ids)

        	# Affichage de la frame
                cv2.imshow('Video', frame)

    	# Arrêt du programme si la touche 'q' est pressée
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        cap.release()
        cv2.destroyAllWindows()

    lien = "http://192.168.4.2/" #remplacer par lien de l'ESP32 
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
    

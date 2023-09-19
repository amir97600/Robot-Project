import cv2
import tkinter as tk
from PIL import Image,ImageTk
import numpy as np

'''cap = cv2.VideoCapture(2,cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
writer = cv2.VideoWriter("recording.mp4",fourcc,30.0,(1280,720))
recording = False

while True:
	ret,frame = cap.read()

	if ret:
		cv2.imshow("video",frame)
		if recording:
			writer.write(frame)
	key = cv2.waitKey(1)
	if key == ord('q'):
		break
	elif key == ord('r'):
		recording = not recording
		print (f"Recording: {recording}") '''



def _set_windows(n):
    #create windows 
    window = tk.Tk()
    # set window title
    window.title("Controller arduino leonardo bot ")
    # set window width and height
    window.configure(width=1000, height=600)
    # set window background color
    window.configure(bg='lightgray')
    
    
    #LabelFrame
    F1 = tk.LabelFrame(window,bg='red')
    F1.pack()
    l1 = tk.Label(F1,bg="red")
    l1.pack()
    cap = cv2.VideoCapture(n)
    
    F2 = tk.LabelFrame(window,bg='blue')
    F2.pack()
    l2 = tk.Label(F2,bg="blue")
    l2.pack()
    stopBtn = tk.Button(l2, text="Stop", fg='blue', command= window.destroy)
    stopBtn.pack()
    
    
    startLbl=tk.Label(l2, text="Commencer a controler le robot", fg='red', font=("Helvetica", 16))
    startLbl.pack()
    
    while True:
    	img = cap.read()[1]
    	img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    	img = ImageTk.PhotoImage(Image.fromarray(img))
    	l1['image'] = img
    	window.update()
    
    
    
    
    
    
    # move window center
    winWidth = window.winfo_reqwidth()
    winwHeight = window.winfo_reqheight()
    posRight = int(window.winfo_screenwidth() / 2 - winWidth / 2)
    posDown = int(window.winfo_screenheight() / 2 - winwHeight / 2)
    window.geometry("+{}+{}".format(posRight, posDown))
    
    
    return window
        
 
    
    

#a = _set_windows(2)
b = _set_windows(0)
b.mainloop()
#a.mainloop()




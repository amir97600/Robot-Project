from flask import Flask,render_template, request
import webbrowser


app = Flask(__name__)

lien = "http://127.0.0.1:5000" #remplacer par lien de l'ESP32 
def browserop():
    webbrowser.open(lien)




@app.route('/')
def index():
   return render_template('index.html')

if __name__ == "__main__":
    browserop()
    app.run()
    

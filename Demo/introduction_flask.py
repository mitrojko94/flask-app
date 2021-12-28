import re
from flask import Flask

app = Flask(__name__)  #Instanciram klasu

@app.route("/")  #Moze da se napise i drugacije, ispod f-je....app.add_url_rule("/", view_func="ime klase")
def home():
    return "Darko Mitrovic"

@app.route("/about")
def about():
    return "About page"
    
if __name__=="__main__":
    app.run(debug=True)


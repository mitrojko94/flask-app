from flask import Flask, render_template

app = Flask(__name__)

def home():
    return render_template("home.html")

def about():
    return render_template("about.html")

app.add_url_rule("/", view_func=home)
app.add_url_rule("/about", view_func=about)

app.run(debug=True)
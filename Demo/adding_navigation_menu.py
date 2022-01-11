from flask import Flask, render_template
from datetime import datetime
from bokeh.plotting import figure
from pandas_datareader import data
from bokeh.embed import components  
from bokeh.resources import CDN

app = Flask(__name__)

@app.route("/plot")
def plot():

    start = datetime(2021, 1, 1)
    end = datetime(2021, 1, 11)
    df = data.DataReader(name="BABA", data_source="yahoo", start=start, end=end)

    def inc_dec(c, o):
        if c > o:
            value = "Increase"
        elif c < o:
            value = "Decrease"
        else:
            value = "Equal"
        return value

    df["Status"] = [inc_dec(c, o) for c, o in zip(df.Close, df.Open)]
    df["Middle"] = abs(df.Open + df.Close)/2
    df["Height"] = abs(df.Close - df.Open)

    f = figure(x_axis_type="datetime", width=1000, height=300, sizing_mode="scale_width")  
    f.title.text="Candlestick Chart"
    f.grid.grid_line_alpha=0.3  

    hours_12 = 12*60*60*1000  

    f.segment(df.index, df.High, df.index, df.Low, color="Black")

    f.rect(x=df.index[df.Status=="Increase"], y=df.Middle[df.Status=="Increase"], width=hours_12, 
        height=df.Height[df.Status=="Increase"], fill_color="#CCFFFF", line_color="black")

    f.rect(x=df.index[df.Status=="Decrease"], y=df.Middle[df.Status=="Decrease"], width=hours_12, 
        height=df.Height[df.Status=="Decrease"], fill_color="#FF3333", line_color="black")

    #Pomocu components dobijam torku, koja ima JS i HTML kod
    components(f)  
    script1, div1 = components(f)  

    #Pomocu CDN dobijam linkove za JS i CSS
    cdn_js = CDN.js_files[0]  #Stavim [0], da bih imao string, prvi element liste, on mi i treba samo
    cdn_css = CDN.css_files
    
    return render_template("plot.html", script1=script1, div1=div1, cdn_js=cdn_js, cdn_css=cdn_css)

def home():
    return render_template("home.html")

def about():
    return render_template("about.html")

app.add_url_rule("/", view_func=home)
app.add_url_rule("/about", view_func=about)

app.run(debug=True)
from flask import Flask, render_template, request,redirect,flash
import requests
import json
import folium
import openrouteservice
from openrouteservice import convert
import folium
import json
import pandas as pd
from bokeh.models import HoverTool, LabelSet, ColumnDataSource
from bokeh.tile_providers import get_provider, STAMEN_TERRAIN
import numpy as np
import os
from geopy.geocoders import Nominatim
from folium import plugins
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
app = Flask(__name__)
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER
# May try using recurssion for another way of updating
fs = plugins.Fullscreen()
this_map = folium.Map(location=[19.48454, 72.543757],zoom_start=10, control_scale=True,tiles="cartodbpositron")

app.secret_key = "secret key"

# def popopHTMLString(point):
#     '''input: a series that contains a url somewhere in it and generate html'''
#     html = '<h2>Flight Details</h2> <br>Flight Number: ' + point.icao24 + '<br>'
#     html += 'CallSign: ' + point.callsign + '<br>'
#     html += ' Origin: ' + point.origin_country + '<br>'
#     html += f' Altitude: { point.geo_altitude } meters <br>'
#     html += f' Velocity: { point.velocity } m/s <br>'
#     html += f' Status: {point.status} <br>'
#     if point.status =='Grounded':
#             pass
#     else:
#             html += f' {point.status} Rate: { point.vertical_rate } m/s2 <br>'

# #         html+= f'<a href=https://www.google.com/search?q={point.callsign}>Check Status</a>>Check Status</a>'
# #         print(f'https://www.google.com/search?q={point.callsign}')
#     return html
ALLOWED_EXTENSIONS = set(['csv'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def getloct(place):
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(place)
    return getLoc

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/map', methods=["GET", "POST"])
def mapp():
    source = request.form.get("source")
    dest = request.form.get("dest")
#     if 'file' not in request.files:
#         flash('No file part')
#         return 
#     file = request.files['file']
#     if file.filename == '':
#         flash('No image selected for uploading')
#         return redirect(request.url)
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#     uploaded_file = request.files['file']
#     coords = request.form.get("csv")
#     data = pd.read_csv(coords)
    print("done")
    if source and dest:
        print(source,dest)
    
        loc = Nominatim(user_agent="GetLoc")
        souloc = loc.geocode(source)
        desloc = loc.geocode(dest)
    this_map = folium.Map(prefer_canvas=True)
    this_map = folium.Map(location=[souloc.latitude, souloc.longitude], zoom_start=12)
    this_map.add_child(fs)
#     print(souloc.address)
#     this_map = folium.Map(prefer_canvas=True,zoom_start=21)
#     folium.TileLayer('stamentoner').add_to(this_map)
#     folium.TileLayer('stamenwatercolor').add_to(this_map)
#     folium.TileLayer('cartodbpositron').add_to(this_map)
#     folium.TileLayer('openstreetmap').add_to(this_map)
#     # Adding the option to switch tiles
#     folium.LayerControl().add_to(this_map)
    def getdata(coord):
        arr=[]
    #     originlo=coord[0][0]
    #     originla=coord[0][1]
    #     destlo=coord[1][0]
    #     destla=coord[1][1]
        originlo=52.5
        originla=13.42
        destlo=52.13
        destla=13.56
        response = requests.get('https://router.hereapi.com/v8/routes?origin='+str(originlo)+','+str(originla)+'&transportMode=car&destination='+str(destlo)+','+str(destla)+'&return=polyline,summary&apiKey=-8aU_4FKHjYVbP7DtHv4hUGhqMPIk5ravey6Zeqaxtk')
        print('https://router.hereapi.com/v8/routes?origin='+str(originlo)+','+str(originla)+'&transportMode=car&destination='+str(destlo)+','+str(destla)+'&return=polyline,summary&apiKey=-8aU_4FKHjYVbP7DtHv4hUGhqMPIk5ravey6Zeqaxtk')
        json_data = json.loads(response.text)
        real_time=json_data['routes'][0]['sections'][0]['summary']['duration']
        real_dist=json_data['routes'][0]['sections'][0]['summary']['length']
        arr.append(real_time)
        arr.append(real_dist)
        return arr
    data = pd.read_csv('coord.csv')
    m = folium.Map(location=[19.48454, 72.543757],zoom_start=10, control_scale=True,tiles="cartodbpositron")
    source=data.iloc[0]
    dest=data.iloc[-1]
    data.drop([0], axis=0, inplace=True)
    data.drop(data.tail(1).index,
            inplace = True)
    data.iat[3,1]
    coords = (( 72.477108,19.075630),(77.221248,28.598863))
    # coords = ((72.864822,19.075939),(72.869617,19.113892))
    # coords=((data.iat[6,1],data.iat[6,0]),(data.iat[0,1],data.iat[0,0]))
    print(coords)
    distance_txt=duration_txt=0
    # print(source,data)
    def map(coords):
        client = openrouteservice.Client(key='5b3ce3597851110001cf6248756b471977894b1585774e6aefdaa7b7')

        res = client.directions(coords)
        geometry = client.directions(coords)['routes'][0]['geometry']
        #     print(res)
        decoded = convert.decode_polyline(geometry)
        #     print(decoded[1])
        dist=round(res['routes'][0]['summary']['distance']/1000,1)
        time=round(res['routes'][0]['summary']['duration']/60,1)
        distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>"+str(dist)+" Km </strong>" +"</h4></b>"
    #     exp=(distance_txt*8)/100
        duration_txt = "<h4> <b>Duration :&nbsp" + "<strong>"+str(time)+" Mins. </strong>" +"</h4></b>"
        arr=getdata(coord)
        print(arr)
        speed = "<h4> <b>Speed :&nbsp" + "<strong>"+str(round(dist/(time/60)))+" Km/hr </strong>" +"</h4></b>" 
        time = "<h4> <b>Time :&nbsp" + "<strong>"+str(round(arr[0]))+" Km/hr </strong>" +"</h4></b>"  
        dist = "<h4> <b>Distance :&nbsp" + "<strong>"+str(round(arr[1]))+" Km/hr </strong>" +"</h4></b>"  

        folium.GeoJson(decoded).add_child(folium.Popup(distance_txt+duration_txt+speed+time+dist,max_width=300)).add_to(m)
        distance_txt+=distance_txt
        duration_txt+=duration_txt
        #     icon = folium.Icon(color="red", icon="fa-solid fa-truck-bolt",
        #                            prefix='fa',  icon_size=(24, 24))

        folium.Marker(
            location=list(coords[0][::-1]),
            popup="WayPoint",

            icon=folium.Icon(color="green"),
            ).add_to(this_map)
    #     for i in range(1,4):
    #             folium.Marker(
    #                 location=list((data.iat[i+1,0],data.iat[i+1,1])),
    #                 popup="Mid-Way",
    #                 icon=folium.Icon(color="blue"),
    #             ).add_to(m)
        #         print(location)
        folium.Marker(
                location=list(coords[1][::-1]),
            #     print
                popup="Destination",
                icon=folium.Icon(color="red"),
            ).add_to(this_map)
        return this_map
    # print(data.shape[0])
    for i in range(data.shape[0]-2):
        map(((data.iat[i+1,1],data.iat[i+1,0]),(data.iat[i+2,1],data.iat[i+2,0])))     
        this_map.save('map1.html')
    return this_map._repr_html_()

@app.route('/upload',methods=["GET,POST"])
def upload():
    if request.method == 'POST':

        # Create variable for uploaded file
        f = request.files['file']  
        data=pd.read_csv(f)
        #store the file contents as a string
        print("Hello")
        
        #create list of dictionaries keyed by header row
#         csv_dicts = [{k: v for k, v in row.items()} for row in csv.DictReader(fstring.splitlines(), skipinitialspace=True)]

        #do something list of dictionaries
#     return render_template("map1.html")
    
@app.route('/', methods=["GET", "POST"])
def suggest():
    sugg = request.form.get("suggest")
    f = open("suggestions.txt", "a")
    ct = datetime.datetime.now()
    print(sugg, ct)
    f.write(f"\n{ct}\n")
    f.write(f"{sugg}\n")
    f.close()
    return render_template('index.html', suggest='Thanks for your time !!')


if __name__ == '__main__':
    app.run()

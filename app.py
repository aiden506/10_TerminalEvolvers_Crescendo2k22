from flask import Flask, render_template, request,redirect
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
# May try using recurssion for another way of updating
fs = plugins.Fullscreen()
this_map = folium.Map(location=[19.48454, 72.543757],zoom_start=10, control_scale=True,tiles="cartodbpositron")


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

def getloct(place):
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(place)
    return getLoc

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/map', methods=["GET", "POST"])
def map():
    source = request.form.get("source")
    dest = request.form.get("dest")
    print(source,dest)
    this_map = folium.Map(prefer_canvas=True)
    loc = Nominatim(user_agent="GetLoc")
    souloc = loc.geocode(source)
    desloc = loc.geocode(dest)

    this_map = folium.Map(location=[souloc.latitude, souloc.longitude], zoom_start=12)
    this_map.add_child(fs)
    print(souloc.address)
#     this_map = folium.Map(prefer_canvas=True,zoom_start=21)
#     folium.TileLayer('stamentoner').add_to(this_map)
#     folium.TileLayer('stamenwatercolor').add_to(this_map)
#     folium.TileLayer('cartodbpositron').add_to(this_map)
#     folium.TileLayer('openstreetmap').add_to(this_map)
#     # Adding the option to switch tiles
#     folium.LayerControl().add_to(this_map)
    def map(coords):
        client = openrouteservice.Client(key='5b3ce3597851110001cf6248756b471977894b1585774e6aefdaa7b7')

        res = client.directions(coords)
        geometry = client.directions(coords)['routes'][0]['geometry']
#         print(res)
        decoded = convert.decode_polyline(geometry)
    #     print(decoded[1])
        distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['distance']/1000,1))+" Km </strong>" +"</h4></b>"
        duration_txt = "<h4> <b>Duration :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['duration']/60,1))+" Mins. </strong>" +"</h4></b>"
        folium.GeoJson(decoded).add_child(folium.Popup(distance_txt+duration_txt,max_width=300)).add_to(this_map)
        icon = folium.Icon(color="red", icon="fa-solid fa-truck-bolt",
                               prefix='fa',  icon_size=(24, 24))
        folium.Marker(
        location=list(coords[0][::-1]),
        popup="Source",
        icon=folium.Icon(color="green"),
        ).add_to(this_map)

        folium.Marker(
            location=list(coords[1][::-1]),
        #     print
            popup="Destination",
            icon=folium.Icon(color="red"),
        ).add_to(this_map)
        return this_map
    coords = (( souloc.longitude,souloc.latitude),(desloc.longitude,desloc.latitude))
    this_map=map(coords)
    # print('Hrllo')
    coord=((72.852851,19.220892),(72.849475,19.405541))
    this_map=map(coord)
    

#     def plotDot(point):
#         '''input: series that contains a numeric named latitude and a numeric named longitude
#         this function creates a CircleMarker and adds it to your this_map'''
#         htmlString = folium.Html(popopHTMLString(point), script=True)
#         icon = folium.Icon(color="red", icon="fa-fighter-jet",
#                            prefix='fa', icon_size=(24, 24))
# #         icon = folium.features.CustomIcon('plane.png',
# #                                               icon_size=(24, 24))
#         marker = folium.Marker([point.lat, point.long], icon=icon, popup=folium.Popup(
#             htmlString, min_width=300, max_width=300)).add_to(this_map)
    #     folium.CircleMarker(location=[point.lat, point.long],
    #                         radius=2,
    #                         weight=10).add_to(this_map)

 

    #use df.apply(,axis=1) to iterate through every row in your dataframe
    

    return this_map._repr_html_()


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

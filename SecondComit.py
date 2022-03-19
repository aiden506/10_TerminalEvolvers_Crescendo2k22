import openrouteservice
from openrouteservice import convert
import folium
import json

client = openrouteservice.Client(key='5b3ce3597851110001cf6248756b471977894b1585774e6aefdaa7b7')

coords = ((80.21787585263182,6.025423265401452),(80.23990263756545,6.018498276842677))
res = client.directions(coords)
geometry = client.directions(coords)['routes'][0]['geometry']
decoded = convert.decode_polyline(geometry)

distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['distance']/1000,1))+" Km </strong>" +"</h4></b>"
duration_txt = "<h4> <b>Duration :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['duration']/60,1))+" Mins. </strong>" +"</h4></b>"

m = folium.Map(location=[6.074834613830474, 80.25749815575348],zoom_start=10, control_scale=True,tiles="cartodbpositron")
folium.GeoJson(decoded).add_child(folium.Popup(distance_txt+duration_txt,max_width=300)).add_to(m)

folium.Marker(
    location=list(coords[0][::-1]),
    popup="Galle fort",
    icon=folium.Icon(color="green"),
).add_to(m)

folium.Marker(
    location=list(coords[1][::-1]),
    popup="Jungle beach",
    icon=folium.Icon(color="red"),
).add_to(m)


m.save('map1.html')
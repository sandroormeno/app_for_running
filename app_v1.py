import pandas as pd # library for data analsysis
#import json # library to handle JSON files
#from geopy.geocoders import Nominatim # convert an address into latitude and longitude values
#import requests # library to handle requests
#import numpy as np
import folium # map rendering library
import streamlit as st
from streamlit_folium import folium_static
from geopy.distance import geodesic
import branca
import branca.colormap as cm

data = pd.read_csv('https://raw.githubusercontent.com/sandroormeno/app_for_running/main/data/GPS-3-15-2023.CSV') # GPS.CSV

#add_select = st.sidebar.selectbox("Cuál data quieres ver?",("OpenStreetMap", "Stamen Terrain","Stamen Toner"))#for calling the function for getting center of maps
add_select = 'cartodbpositron' # 'stamentoner' OpenStreetMap cartodbdark_matter cartodbpositron stamenwatercolor cartodbdark_matter
#select_data = st.sidebar.radio("What data do you want to see?"("Total_Pop", "Area_Region","Male_Pop",'Female_Pop'))
dicts = {"Run down": [1,0],
         "Run Up": [0,1],
         "Both": [1,1] }
         
view_data = st.sidebar.radio("What data do you want to see?", ("Run down", "Run Up", "Both"))
ini = 130 #280
mid = 730 # 890
fin = 1410 # 1620
values = st.sidebar.slider(
    'Select a range of samples',
    0, len(data), (ini, fin))
    
#st.write('Values:', values)

#map_sby = folium.Map(tiles=add_select, location=[-12.1070348,-76.9468047], zoom_start=14)
map_sby = folium.Map(location=[-12.1070348,-76.9468047], zoom_start=14)

	
folium.TileLayer(add_select).add_to(map_sby)

st.title('Route on bikeway in La Molina') # 32 / 5.000

text = '''
Desde hace unos meses he comenzado a hacer algo de ejercicio, 
corriendo en la ciclovía de *Las Viñas* en el distrito de **La Molina**. 
Estoy usando un **GPS** (GPS-EM-406A) para recopilar datos de posición 
y lo estoy graficando en un mapa personalizado gracias a Folium. 
Si bien El dispositivo puede proporcionarnos la velocidad y la distancia recorrida, 
he decidido recalcularlos y mostrarlos a manera de datos acumulativos en cada marca graficada en el mapa. 
Además, indico la velocidad en cada tramo del recorrido. 
Espero hacer más análisis con los datos recopilados y con los que pueda generar.
'''
#st.markdown('Streamlit is **_really_ cool**.')
st.markdown(text)

def show_maps(view, samples):
    down = dicts[view][0]
    up = dicts[view][1]
    
    icon_url = 'https://raw.githubusercontent.com/sandroormeno/EnglishWeb/main/static/images/running1.png'
    icon_url_2 = 'https://raw.githubusercontent.com/sandroormeno/EnglishWeb/main/static/images/running2.png'
    
    lat_previo = 0
    long_previo = 0
    s = 0
    t = 0
    tim = 0
    color = cm.LinearColormap(['red','yellow', 'green'],
                            vmin=1, vmax=2.8,
                            index=[0, 2.0, 2.8])
    for i in range(samples[0],samples[1]):
      if (i % 10 == 0):
          if (i <= mid and down == 1):
            if (lat_previo != 0):
              origin = (lat_previo, long_previo)
              dist = (data.iloc[i]['Lat'], data.iloc[i]['Long'])
              s = s + float("{:.1f}".format(geodesic(origin, dist).meters))
              s = float("{:.1f}".format(s))
              speed = float("{:.1f}".format(geodesic(origin, dist).meters/30))
            else:
              s = 0
              speed = 0
            if (i != samples[0]):  
                t = t + 30
            else:
                t = 0
            if (t <= 60):
                tim = str(t) + " seg"
            else:
                tim = str(float("{:.1f}".format(t/60))) + " min"
            lat_previo = data.iloc[i]['Lat']
            long_previo = data.iloc[i]['Long']
            if(i == samples[0]):
                iframe = folium.IFrame("<img src='https://raw.githubusercontent.com/sandroormeno/EnglishWeb/main/static/images/ini.jpg'> <i><br>Hora: " + str(data.iloc[i]['Tiempo']) + " <br>Tiempo : " + str(tim) + " <br>Distacia: "+ str(s) + " mts<br>Speed: "+ str(speed)+" mts/seg</i>")
                iframe_ = branca.element.IFrame(html=iframe, width=340, height=210)
            elif(i == mid):
                iframe = folium.IFrame("<img src='https://raw.githubusercontent.com/sandroormeno/EnglishWeb/main/static/images/fin.jpg'> <i><br>Hora: " + str(data.iloc[i]['Tiempo']) + " <br>Tiempo : " + str(tim) + " <br>Distacia: "+ str(s) + " mts<br>Speed: "+ str(speed)+" mts/seg</i>")
                iframe_ = branca.element.IFrame(html=iframe, width=340, height=210)
            else:
                iframe = folium.IFrame("Hora: " + str(data.iloc[i]['Tiempo']) + " <br>Tiempo : " + str(tim) + " <br>Distacia: "+ str(s) + " mts<br>Speed: "+ str(speed)+" mts/seg mts<br>Altitude: "+ str(data.iloc[i]['Altitude'])  +" mts</i>")
                iframe_ = branca.element.IFrame(html=iframe, width=200, height=130)
            #popup = folium.Popup(iframe, min_width=180, max_width=250, height=500)
            
            popup = folium.Popup(iframe_,  max_width=210)
            
            index = "<i>Sample: " + str(i) + "</i>"
            

            folium.Marker([data.iloc[i]['Lat'], data.iloc[i]['Long']], 
                          icon = folium.features.CustomIcon(icon_url,icon_size=(30, 36)),  # Creating a custom Icon
                          popup=popup, 
                          tooltip=index,
                          ).add_to(map_sby)
                         
            #folium.Circle(location=[data.iloc[i]['Lat'],data.iloc[i]['Long']],radius=speed*4,color=color(speed), fill= True, fill_opacity=0.9, weight=0, popup=popup, tooltip=index).add_to(map_sby)
            origin = [data.iloc[i]['Lat'], data.iloc[i]['Long']]
            destino =[data.iloc[i-10]['Lat'], data.iloc[i-10]['Long']]
            speed_text = "<i>Speed: " + str(speed) + " mts/seg</i>"
            folium.PolyLine([origin,destino], color=color(speed), weight=speed*3, opacity=1, dash_array="5, 10", tooltip=speed_text).add_to(map_sby)
          elif(i > mid and up == 1):
            if (lat_previo != 0):
              origin = (lat_previo, long_previo)
              dist = (data.iloc[i]['Lat'], data.iloc[i]['Long'])
              s = s + float("{:.1f}".format(geodesic(origin, dist).meters))
              s = float("{:.1f}".format(s))
              speed = float("{:.1f}".format(geodesic(origin, dist).meters/30))
            else:
              s = 0
              speed = 0
              
            if (i != samples[0]):  
                t = t + 30
            else:
                t = 0
            if (t <= 60):
                tim = str(t) + " seg"
            else:
                tim = str(float("{:.1f}".format(t/60))) + " min"
                
            lat_previo = data.iloc[i]['Lat']
            long_previo = data.iloc[i]['Long']
            # https://raw.githubusercontent.com/sandroormeno/EnglishWeb/main/static/images/ini.jpg
            
            #iframe = folium.IFrame("<img src='https://raw.githubusercontent.com/sandroormeno/EnglishWeb/main/static/images/ini.jpg' width='100' height='100'> <i><br>Hora: " + str(data.iloc[i]['Tiempo']) + " <br>Tiempo : " + str(tim) + " <br>Distacia: "+ str(s) + " mts<br>Speed: "+ str(speed)+" mts/seg</i>")
            #popup = folium.Popup(iframe, min_width=180, max_width=250)
            if(i == mid):
                iframe = folium.IFrame("<img src='https://raw.githubusercontent.com/sandroormeno/EnglishWeb/main/static/images/fin.jpg'> <i><br>Hora: " + str(data.iloc[i]['Tiempo']) + " <br>Tiempo : " + str(tim) + " <br>Distacia: "+ str(s) + " mts<br>Speed: "+ str(speed)+" mts/seg<br>Altitude: "+ str(data.iloc[i]['Altitude'])  +" mts</i>")
                #iframe = folium.IFrame("Hora: " + str(data.iloc[i]['Tiempo']) + " <br>Tiempo : " + str(tim) + " <br>Distacia: "+ str(s) + " mts<br>Speed: "+ str(speed)+" mts/seg mts<br>Altitude: "+ str(data.iloc[i]['Altitude'])  +" mts</i>")
                iframe_ = branca.element.IFrame(html=iframe, width=340, height=210)
            else:
                #iframe = folium.IFrame("Hora: " + str(data.iloc[i]['Tiempo']) + " <br>Tiempo : " + str(tim) + " <br>Distacia: "+ str(s) + " mts<br>Speed: "+ str(speed)+" mts/seg</i>")
                iframe = folium.IFrame("Hora: " + str(data.iloc[i]['Tiempo']) + " <br>Tiempo : " + str(tim) + " <br>Distacia: "+ str(s) + " mts<br>Speed: "+ str(speed)+" mts/seg mts<br>Altitude: "+ str(data.iloc[i]['Altitude'])  +" mts</i>")
                iframe_ = branca.element.IFrame(html=iframe, width=200, height=130)
            popup = folium.Popup(iframe_,  max_width=210)
            index = "<i>Sample: " + str(i) + "</i>"
            folium.Marker([data.iloc[i]['Lat'], data.iloc[i]['Long']], 
                          popup=popup, 
                          tooltip=index,
                          icon = folium.features.CustomIcon(icon_url_2,icon_size=(30, 36)),
                          ).add_to(map_sby)
                          
            origin = [data.iloc[i]['Lat'], data.iloc[i]['Long']]
            destino =[data.iloc[i-10]['Lat'], data.iloc[i-10]['Long']]
            speed_text = "<i>Speed: " + str(speed) + " mts/seg</i>"
            folium.PolyLine([origin,destino], color=color(speed), weight=speed*3, opacity=1, dash_array="5, 10", tooltip=speed_text).add_to(map_sby)

    folium_static(map_sby)


show_maps(view_data, values)
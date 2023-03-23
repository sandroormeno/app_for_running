import pandas as pd # library for data analsysis
#import json # library to handle JSON files
#from geopy.geocoders import Nominatim # convert an address into latitude and longitude values
#import requests # library to handle requests
#import numpy as np
import folium # map rendering library
import streamlit as st
from folium.plugins import Draw
from streamlit_folium import folium_static
from geopy.distance import geodesic
import branca
import branca.colormap as cm
import numpy as np
import base64
from datetime import datetime
import time
#import matplotlib.pyplot as plt

#import vincent
#import json

data = pd.read_csv('https://raw.githubusercontent.com/sandroormeno/app_for_running/main/data/GPS-3-19-2023.CSV') # GPS.CSV

#add_select = st.sidebar.selectbox("Cuál data quieres ver?",("OpenStreetMap", "Stamen Terrain","Stamen Toner"))#for calling the function for getting center of maps
add_select = 'cartodbpositron' # 'stamentoner' OpenStreetMap cartodbdark_matter cartodbpositron stamenwatercolor cartodbdark_matter
#select_data = st.sidebar.radio("What data do you want to see?"("Total_Pop", "Area_Region","Male_Pop",'Female_Pop'))

dicts = {"Run down": [1,0],
         "Run Up": [0,1],
         "Both": [1,1] }
         
view_data = st.sidebar.radio("What data do you want to see?", ("Run down", "Run Up", "Both"))

_ = ''' estas son los datos para casa archivo.csv
csv                 ini         mid         fin
GPS-3-11-2023.CSV   280         890         1620
GPS-3-15-2023.CSV   130         730         1410
GPS-3-19-2023.CSV   150         970         1870
'''

ini = 150 #280
mid = 970 # 890
fin = 1860 # 1620
values = st.sidebar.slider(
    'Select a range of samples',
    0, len(data), (ini, fin))

 
#st.write('Values:', values)

#map_sby = folium.Map(tiles=add_select, location=[-12.1070348,-76.9468047], zoom_start=14)
map_sby = folium.Map(location=[-12.1070348,-76.9468047], zoom_start=13, tiles='cartodbpositron')

#folium.TileLayer(add_select).add_to(map_sby)

#-12.110329387600332, -76.93845036327191	


html = "{a resource that is heavy to load, such as an image}"
#lolo = popup=Popup("Mom & Pop Arrow Shop >>", parse_html=True)

#folium.Marker([-12.110329387600332, -76.93845036327191], popup=html, lazy=True).add_to(map_sby)
# https://levelup.gitconnected.com/creating-interactive-maps-with-python-folium-and-some-html-f8ac716966f

df = pd.read_csv('https://raw.githubusercontent.com/sandroormeno/app_for_running/main/OpenCamera/data_gps.csv')

#view_images = st.sidebar.radio("What data-view do you want to see?", ("View down", "View Up"))

#dicts_view = {"View down": [1,0],
#              "View Up": [0,1]}
mid_= 380
#range_img = st.sidebar.slider(
#    'Select a range to view images',
#    0, len(df), (12, 776))

#df = pd.read_csv('images/data_image.csv')
#st.dataframe(df, 200, 100)
#st.text(str(df.iloc[0]['file']))
#image = df.iloc[2]['file']
#image = 'https://raw.githubusercontent.com/sandroormeno/app_for_running/main/images/1.jpg'
#st.image(image, caption='Sunrise by the mountains')
#encoded = base64.b64encode(open('images/1.jpg', 'rb').read()).decode()
#html = '<img src="data:image/jpeg;base64,{}" width="400" height="400">'.format

#html = """
#    <h1> This is a big popup</h1><br>
#   With a few lines of code...
#    <p>
#    <code>
#        from numpy import *<br>
#        exp(-2*pi)
#    </code>
#    </p>
#    """
#

#st.text('https://raw.githubusercontent.com/sandroormeno/app_for_running/main'+str(df.iloc[0]['path']))

correr_group = folium.FeatureGroup(name="View path + images", show=True)
feature_group = folium.FeatureGroup(name="View images", show=False)
img_group = folium.FeatureGroup(name="View images better", show=False)
view_path = folium.FeatureGroup(name="View only path", show=False)

#down_ = dicts_view[view_images][0]
#up_ = dicts_view[view_images][1]

list_of_images = []
pos =[]
for i in range(len(df)):
   image =f"https://raw.githubusercontent.com/sandroormeno/app_for_running/main{df.iloc[i]['path']}"
   lat = df.iloc[i]['Lat']
   lon = df.iloc[i]['Long']
   pos.append((lat,lon))
   list_of_images.append(image)
#for i in range(len(df)):
#st.write('Cantidad de images:', len(list_of_images)) 
#st.write('Images:', list_of_images) 
#img_df = pd.DataFrame(list_of_images, columns=["Url"])
#st.dataframe(img_df)

# this is the better View
df_img = pd.read_csv('https://raw.githubusercontent.com/sandroormeno/app_for_running/main/OpenCamera/data_gps_image.csv')
___ = '''
for i in range(len(df_img)):
    
    if (i <= 82 and down_ == 1):
        image =f"https://raw.githubusercontent.com/sandroormeno/app_for_running/main{df_img.iloc[i]['path']}"
        #image =list_of_images[ini_imagen]
        html = f"<img src={str(image)} width='400' height='400'><br><i> &copy 2023 Sandro Ormeño</i>"
        iframe = branca.element.IFrame(html=html, width=400+20, height=400+60)
        popup = folium.Popup(iframe, max_width=2650)
        folium.Marker([df_img.iloc[i]['Lat'], df_img.iloc[i]['Long']], popup=popup).add_to(img_group)
    elif(i > 82 and up_ == 1):
        image =f"https://raw.githubusercontent.com/sandroormeno/app_for_running/main{df_img.iloc[i]['path']}"
        #image =list_of_images[ini_imagen]
        html = f"<img src={str(image)} width='400' height='400'><br><i> Time: &copy 2023 Sandro Ormeño</i>"
        iframe = branca.element.IFrame(html=html, width=400+20, height=400+60)
        popup = folium.Popup(iframe, max_width=2650)
        folium.Marker([df_img.iloc[i]['Lat'], df_img.iloc[i]['Long']], popup=popup).add_to(img_group)

#img_group.add_to(map_sby)
# end better View
'''

__ = '''

num = 0

for i in range(range_img[0],range_img[1]):
    #index_ = "<i>Sample: " + str(i) + "</i>"
    #if (i % 3 == 0):
    num = num+1
    if (i <= mid_ and down_ == 1):
        
    
        #image = df.iloc[i]['path'] # f"{to_lowercase(name)} is funny."
        image =f"https://raw.githubusercontent.com/sandroormeno/app_for_running/main{df.iloc[i]['path']}"
        #html = f"<img src={str(image)} width='400' height='400'><br><i> Lat: {str(df.iloc[i]['Lat'])}<br>Long: {str(df.iloc[i]['Long'])}</i>"
        date_now = str(df.iloc[i]['date_time'])
        time_now = date_now.split(" ")[-1]
        time_object = datetime.strptime(time_now, '%H:%M:%S').time()
        #time_object = time_object + pd.DateOffset(hours = 5)
        #final_time = time_object + pd.DateOffset(hours=5)

        html = f"<img src={str(image)} width='400' height='400'><br><i> Time: {time_object.hour} : {time_object.minute} : {time_object.second} </i>"
        #html = '<img src="data:image/jpeg;base64,{}" width="400" height="400">'.format
        #iframe = folium.IFrame(html(encoded), width=400+20, height=400+20)
        iframe = branca.element.IFrame(html=html, width=400+20, height=400+60)
        popup = folium.Popup(iframe, max_width=2650)
        
        folium.Marker([df.iloc[i]['Lat'], df.iloc[i]['Long']], popup=popup).add_to(feature_group)
    elif(i > mid_ and up_ == 1):
        image =f"https://raw.githubusercontent.com/sandroormeno/app_for_running/main{df.iloc[i]['path']}"
        #html = f"<img src={str(image)} width='400' height='400'><br><i> Lat: {str(df.iloc[i]['Lat'])}<br>Long: {str(df.iloc[i]['Long'])}</i>"
        date_now = str(df.iloc[i]['date_time'])
        time_now = date_now.split(" ")[-1]
        html = f"<img src={str(image)} width='400' height='400'><br><i> Date: {time_now}</i>"
        #html = '<img src="data:image/jpeg;base64,{}" width="400" height="400">'.format
        #iframe = folium.IFrame(html(encoded), width=400+20, height=400+20)
        iframe = branca.element.IFrame(html=html, width=400+20, height=400+60)
        popup = folium.Popup(iframe, max_width=2650)
        folium.Marker([df.iloc[i]['Lat'], df.iloc[i]['Long']], popup=popup).add_to(feature_group)
        
#st.write('Samples per images:',num)        
   
#feature_group.add_to(map_sby)
#folium.LayerControl().add_to(map_sby)
#folium.LayerControl().add_to(map_sby)
'''




st.title('Route on bikeway in La Molina') # 32 / 5.000
st.markdown("![Alt Text](https://raw.githubusercontent.com/sandroormeno/app_for_running/main/images/run.gif)")
#st.image('images/1.jpg', caption='Sunrise by the mountains')

text = '''
Desde hace unos meses he comenzado a hacer algo de ejercicio, 
corriendo en la ciclovía de *Las Viñas* en el distrito de **La Molina**. 
Estoy usando un **GPS** (GPS-EM-406A) para recopilar datos de posición 
y lo estoy graficando en un mapa personalizado gracias a Folium. 
Si bien El dispositivo puede proporcionarnos la velocidad y la distancia recorrida, 
he decidido recalcularlos y mostrarlos a manera de datos acumulativos en cada marca graficada en el mapa. 
Además, indico la velocidad en cada tramo del recorrido, el cual se puede visualizar en el apartado `View only path`.

'''
#st.markdown('Streamlit is **_really_ cool**.')
st.markdown(text)

st.markdown("![Alt Text](https://raw.githubusercontent.com/sandroormeno/app_for_running/main/images/path.PNG)")

text = "Para representar la velocidad estoy usando un mapeo de color como se muestra a continuación:"
st.markdown(text)
color = cm.LinearColormap(['red','yellow', 'green'],
                        vmin=1, vmax=2.8,
                        index=[0, 2.0, 2.8])                     
st.write(color)

text = '''
Esto quiere decir que estoy usando :red[rojo] para bajas velocidades (1 mts/seg) y :green[verde] para altas velocidades (2.8mts/seg). 
Además, también se representa en el espesor del trazo.

'''


st.markdown(text)

indice = st.slider('Imagen a ver: ', 11, 774, 567)


#m = folium.Map(location=[-12.1070348,-76.9468047], zoom_start=10)

#m.fit_bounds([[-12.085559732437236, -76.95951832322937], [-12.116557310906174, -76.93135291029945]])
#Draw(export=True).add_to(m)
# tutorial
from streamlit_folium import st_folium

m = folium.Map(pos[indice], zoom_start=16)
index = "<i>Indice: " + str(indice) + "</i>"
folium.Marker(pos[indice],tooltip=index ).add_to(m)
#Draw(export=True).add_to(m)

c1, c2 = st.columns(2)
with c1:
    #output = st_folium(m, width=700, height=500)
    st_folium(m, width=500, height=400)

with c2:
    #st.write(output)
    st.markdown(f"![Alt Text]({str(list_of_images[indice])})")
    
    

    

def show_maps(view, samples):
    down = dicts[view][0]
    up = dicts[view][1]
    
    #icon_url = 'https://raw.githubusercontent.com/sandroormeno/EnglishWeb/main/static/images/running1.png'
    icon_url = 'https://raw.githubusercontent.com/sandroormeno/app_for_running/main/images/running1.png'
    #icon_url_2 = 'https://raw.githubusercontent.com/sandroormeno/EnglishWeb/main/static/images/running2.png'
    icon_url_2 = 'https://raw.githubusercontent.com/sandroormeno/app_for_running/main/images/running2.png'
    
    lat_previo = 0
    long_previo = 0
    lat_previo_ = 0
    long_previo_ = 0
    s_ = 0
    s = 0
    t = 0
    tim = 0
    list_speed =[]
    color = cm.LinearColormap(['red','yellow', 'green'],
                            vmin=1, vmax=2.8,
                            index=[0, 2.0, 2.8])
    
    num = 0 
    for i in range(samples[0],samples[1]):
        if (i % 10 == 0):
            
            if (i <= mid and down == 1):
                if (lat_previo != 0):
                    origin = (lat_previo, long_previo)
                    dist = (data.iloc[i]['Lat'], data.iloc[i]['Long'])
                    s = s + float("{:.1f}".format(geodesic(origin, dist).meters))
                    s = float("{:.1f}".format(s))
                    speed = float("{:.1f}".format(geodesic(origin, dist).meters/30))
                    list_speed.append(speed)
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
                    tim = str(float("{:.1f}".format(t/60))) + " minutos"
                lat_previo = data.iloc[i]['Lat']
                long_previo = data.iloc[i]['Long']
                # integracion de la imagen
                image =f"https://raw.githubusercontent.com/sandroormeno/app_for_running/main{df_img.iloc[num]['path']}"
                html = f"<img src={str(image)} width='400' height='400'><br><i>Tiempo : {str(tim)}<br>Distacia: {str(s)} mts<br>Velocidad: {str(speed)} mts/seg<br>&copy 2023 Sandro Ormeño</i>"
                iframe = branca.element.IFrame(html=html, width=400+20, height=400+90)
                popup = folium.Popup(iframe, max_width=2650)
                #if(i == samples[0]):
                #    iframe = folium.IFrame("<img src='https://raw.githubusercontent.com/sandroormeno/EnglishWeb/main/static/images/ini.jpg'> <i><br>Hora: " + str(data.iloc[i]['Tiempo']) + " <br>Tiempo : " + str(tim) + " <br>Distacia: "+ str(s) + " mts<br>Velocidad: "+ str(speed)+" mts/seg</i>")
                #    iframe_ = branca.element.IFrame(html=iframe, width=340, height=210)
                #elif(i == mid):
                #    iframe = folium.IFrame("<img src='https://raw.githubusercontent.com/sandroormeno/EnglishWeb/main/static/images/fin.jpg'> <i><br>Hora: " + str(data.iloc[i]['Tiempo']) + " <br>Tiempo : " + str(tim) + " <br>Distacia: "+ str(s) + " mts<br>Velocidad: "+ str(speed)+" mts/seg</i>")
                #    iframe_ = branca.element.IFrame(html=iframe, width=340, height=210)
                #else:
                #    iframe = folium.IFrame("Hora: " + str(data.iloc[i]['Tiempo']) + " <br>Tiempo : " + str(tim) + " <br>Distacia: "+ str(s) + " mts<br>Velocidad: "+ str(speed)+" mts/seg<br>Altitud: "+ str(data.iloc[i]['Altitude'])  +" mts</i>")
                #    iframe_ = branca.element.IFrame(html=iframe, width=200, height=130)
                #popup = folium.Popup(iframe, min_width=180, max_width=250, height=500)
                
                #popup = folium.Popup(iframe_,  max_width=210)
                
                index = "<i>Sample: " + str(i) + "</i>"
                

                folium.Marker([data.iloc[i]['Lat'], data.iloc[i]['Long']], 
                              icon = folium.features.CustomIcon(icon_url,icon_size=(64, 64)),  # Creating a custom Icon
                              popup=popup, 
                              tooltip=index,
                              ).add_to(correr_group)
                             
                #folium.Circle(location=[data.iloc[i]['Lat'],data.iloc[i]['Long']],radius=speed*4,color=color(speed), fill= True, fill_opacity=0.9, weight=0, popup=popup, tooltip=index).add_to(map_sby)
                origin = [data.iloc[i]['Lat'], data.iloc[i]['Long']]
                destino =[data.iloc[i-10]['Lat'], data.iloc[i-10]['Long']]
                speed_text = "<i>Speed: " + str(speed) + " mts/seg</i>"
                #folium.PolyLine([origin,destino], color=color(speed), weight=speed*3, opacity=1, dash_array="5, 10", tooltip=speed_text).add_to(view_path)
            elif(i > mid and up == 1):
                if (lat_previo != 0):
                    origin = (lat_previo, long_previo)
                    dist = (data.iloc[i]['Lat'], data.iloc[i]['Long'])
                    s = s + float("{:.1f}".format(geodesic(origin, dist).meters))
                    s = float("{:.1f}".format(s))
                    speed = float("{:.1f}".format(geodesic(origin, dist).meters/30))
                    list_speed.append(speed)
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
                    tim = str(float("{:.1f}".format(t/60))) + " minutos" 
                lat_previo = data.iloc[i]['Lat']
                long_previo = data.iloc[i]['Long']
                # https://raw.githubusercontent.com/sandroormeno/EnglishWeb/main/static/images/ini.jpg
                #iframe = folium.IFrame("<img src='https://raw.githubusercontent.com/sandroormeno/EnglishWeb/main/static/images/ini.jpg' width='100' height='100'> <i><br>Hora: " + str(data.iloc[i]['Tiempo']) + " <br>Tiempo : " + str(tim) + " <br>Distacia: "+ str(s) + " mts<br>Speed: "+ str(speed)+" mts/seg</i>")
                #popup = folium.Popup(iframe, min_width=180, max_width=250)
                #if(i == mid):
                #    iframe = folium.IFrame("<img src='https://raw.githubusercontent.com/sandroormeno/EnglishWeb/main/static/images/fin.jpg'> <i><br>Hora: " + str(data.iloc[i]['Tiempo']) + " <br>Tiempo : " + str(tim) + " <br>Distacia: "+ str(s) + " mts<br>Velocidad: "+ str(speed)+" mts/seg<br>Altitud: "+ str(data.iloc[i]['Altitude'])  +" mts</i>")
                #    iframe = folium.IFrame("Hora: " + str(data.iloc[i]['Tiempo']) + " <br>Tiempo : " + str(tim) + " <br>Distacia: "+ str(s) + " mts<br>Speed: "+ str(speed)+" mts/seg mts<br>Altitude: "+ str(data.iloc[i]['Altitude'])  +" mts</i>")
                #    iframe_ = branca.element.IFrame(html=iframe, width=340, height=210)
                #else:
                    #iframe = folium.IFrame("Hora: " + str(data.iloc[i]['Tiempo']) + " <br>Tiempo : " + str(tim) + " <br>Distacia: "+ str(s) + " mts<br>Speed: "+ str(speed)+" mts/seg</i>")
                #    iframe = folium.IFrame("Hora: " + str(data.iloc[i]['Tiempo']) + " <br>Tiempo : " + str(tim) + " <br>Distacia: "+ str(s) + " mts<br>Velocidad: "+ str(speed)+" mts/seg<br>Altitud: "+ str(data.iloc[i]['Altitude'])  +" mts</i>")
                #    iframe_ = branca.element.IFrame(html=iframe, width=200, height=130)   
                #popup = folium.Popup(iframe_, lolo = df_img.iloc[-1]['path']
                image=f"https://raw.githubusercontent.com/sandroormeno/app_for_running/main{df_img.iloc[num]['path']}"
                html = f"<img src={str(image)} width='400' height='400'><br><i>Tiempo : {str(tim)}<br>Distacia: {str(s)} mts<br>Velocidad: {str(speed)} mts/seg<br>&copy 2023 Sandro Ormeño</i>" #<h6>Heading level 6</h6>
                iframe = branca.element.IFrame(html=html, width=400+20, height=400+90)
                popup = folium.Popup(iframe, max_width=2650)
                index = "<i>Sample: " + str(i) + "</i>"
                folium.Marker([data.iloc[i]['Lat'], data.iloc[i]['Long']], 
                              popup=popup, 
                              tooltip=index,
                              icon = folium.features.CustomIcon(icon_url_2,icon_size=(64, 64)),
                              ).add_to(correr_group)
                              
                origin = [data.iloc[i]['Lat'], data.iloc[i]['Long']]
                destino =[data.iloc[i-10]['Lat'], data.iloc[i-10]['Long']]
                speed_text = "<i>Speed: " + str(speed) + " mts/seg</i>"
                #folium.PolyLine([origin,destino], color=color(speed), weight=speed*3, opacity=1, dash_array="5, 10", tooltip=speed_text).add_to(view_path)
                #folium.PolyLine([origin,destino], color=color(speed), weight=speed*3, opacity=1, tooltip=speed_text).add_to(view_path)
            num = num +1 
        if (i % 2 == 0):
            if (i <= mid and down == 1):
                if (lat_previo_ != 0):
                    origin = (lat_previo_, long_previo_)
                    dist = (data.iloc[i]['Lat'], data.iloc[i]['Long'])
                    s_ = s_ + float("{:.1f}".format(geodesic(origin, dist).meters))
                    s_ = float("{:.1f}".format(s_))
                    speed = float("{:.1f}".format(geodesic(origin, dist).meters/6))
                    #list_speed.append(speed)
                else:
                    s_ = 0
                    speed = 0
                lat_previo_ = data.iloc[i]['Lat']
                long_previo_ = data.iloc[i]['Long']
                origin = [data.iloc[i]['Lat'], data.iloc[i]['Long']]
                destino =[data.iloc[i-2]['Lat'], data.iloc[i-2]['Long']]
                speed_text = "<i>Speed: " + str(speed) + " mts/seg</i>"
                #folium.PolyLine([origin,destino], color=color(speed), weight=speed*3, opacity=1, dash_array="5, 10", tooltip=speed_text).add_to(view_path)
                folium.PolyLine([origin,destino], color=color(speed), weight=speed*speed*3, opacity=.7, tooltip=speed_text).add_to(view_path)
            elif(i > mid and up == 1):
                if (lat_previo_ != 0):
                    origin = (lat_previo_, long_previo_)
                    dist = (data.iloc[i]['Lat'], data.iloc[i]['Long'])
                    s_ = s_ + float("{:.1f}".format(geodesic(origin, dist).meters))
                    s_ = float("{:.1f}".format(s_))
                    speed = float("{:.1f}".format(geodesic(origin, dist).meters/6))
                    #list_speed.append(speed)
                else:
                    s_ = 0
                    speed = 0
                lat_previo_ = data.iloc[i]['Lat']
                long_previo_ = data.iloc[i]['Long']
                origin = [data.iloc[i]['Lat'], data.iloc[i]['Long']]
                destino =[data.iloc[i-2]['Lat'], data.iloc[i-2]['Long']]
                speed_text = "<i>Speed: " + str(speed) + " mts/seg</i>"
                #folium.PolyLine([origin,destino], color=color(speed), weight=speed*3, opacity=1, dash_array="5, 10", tooltip=speed_text).add_to(view_path)
                folium.PolyLine([origin,destino], color=color(speed), weight=speed*speed*3, opacity=.7, tooltip=speed_text).add_to(view_path)
            
    st.write("### Algunas estadisticas:")        
    st.write("Total de distancia  recorrida:  __" + str(s) + " mts__")
    st.write("Total de tiempo usado en el recorrido:  __" + str(tim) + "__")
    speed_average = float("{:.2f}".format(sum(list_speed)/len(list_speed)))
    st.write("Velocidad promedio del recorrido:  __" + str(speed_average) + " mts/seg__")
    df_speed = pd.DataFrame(list_speed, columns=['speed'])
    #import io
    #st.table(df_speed)
    #st.write(df_speed.describe())
    #fig, ax = plt.subplots(figsize =(10, 7))
    #plt.hist(x)
    #ax.hist(list_speed, bins = [1.0, 1.5, 2.0, 2.5, 2.8])
    #contador = df_speed.value_counts(dropna=False)
    contador = df_speed.value_counts(dropna=False)
    #st.write(contador)
    #st.write(dict(contador))# df_index_set.dtypes
    lolo = np.c_[np.unique(df_speed.speed, return_counts=1)]
    su1 = df_speed['speed'].value_counts().index.tolist()
    df_ = df_speed.value_counts().rename_axis('speed').to_frame('counts')
    #st.write(df_)
    
    #print(df_["counts"].tolist())
    #print(list(df_.index.values))
    
    #fig, x = plt.subplots()

    #x.hist(df_speed['speed'], color='orange', bins=5)
    #plotting the figure

    #st.pyplot(fig)
    
    import plotly.express as px
    
    l = list(df_.index.values)
    list_speed=[]
    for i in l:
        list_speed.append(i[0])
        
    data_h = pd.DataFrame(
    {

        "Speed" : list_speed , 
        "counts": np.array(df_["counts"].tolist()),
    }
    )
    
    data_h["Speed"] = data_h["Speed"].astype(str) + " m/s"

    #st.table(grouper)
    
    fig = px.histogram(
        data_h,
        x="Speed",
        y="counts",
        color="Speed",
        color_discrete_sequence=[
            px.colors.sample_colorscale("rdylgn", v)[0]
            for v in (
                data_h["counts"] / data_h["counts"].max()
            ).tolist()
        ],
        hover_data=dict(Speed=False),
    )
    fig.update_layout(title_text='Histograma de velocidades', title_x=0.4)
    fig.update_layout(showlegend=False)
    fig.update_yaxes(title="  ")

    st.plotly_chart(fig, use_container_width=True)
    
    
    st.markdown("Espero hacer más análisis con los datos recopilados y con los que pueda generar.")
     
    correr_group.add_to(map_sby)
    view_path.add_to(map_sby)
    folium.LayerControl(collapsed=True).add_to(map_sby)
    folium_static(map_sby)
    




show_maps(view_data, values)

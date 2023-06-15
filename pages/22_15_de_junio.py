import pandas as pd 
import folium 
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
import random
#import chardet



#with open('GPS-7-5-2023.CSV', 'rb') as rawdata:
#    result = chardet.detect(rawdata.read(100000))
#print(result)
#import vincent
#import json
st.title('Route on bikeway in La Molina') # 32 / 5.000

#file_encoding = 'utf8'        # set file_encoding to the file encoding (utf8, latin1, etc.)
#input_fd = open('https://raw.githubusercontent.com/sandroormeno/app_for_running/main/data/GPS-7-5-2023.CSV', encoding=file_encoding, errors = 'backslashreplace')

data = pd.read_csv('https://raw.githubusercontent.com/sandroormeno/app_for_running/main/data/GPS-15-6-2023.CSV') # GPS.CSV
#data =pd.read_csv(input_fd)

#add_select = st.sidebar.selectbox("Cuál data quieres ver?",("OpenStreetMap", "Stamen Terrain","Stamen Toner"))#for calling the function for getting center of maps
add_select = 'cartodbpositron' # 'stamentoner' OpenStreetMap cartodbdark_matter cartodbpositron stamenwatercolor cartodbdark_matter
#select_data = st.sidebar.radio("What data do you want to see?"("Total_Pop", "Area_Region","Male_Pop",'Female_Pop'))


_ = ''' estas son los datos para casa archivo.csv
csv                 ini         mid         fin
GPS-3-11-2023.CSV   280         890         1620
GPS-3-15-2023.CSV   130         730         1410
GPS-3-19-2023.CSV   150         970         1870
GPS-3-27-2023.CSV   140         790         1540
GPS-3-29-2023.CSV   120         770         1510
GPS-3-31-2023.CSV   120         870         1750
'''

dicts = {"Run down": [1,0],
         "Run Up": [0,1],
         "Both": [1,1] }
         
a = st.empty()
#view_data = a.radio("What data do you want to see?", ("Run down", "Run Up", "Both"), 0, key=2)   
      
view_data = st.sidebar.radio("What data do you want to see?", ("Run down", "Run Up", "Both"), 0, key=20)

# valores inicales 
#ini = 100 #280
#mid = int((1823*0.05)+110) # 890
#mid = int(len(data)/2) # 890
#fin = len(data)-50 # 1620



ini = 110 #280
mid = 1050 # 890
fin = 2045 # 1620
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
#mid_= 380

#st.text('https://raw.githubusercontent.com/sandroormeno/app_for_running/main'+str(df.iloc[0]['path']))

correr_group = folium.FeatureGroup(name="View path + images", show=True)
feature_group = folium.FeatureGroup(name="View images", show=False)
img_group = folium.FeatureGroup(name="View images better", show=False)
view_path = folium.FeatureGroup(name="View only path", show=False)
view_altitud = folium.FeatureGroup(name="View Altitud", show=False)

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


# this is the better View
df_img = pd.read_csv('https://raw.githubusercontent.com/sandroormeno/app_for_running/main/OpenCamera/data_gps_image.csv')




#st.markdown("![Alt Text](https://raw.githubusercontent.com/sandroormeno/app_for_running/main/images/run.gif)")
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
#st.markdown(text)

#st.markdown("![Alt Text](https://raw.githubusercontent.com/sandroormeno/app_for_running/main/images/view_path.gif)")


text = "Para representar la velocidad estoy usando un mapeo de color como se muestra a continuación:"
#st.markdown(text)
color = cm.LinearColormap(['red','yellow', 'green'],
                        vmin=1, vmax=2.8,
                        index=[0, 2.0, 2.8])  
#st.write(color) 

text = '''
Esto quiere decir que estoy usando :red[rojo] para bajas velocidades (1 mts/seg) y :green[verde] para altas velocidades (2.8mts/seg). 
Además, también se representa en el espesor del trazo.

'''

#st.markdown(text)                        

text = "También se representa la altura del terreno, el cual se puede visualizar en el apartado `View Altitud`. En combinación con `View only path`,  se puede tener tener una intuición de la dificultad del recorrido."
#st.markdown(text)
#st.markdown("![Alt Text](https://raw.githubusercontent.com/sandroormeno/app_for_running/main/images/view_altitude.gif)")
                       
colormap_h = cm.LinearColormap(['#525252','#bababa', '#f0f0f0'],
                        vmin=200.0, vmax=400.0,
                        index=[220.0, 300.0, 400.0])
#st.write(colormap_h) 

text = '''
<style>
gris { color: #a8a8a8 }
grisoscuro { color: #696969 }
</style>
Estoy usando una escala de grices para mostrar la altura que tiene un rango de entre 200 a 400 metros sobre el nivel del mar. 
Esto quiere decir que estoy usando <gris> __gris__ </gris>  para altas alturas  (360 metros sobre el nivel del mar) y <grisoscuro>__un gris oscuro__</grisoscuro> para altas bajas alturas (240 mts).
'''
#st.markdown(text,unsafe_allow_html=True)


text = '''
<style>
gris { color: #a8a8a8 }
grisoscuro { color: #696969 }
</style>
Si desea ver imágenes del recorrio, he incluido alguas fotografías a intervalos y con posicionamiento. 
Use el `slider` para seleccionar las imágenes o puede hacer click en las marcas con el icono del personaje corriendo en el último mapa, más abajo.
'''
#st.markdown(text,unsafe_allow_html=True)



from streamlit_folium import st_folium

#m = folium.Map(location=[-12.1070348,-76.9468047], zoom_start=10)

#m.fit_bounds([[-12.085559732437236, -76.95951832322937], [-12.116557310906174, -76.93135291029945]])
#Draw(export=True).add_to(m)
# tutorial
def show_map_picture(picture):
    indice = st.slider(' ', 11, 774, picture)
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


Picture = 112
#show_map_picture(Picture)
    

    
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
    period_time = 30
    for i in range(samples[0],samples[1]):
        if (i % 10 == 0):
            
            if (i <= mid and down == 1):
                if (lat_previo != 0):
                    origin = (lat_previo, long_previo)
                    dist = (data.iloc[i]['Lat'], data.iloc[i]['Long'])
                    s = s + float("{:.1f}".format(geodesic(origin, dist).meters))
                    s = float("{:.1f}".format(s))
                    speed = float("{:.1f}".format(geodesic(origin, dist).meters/period_time))
                    list_speed.append(speed)
                else:
                    s = 0
                    speed = 0
                if (i != samples[0]):  
                    t = t + period_time
                else:
                    t = 0
                if (t <= 60):
                    tim = str(t) + " seg"
                else:
                    tim = str(float("{:.1f}".format(t/60))) + " minutos"
                lat_previo = data.iloc[i]['Lat']
                long_previo = data.iloc[i]['Long']
                # integracion de la imagen
                #image =f"https://raw.githubusercontent.com/sandroormeno/app_for_running/main{df_img.iloc[num]['path']}"
                #html = f"<img src={str(image)} width='400' height='400'><br><i>Tiempo : {str(tim)}<br>Distacia: {str(s)} mts<br>Velocidad: {str(speed)} mts/seg<br>&copy 2023 Sandro Ormeño</i>"
                html = f"<i>Tiempo : {str(tim)}<br>Distacia: {str(s)} mts<br>Velocidad: {str(speed)} mts/seg<br>&copy 2023 Sandro Ormeño</i>"
                #iframe = branca.element.IFrame(html=html, width=400+20, height=400+90)
                iframe = branca.element.IFrame(html=html, width=200, height=100)
                popup = folium.Popup(iframe, max_width=2650)
               
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
                #p = data.iloc[i]['Altitude']
                #text_ = "<i>Altitud: " + str(p) + "</i>"
                #folium.Circle(location=(data.iloc[i]['Lat'],data.iloc[i]['Long']),popup=text_,radius=20, fill_opacity = 1.0,stroke=False, color=colormap_h(p), fill=True, fill_color= colormap_h(p)).add_to(view_path)
                #folium.PolyLine([origin,destino], color=color(speed), weight=speed*3, opacity=1, dash_array="5, 10", tooltip=speed_text).add_to(view_path)
            elif(i > mid and up == 1):
                if (lat_previo != 0):
                    origin = (lat_previo, long_previo)
                    dist = (data.iloc[i]['Lat'], data.iloc[i]['Long'])
                    s = s + float("{:.1f}".format(geodesic(origin, dist).meters))
                    s = float("{:.1f}".format(s))
                    speed = float("{:.1f}".format(geodesic(origin, dist).meters/period_time))
                    list_speed.append(speed)
                else:
                    s = 0
                    speed = 0
                if (i != samples[0]):  
                    t = t + period_time
                else:
                    t = 0
                if (t <= 60):
                    tim = str(t) + " seg"
                else:
                    tim = str(float("{:.1f}".format(t/60))) + " minutos" 
                lat_previo = data.iloc[i]['Lat']
                long_previo = data.iloc[i]['Long']
                # https://raw.githubusercontent.com/sandroormeno/EnglishWeb/main/static/images/ini.jpg

                #image=f"https://raw.githubusercontent.com/sandroormeno/app_for_running/main{df_img.iloc[num]['path']}"
                #html = f"<img src={str(image)} width='400' height='400'><br><i>Tiempo : {str(tim)}<br>Distacia: {str(s)} mts<br>Velocidad: {str(speed)} mts/seg<br>&copy 2023 Sandro Ormeño</i>" #<h6>Heading level 6</h6>
                #iframe = branca.element.IFrame(html=html, width=400+20, height=400+90)
                                
                html = f"<i>Tiempo : {str(tim)}<br>Distacia: {str(s)} mts<br>Velocidad: {str(speed)} mts/seg<br>&copy 2023 Sandro Ormeño</i>"
                iframe = branca.element.IFrame(html=html, width=200, height=100)
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
                #p = data.iloc[i]['Altitude']
                #text_ = "<i>Altitud: " + str(p) + "</i>"
                #folium.Circle(location=(data.iloc[i]['Lat'],data.iloc[i]['Long']),popup=text_,radius=20, fill_opacity = 1.0, stroke=False, color=colormap_h(p), fill=True, fill_color= colormap_h(p)).add_to(view_path)
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
                p = data.iloc[i]['Altitude']
                text_a = "<i>Altitud: " + str(p) + "</i>"
                folium.Circle(location=(data.iloc[i]['Lat'],data.iloc[i]['Long']),radius=20, fill_opacity = 1.0, stroke=False, color=colormap_h(p), fill=True, fill_color= colormap_h(p), tooltip=text_a).add_to(view_altitud)
                #folium.Circle(location=(data.iloc[i]['Lat'],data.iloc[i]['Long']),radius=10, fill=True, color= colormap_h(p)).add_to(view_path)
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
                p = data.iloc[i]['Altitude']
                text_a = "<i>Altitud: " + str(p) + "</i>"
                folium.Circle(location=(data.iloc[i]['Lat'],data.iloc[i]['Long']),radius=20, fill_opacity = 1.0, stroke=False, color=colormap_h(p), fill=True, fill_color= colormap_h(p), tooltip=text_a).add_to(view_altitud)
                #folium.Circle(location=(data.iloc[i]['Lat'],data.iloc[i]['Long']),radius=10, fill=True, color= colormap_h(p)).add_to(view_path)
            
    st.write("### Algunas estadisticas:")        
    st.write("Total de distancia  recorrida:  __" + str(s) + " mts__")
    st.write("Total de tiempo usado en el recorrido:  __" + str(tim) + "__")
    speed_average = float("{:.2f}".format(sum(list_speed)/len(list_speed)))
    st.write("Velocidad promedio del recorrido:  __" + str(speed_average) + " mts/seg__")
    df_speed = pd.DataFrame(list_speed, columns=['speed'])
    
    st.write("Además, podemos representar la distribución de las frecuencias de velocidades:")

    contador = df_speed.value_counts(dropna=False)
    #st.write(contador)
    #st.write(dict(contador))# df_index_set.dtypes
    lolo = np.c_[np.unique(df_speed.speed, return_counts=1)]
    su1 = df_speed['speed'].value_counts().index.tolist()
    df_ = df_speed.value_counts().rename_axis('speed').to_frame('counts')
    #st.write(df_)
    #st.table(df_)
       
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
    
    newdf = data_h.sort_values(by='Speed') 
    #st.table(newdf)
    
    newdf["Speed"] = newdf["Speed"].astype(str) + " m/s"
    
    #st.table(newdf)
    
    my_colors = ['#992708', '#ab2d0a', '#de3709', '#eb3c0c', '#ff4917', '#EF553B', '#faa328', '#fad028', '#fae528', '#fcef35', '#faf328', '#effa28', '#dbfa28', '#cdfa28', '#adfa28', '#85f714', '#10e63b', '#09d932', '#08cf2f', '#07b329', '#069e24', '#048a1e', '#04801c', '#036917', '#035c14', '#025b14', '#025b27','#025b2c', '#025b33', '#025b3a','#025b40','#025b4b']
    my_Speed = ['0.7 m/s', '0.8 m/s', '0.9 m/s', '1.0 m/s', '1.1 m/s', '1.2 m/s','1.3 m/s','1.4 m/s','1.5 m/s','1.6 m/s','1.7 m/s','1.8 m/s','1.9 m/s', '2.0 m/s', '2.1 m/s', '2.2 m/s', '2.3 m/s', '2.4 m/s', '2.5 m/s', '2.6 m/s', '2.7 m/s', '2.8 m/s', '2.9 m/s',  '3.0 m/s', '3.1 m/s', '3.2 m/s', '3.3 m/s', '3.4 m/s', '3.5 m/s', '3.6 m/s', '3.7 m/s', '3.8 m/s']
    my_color_dict = dict(zip(my_Speed,my_colors ))
    fig = px.histogram(
        newdf,
        x="Speed",
        y="counts",
        color="Speed",
        #color_discrete_map = {'1.1 m/s':'#ff4917','1.3 m/s':'#EF553B','2 m/s':'yellow','2.8 m/s':'green'},
        color_discrete_map = my_color_dict,
        #color_discrete_sequence=['indianred']
        #color_discrete_sequence=px.colors.qualitative.G10 
        #color_discrete_sequence=['#ff4917', '#EF553B', '#faa328', '#fad028', '#fae528', '#fad728', '#faec28', '#effa28', '#dbfa28', '#cdfa28', '#adfa28', '#85f714', '#12fc31'],        
        hover_data=dict(Speed=False),
    )
    
    
    fig.update_layout(title_text='Histograma de velocidades', title_x=0.4)
    fig.update_layout(showlegend=False)
    fig.update_yaxes(title="  ")

    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("Espero hacer más análisis con los datos recopilados y con los que pueda generar.")
     
    correr_group.add_to(map_sby)
    view_altitud.add_to(map_sby)
    view_path.add_to(map_sby)
    folium.LayerControl(collapsed=True).add_to(map_sby)
    folium_static(map_sby)
    
show_maps(view_data, values)


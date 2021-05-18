from django.shortcuts import render
import folium
from folium.plugins import Search
import json
from requests import get
import html

# weather from OpenWeatherMap api
api_key = "969bd7bdde2aa8690b83ebfa2b4056cb"
urls = [f'http://api.openweathermap.org/data/2.5/weather?q=London&units=metric&appid={api_key}',
        f'http://api.openweathermap.org/data/2.5/weather?q=Moscow&units=metric&appid={api_key}',
        f'http://api.openweathermap.org/data/2.5/weather?q=Paris&units=metric&appid={api_key}',
        f'http://api.openweathermap.org/data/2.5/weather?q=New York&units=metric&appid={api_key}',
        f'http://api.openweathermap.org/data/2.5/weather?q=Tokyo&units=metric&appid={api_key}'
]

cities = ['London', 'Moscow', 'Paris', 'New York', 'Tokyo']
lon_lst, lat_lst, desc_lst, temper_lst = [], [], [], []
for url in urls:
    stations = get(url).json()
    lon = stations['coord']['lon']
    lat = stations['coord']['lat']
    desc = stations['weather'][0]['main']
    temper = stations['main']['temp']
    lon_lst.append(str(lon))
    lat_lst.append(str(lat))
    desc_lst.append(str(desc))
    temper_lst.append(str(temper))


def weather_map(request):
    m = folium.Map(location=[48.856613, 2.352222], zoom_start=1.7, tiles="Stamen Terrain")

    folium.TileLayer('openstreetmap').add_to(m)
    folium.TileLayer('Stamen Toner').add_to(m)
    # other mapping code (e.g. lines, markers etc.)
    folium.LayerControl().add_to(m)

    for n in range(len(lon_lst)):
        html=f'''
        <h4><b>{cities[n]} {temper_lst[n]}°C</b></h4>
        <p style="font-size:11pt;"><i class="fas fa-sun" style="font-size:25px;color:black"></i>{desc_lst[n]}</p>
        '''
        iframe = folium.IFrame(html=html, width=250, height=230)
        popup = folium.Popup(iframe, min_width=100, max_width=2650)
        folium.Marker([lat_lst[n], lon_lst[n]],
                      radius = 5,
                      popup = popup).add_to(m)

    m = m._repr_html_()
    context = {'my_map': m}

    return render(request, 'weather/weather.html', context)


def about(request):
    return render(request, 'weather/about.html', {'title': 'About'})

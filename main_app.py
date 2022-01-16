import streamlit as st
from streamlit_folium import folium_static
import folium
from datetime import datetime
from dateutil import tz
from streamlit_echarts import st_echarts

import os
import json
import requests
# from pprint import pprint

API_Key = "79474694d5c7f4cf4a1d2ee01d4d90fd"

st.set_page_config(layout="wide")

st.title("Real Time Weather Forecast Lookup App")
st.image('johannes-plenio-600dw3-1rv4-unsplash.jpg')
'''
*Top Photo by Johannes Plenio on Unsplash*
'''

def convert_to_celcius(kelvin_temp):
    become_celcius = kelvin_temp - 273.15
    return become_celcius

city_text = st.text_input('Enter the city (For example, London):', '')

if city_text:

    try:
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_text}&appid="
        final_url = weather_url + API_Key
        weather_data = requests.get(final_url).json()

        home1,home2,home3 = st.beta_columns(3)

        with home1:
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
            sunrise = weather_data['sys']['sunrise']
            # Convert UTC to local time using auto-detecting:
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
            utc1 = datetime.strptime(str(datetime.utcfromtimestamp(sunrise).strftime('%Y-%m-%d %H:%M:%S')),
                                     '%Y-%m-%d %H:%M:%S')
            utc1 = utc1.replace(tzinfo=from_zone)
            local1 = utc1.astimezone(to_zone)
            st.markdown("Sunrise: ")
            st.markdown(str(local1))
            st.image("https://media0.giphy.com/media/C3FangwuYVrIHPp0EB/giphy.gif", width=110)

            feels_like = weather_data['main']['feels_like']
            feels_like_temp = convert_to_celcius(feels_like)
            feels_like_temp = "{:.2f}".format(feels_like_temp)

            humidity = weather_data['main']['humidity']

            def get_gauge_options(value, name, color):
                options = {
                    "tooltip": {
                        "formatter": '{a} <br/>{b} : {c}%'
                    },
                    "series": [{
                        "type": 'gauge',
                        "startAngle": 180,
                        "endAngle": 0,
                        "progress": {
                            "show": "true"
                        },
                        "radius": '100%',

                        "itemStyle": {
                            "color": color,
                            "shadowColor": 'rgba(192,192,192,0.3)',
                            "shadowBlur": 10,
                            "shadowOffsetX": 2,
                            "shadowOffsetY": 2,
                            "radius": '55%',
                        },
                        "progress": {
                            "show": "true",
                            "roundCap": "true",
                            "width": 15
                        },
                        "pointer": {
                            "length": '60%',
                            "width": 8,
                            "offsetCenter": [0, '5%']
                        },
                        "detail": {
                            "valueAnimation": "true",
                            "formatter": '{value}',
                            "backgroundColor": '#fff',
                            "borderColor": '#999',
                            "borderWidth": 4,
                            "width": '60%',
                            "lineHeight": 20,
                            "height": 20,
                            "borderRadius": 188,
                            "offsetCenter": [0, '40%'],
                            "valueAnimation": "true",
                        },
                        "data": [{
                            "value": value,
                            "name": name
                        }]
                    }]
                }
                return options

            temp_options_1 = get_gauge_options(feels_like_temp, "Feels Like (°C)", "#527B94") #2F4554
            st_echarts(options=temp_options_1, width="100%", key=0)

            options_1 = get_gauge_options(humidity, "Humidity (%)", "#FF7F50")
            st_echarts(options=options_1, width="100%", key=3)

        with home2:
            sunset = weather_data['sys']['sunset']
            # Convert UTC to local time using auto-detecting:
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
            utc2 = datetime.strptime(str(datetime.utcfromtimestamp(sunset).strftime('%Y-%m-%d %H:%M:%S')),
                                     '%Y-%m-%d %H:%M:%S')
            utc2 = utc2.replace(tzinfo=from_zone)
            local2 = utc2.astimezone(to_zone)
            st.markdown("Sunset: ")
            st.markdown(str(local2))
            st.image("https://media1.giphy.com/media/J7CRqi4scgEaQ/giphy.gif", width=94)

            max_temp = weather_data['main']['temp_max']
            max_temp_temp = convert_to_celcius(max_temp)
            max_temp_temp = "{:.2f}".format(max_temp_temp)

            wind_speed = weather_data['wind']['speed']

            def get_gauge_options(value, name, color):
                options = {
                    "tooltip": {
                        "formatter": '{a} <br/>{b} : {c}%'
                    },
                    "series": [{
                        "type": 'gauge',
                        "startAngle": 180,
                        "endAngle": 0,
                        "progress": {
                            "show": "true"
                        },
                        "radius": '100%',

                        "itemStyle": {
                            "color": color,
                            "shadowColor": 'rgba(192,192,192,0.3)',
                            "shadowBlur": 10,
                            "shadowOffsetX": 2,
                            "shadowOffsetY": 2,
                            "radius": '55%',
                        },
                        "progress": {
                            "show": "true",
                            "roundCap": "true",
                            "width": 15
                        },
                        "pointer": {
                            "length": '60%',
                            "width": 8,
                            "offsetCenter": [0, '5%']
                        },
                        "detail": {
                            "valueAnimation": "true",
                            "formatter": '{value}',
                            "backgroundColor": '#fff',
                            "borderColor": '#999',
                            "borderWidth": 4,
                            "width": '60%',
                            "lineHeight": 20,
                            "height": 20,
                            "borderRadius": 188,
                            "offsetCenter": [0, '40%'],
                            "valueAnimation": "true",
                        },
                        "data": [{
                            "value": value,
                            "name": name
                        }]
                    }]
                }
                return options

            temp_options_2 = get_gauge_options(max_temp_temp, "Max Temperature (°C)", "#C23531")
            st_echarts(options=temp_options_2, width="100%", key=1)

            options_2 = get_gauge_options(wind_speed, "Wind Speed (m/s)", "#90EE90")
            st_echarts(options=options_2, width="100%", key=4)

        with home3:
            m = folium.Map(location=[weather_data['coord']['lat'], weather_data['coord']['lon']], width = 250, height = 168) # width = 443 225 height = 143 168 zoom_start=12
            folium.Marker([weather_data['coord']['lat'], weather_data['coord']['lon']], popup=city_text).add_to(m)
            folium_static(m, width = 250, height = 168)

            min_temp = weather_data['main']['temp_min']
            min_temp_temp = convert_to_celcius(min_temp)
            min_temp_temp = "{:.2f}".format(min_temp_temp)

            cloud = weather_data['clouds']['all']

            def get_gauge_options(value, name, color):
                options = {
                    "tooltip": {
                        "formatter": '{a} <br/>{b} : {c}%'
                    },
                    "series": [{
                        "type": 'gauge',
                        "startAngle": 180,
                        "endAngle": 0,
                        "progress": {
                            "show": "true"
                        },
                        "radius": '100%',

                        "itemStyle": {
                            "color": color,
                            "shadowColor": 'rgba(192,192,192,0.3)',
                            "shadowBlur": 10,
                            "shadowOffsetX": 2,
                            "shadowOffsetY": 2,
                            "radius": '55%',
                        },
                        "progress": {
                            "show": "true",
                            "roundCap": "true",
                            "width": 15
                        },
                        "pointer": {
                            "length": '60%',
                            "width": 8,
                            "offsetCenter": [0, '5%']
                        },
                        "detail": {
                            "valueAnimation": "true",
                            "formatter": '{value}',
                            "backgroundColor": '#fff',
                            "borderColor": '#999',
                            "borderWidth": 4,
                            "width": '60%',
                            "lineHeight": 20,
                            "height": 20,
                            "borderRadius": 188,
                            "offsetCenter": [0, '40%'],
                            "valueAnimation": "true",
                        },
                        "data": [{
                            "value": value,
                            "name": name
                        }]
                    }]
                }
                return options

            temp_options_3 = get_gauge_options(min_temp_temp, "Min Temperature (°C)", "#3399FF")
            st_echarts(options=temp_options_3, width="100%", key=2)

            options_3 = get_gauge_options(cloud, "Cloudiness (%)", "#61A0A8")
            st_echarts(options=options_3, width="100%", key=5)

        # pprint(weather_data)

    except:
        st.header("Please re-type the location again as you've misspelled it")


st.sidebar.write("Building a real-time weather forecasting app using OpenWeather API with visualisations to showcase the weather forecast of the city that the user has searched.")
st.sidebar.write("OpenWeather API Documentation: [https://openweathermap.org/current] (https://openweathermap.org/current)")
st.sidebar.write("Limitation: The timings of the sunrise and sunset are in UTC format and not according to the city the user has searched.")
st.sidebar.write("Have fun using this app to check the weather forecast before leaving your house!")
st.sidebar.subheader("Jim Meng Kok")
st.sidebar.markdown('Please feel free to connect with me on LinkedIn: [www.linkedin.com/in/jimmengkok](www.linkedin.com/in/jimmengkok)')
st.sidebar.markdown('Medium: [https://medium.com/@jimintheworld](https://medium.com/@jimintheworld)')

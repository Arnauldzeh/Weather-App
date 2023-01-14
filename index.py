# NEW CODE
import streamlit as st
import requests
def get_user_ip():
    ip_url = "https://api.ipify.org?format=json"
    try:
        ip_response = requests.get(ip_url)
        return ip_response.json()["ip"]
    except requests.exceptions.RequestException as e:
        st.write("Impossible de récupérer l'adresse IP de l'utilisateur.")
        st.write("Erreur:", e)
        return None

def get_location(ip):
    api_key = "aee7849fb61944aaa17409660529bc5d"
    geolocation_url = "https://api.ipgeolocation.io/ipgeo?apiKey={}&ip={}".format(api_key,ip)
    try:
        geolocation_response = requests.get(geolocation_url)
        location = geolocation_response.json()
        return location
    except requests.exceptions.RequestException as e:
        st.write("Impossible de récupérer les informations de géolocalisation.")
        st.write("Erreur:", e)
        return None

def get_city_coordinates(city):
    api_key = "26788b89116e49fc8199d5798a73d02d"
    geocode_url = "https://api.opencagedata.com/geocode/v1/json?q={}&key={}".format(city, api_key)
    try:
        geocode_response = requests.get(geocode_url)
        lat = geocode_response.json()["results"][0]["geometry"]["lat"]
        lon = geocode_response.json()["results"][0]["geometry"]["lng"]
        return lat, lon
    except requests.exceptions.RequestException as e:
        st.write("Impossible de récupérer les coordonnées de la ville.")
        st.write("Erreur:", e)
        return None

def get_weather(lat, lon):
    api_key = "8ad73f301dd774a37a0a13c03ed2f8f1"
    url = "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(lat, lon, api_key)
    try:
        r = requests.get(url)
        data = r.json()
        return data
    except requests.exceptions.RequestException as e:
        st.write("Impossible de récupérer les données météo.")
        st.write("Erreur:", e)
        return None


def get_forecast_weather(city):
    api_key = "8ad73f301dd774a37a0a13c03ed2f8f1"
    forecast_url = "http://api.openweathermap.org/data/2.5/forecast?q={}&appid={}".format(city, api_key)
    forecast_response = requests.get(forecast_url)
    return forecast_response.json()

def weather_app():
    st.title("Application Météo")
    st.write("Récupération de la météo à votre position actuelle:")
    ip = get_user_ip()
    location = get_location(ip)
    if location:
        lat, lon = location['latitude'], location['longitude'] 
        data = get_weather(lat, lon)
        if data:
            try:
                st.write("Température: {}°F".format(data["main"]["temp"]))
                st.write("Humidité: {}%".format(data["main"]["humidity"]))
                st.write("Pression: {} hPa".format(data["main"]["pressure"]))
            except KeyError:
                st.write("Données météorologiques non disponibles pour votre position actuelle.")
    else:
        st.write("Impossible de récupérer les informations de géolocalisation.")
        
    city = st.text_input("Entrez le nom de la ville:")
    if st.button("Valider"):
        lat, lon = get_city_coordinates(city)
        if lat and lon:
            data = get_weather(lat, lon)
            if data:
                st.write("Météo à {}:".format(city))
                st.write("Température: {}°F".format(data["main"]["temp"]))
                st.write("Humidité: {}%".format(data["main"]["humidity"]))
                st.write("Pression: {} hPa".format(data["main"]["pressure"]))
                forecast_data = get_forecast_weather(city)
                st.write("Prévisions météo pour les prochains 5 jours:")
                for day in forecast_data["list"]:
                    st.write("Date: {}".format(day["dt_txt"]))
                    st.write("Température: {}°F".format(day["main"]["temp"]))
                    st.write("Humidité: {}%".format(day["main"]["humidity"]))
        else:
            st.write("Impossible de récupérer les coordonnées de la ville.")

            st.write("Veuillez remplacer 'YOUR_API_KEY' par votre propre clé API")

if __name__ == "__main__":
    weather_app()


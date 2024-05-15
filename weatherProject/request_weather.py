import requests

BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'
forecast_url = 'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}'


def fetch_weather(api_key, city_name):
    url = f"{BASE_URL}appid={api_key}&q={city_name}"
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        print("Error:", response.status_code)
        return None


def fetch_forecast(api_key, city_name):
    city_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&units=metric&appid={api_key}"
    city_response = requests.get(city_url)

    if city_response.status_code == 200:
        city_data = city_response.json()
        if city_data:
            lat = city_data[0]['lat']
            lon = city_data[0]['lon']

            url = forecast_url.format(lat=lat, lon=lon, API_key=api_key)
            forecast_response = requests.get(url)

            if forecast_response.status_code == 200:
                forecast_data = forecast_response.json()
                return forecast_data
            else:
                print("Error fetching forecast data:", forecast_response.status_code)
                return None
        else:
            print("No data found for the city:", city_name)
            return None
    else:
        print("Error fetching city data:", city_response.status_code)
        return None


def get_local_icon(icon_code):
    icon_mapping = {
        "01d": "Icons/01d@2x.png",
        "02d": "Icons/02d@2x.png",
        "03d": "Icons/03d@2x.png",
        "04d": "Icons/04d@2x.png",
        "09d": "Icons/09d@2x.png",
        "10d": "Icons/10d@2x.png",
        "11d": "Icons/thunderstorm.png",
        "13d": "Icons/snow.png",
        "50d": "Icons/haze.png",
    }
    return icon_mapping.get(icon_code, "Icons/weather.png")


def get_tomorrow_forecast(forecast_data):
    tomorrow_data = None
    for data in forecast_data['list']:
        if '06:00:00' in data['dt_txt']:
            tomorrow_data = data
            break

    if tomorrow_data:
        temperature = tomorrow_data['main']['temp']
        temperature = kelvin_to_celsius(temperature)
        humidity = tomorrow_data['main']['humidity']
        wind_speed = tomorrow_data['wind']['speed']

        lst = [temperature, humidity, wind_speed]
        return lst
    else:
        return None, None, None



def get_twoday_forecast(forecast_data):
    twoday_data = None
    found_tomorrow = False
    for data in forecast_data['list']:
        if found_tomorrow and '12:00:00' in data['dt_txt']:
            twoday_data = data
            break
        if '06:00:00' in data['dt_txt']:
            found_tomorrow = True

    if twoday_data:
        temperature = twoday_data['main']['temp']
        temperature = kelvin_to_celsius(temperature)
        humidity = twoday_data['main']['humidity']
        wind_speed = twoday_data['wind']['speed']
        lst = [temperature, humidity, wind_speed]
        return lst
    else:
        return None, None, None

def get_threeday_forecast(forecast_data):
    threeday_data = None
    found_tomorrow = False
    for data in forecast_data['list']:
        if found_tomorrow and '12:00:00' not in data['dt_txt']:
            threeday_data = data
            break
        if '06:00:00' not in data['dt_txt']:
            found_tomorrow = True
    if threeday_data:
        temperature = threeday_data['main']['temp']
        temperature = kelvin_to_celsius(temperature)
        humidity = threeday_data['main']['humidity']
        wind_speed = threeday_data['wind']['speed']
        lst = [temperature, humidity, wind_speed]
        return lst
    else:
        return None, None, None

def get_fourday_forecast(forecast_data):
    fourday_data = None
    found_threeday = False
    found_twoday = False
    for data in forecast_data['list']:
        if found_threeday and found_twoday and '12:00:00' not in data['dt_txt']:
            fourday_data = data
            break
        if '06:00:00' not in data['dt_txt'] and not found_threeday:
            found_threeday = True
        if '06:00:00' in data['dt_txt'] and found_threeday and not found_twoday:
            found_twoday = True
    if fourday_data:
        temperature = fourday_data['main']['temp']
        temperature = kelvin_to_celsius(temperature)
        humidity = fourday_data['main']['humidity']
        wind_speed = fourday_data['wind']['speed']
        lst = [temperature, humidity, wind_speed]
        return lst
    else:
        return None, None, None


def get_temperature(weather_data):
    temp = weather_data['main']['temp']
    return kelvin_to_celsius(temp)

def kelvin_to_celsius(weather_data):
    celsius = weather_data - 273.15
    celsius = round(celsius, 1)
    return celsius

def get_humidity(weather_data):
    return weather_data['main']['humidity']

def get_wind_speed(weather_data):
    return weather_data['wind']['speed']

def get_humidity(weather_data):
    return weather_data['main']['humidity']







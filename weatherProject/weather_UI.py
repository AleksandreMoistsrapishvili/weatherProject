import sqlite3
import sys
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.uic import loadUi
from request_weather import *
from date_weather import *
from currentLocation import get_city

API_KEY = "19d6a39cb49cc4c0d38b8d29968f17f3"


class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("weather.ui", self)
        self.setWindowTitle("Weather Program")
        self.cityName.setStyleSheet("color: black; font-weight: bold; font-size: 20px;")
        self.citySearch.setStyleSheet("color:black; font-size: 18px;")
        self.searchButton.setStyleSheet("background-color: #5372F0; border-radius: 10px;")
        self.currLocation.setStyleSheet("background-color: rgb(168, 168, 168); border-radius: 10px;")
        self.weatherDate.setStyleSheet("color: #ffffff; font-weight: bold; font-size:18px;")
        self.weatherDate.setText(f"Tbilisi({today_date()})")
        self.set_icon("Icons/weather.png")
        self.mainIcon.setFixedSize(50, 35)
        self.searchButton.clicked.connect(self.update_weather)
        self.currLocation.clicked.connect(self.currentLoc)
        self.initialize_default()

    def set_icon(self, path):
        pixmap = QPixmap(path)
        self.mainIcon.setPixmap(pixmap)

    def initialize_default(self):
        self.update_weather("Tbilisi")

    def set_todayIcon(self, path):
        pixmap = QPixmap(path)
        self.todayIcon.setPixmap(pixmap)

    def set_twoday_icon(self, path):
        pixmap = QPixmap(path)
        self.twodayIcon.setPixmap(pixmap)

    def set_threeday_icon(self, path):
        pixmap = QPixmap(path)
        self.threedayIcon.setPixmap(pixmap)

    def set_fourday_icon(self, path):
        pixmap = QPixmap(path)
        self.fourdayIcon.setPixmap(pixmap)

    def set_tomorrowIcon(self, path):
        pixmap = QPixmap(path)
        self.tomorrowIcon.setPixmap(pixmap)

    def search_clicked(self):
        return self.citySearch.text()

    def fetch_weather(self, city_name):
        response = fetch_weather(API_KEY, city_name)
        if response:
            return response
        else:
            print("Failed to fetch weather data.")
            return None

    def update_weather(self, city_name=None):
        if not city_name:
            city_name = self.search_clicked()

        weather_data = self.fetch_weather(city_name)
        if weather_data:
            self.set_temperature(weather_data)
            self.set_wind_speed(weather_data)
            self.set_humidity(weather_data)
            self.set_cityName(city_name)
            self.tomorrow_forecast(city_name)
            self.twoday_forecast(city_name)
            self.threeday_forecast(city_name)
            self.fourday_forecast(city_name)
            self.insert_weatherDB(city_name, weather_data)
        else:
            print("Failed to update weather.")

    def set_temperature(self, weather_data):
        temperature = get_temperature(weather_data)
        icon_code = weather_data['weather'][0]['icon']
        set_ic = get_local_icon(icon_code)
        self.weatherTemp.setText(f"Temperature: {temperature:.1f} °C")
        self.set_todayIcon(set_ic)

    def set_wind_speed(self, weather_data):
        wind_speed = get_wind_speed(weather_data)
        self.weatherWind.setText(f"Wind: {wind_speed} m/s")

    def set_humidity(self, weather_data):
        humidity = get_humidity(weather_data)
        self.weatherHum.setText(f"Humidity: {humidity} %")

    def set_cityName(self, city_name):
        weather = today_date()
        city_name = city_name[0].upper() + city_name[1:]
        self.weatherDate.setText(f"{city_name}({weather})")

    def tomorrow_forecast(self, city_name):
        weather_data = self.fetch_weather(city_name)
        if weather_data:
            tomorrow = tomorrow_date()
            forecast_data = fetch_forecast(API_KEY, city_name)
            get_tomorrow = get_tomorrow_forecast(forecast_data)
            icon_code = weather_data['weather'][0]['icon']
            set_ic = get_local_icon(icon_code)
            self.set_tomorrowIcon(set_ic)
            self.tomorrowDate.setText(f"{tomorrow}")
            self.tomorrowTemp.setText(f"Temperature: {get_tomorrow[0]}")
            self.tomorrowWind.setText(f"Wind Speed: {get_tomorrow[1]}")
            self.tomorrowHumidity.setText(f"Humidity: {get_tomorrow[2]}")

    def twoday_forecast(self, city_name):
        weather_data = self.fetch_weather(city_name)
        if weather_data:
            get_date = twoday_date()
            forecast_data = fetch_forecast(API_KEY, city_name)
            get_twoday = get_twoday_forecast(forecast_data)
            icon_code = weather_data['weather'][0]['icon']
            set_ic = get_local_icon(icon_code)
            self.set_twoday_icon(set_ic)
            self.twoDayForecast.setText(get_date)
            self.twodayTemp.setText(f"Temperature: {get_twoday[0]}")
            self.twodayWind.setText(f"Wind Speed: {get_twoday[1]}")
            self.twodayHumi.setText(f"Humidity: {get_twoday[2]}")

    def threeday_forecast(self, city_name):
        weather_data = self.fetch_weather(city_name)
        if weather_data:
            get_date = threeday_date()
            forecast_data = fetch_forecast(API_KEY, city_name)
            get_threeday = get_threeday_forecast(forecast_data)
            icon_code = weather_data['weather'][0]['icon']
            set_ic = get_local_icon(icon_code)
            self.set_threeday_icon(set_ic)
            self.threedayDate.setText(get_date)
            self.threedayTemp.setText(f"Temperature: {get_threeday[0]}")
            self.threedayWind.setText(f"Wind speed: {get_threeday[1]}")
            self.threedayHumi.setText(f"Humidity: {get_threeday[2]}")

    def fourday_forecast(self, city_name):
        weather_data = self.fetch_weather(city_name)
        if weather_data:
            get_date = fourthday_date()
            forecast_data = fetch_forecast(API_KEY, city_name)
            get_fourday = get_fourday_forecast(forecast_data)
            icon_code = weather_data['weather'][0]['icon']
            set_ic = get_local_icon(icon_code)
            self.set_fourday_icon(set_ic)
            self.fourdayDate.setText(get_date)
            self.fourdayTemp.setText(f"Temperature: {get_fourday[0]}")
            self.fourdayWind.setText(f"Wind speed: {get_fourday[1]}")
            self.fourdayHumi.setText(f"Humidity: {get_fourday[2]}")

    def currentLoc(self):
        current_city = get_city()
        if current_city:
            self.citySearch.setText(current_city)
            self.update_weather(current_city)
        else:
            print("Failed to fetch current location.")

    def insert_weatherDB(self, city, weather_data):
        try:
            conn = sqlite3.connect('weather.db')
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS weather (
                    date TEXT PRIMARY KEY,
                    city TEXT NOT NULL,
                    temperature TEXT NOT NULL,
                    wind TEXT NOT NULL,
                    humidity TEXT NOT NULL
                )
            ''')
            conn.commit()

            date = today_date()
            temp = str(weather_data['main']['temp'])
            wind = str(weather_data['wind']['speed'])
            humidity = str(weather_data['main']['humidity'])

            c.execute('''
                INSERT OR REPLACE INTO weather (date, city, temperature, wind, humidity) 
                VALUES (?, ?, ?, ?, ?)
            ''', (date, city, temp, wind, humidity))

            conn.commit()
            print(f"Inserted/Updated weather data into DB for {city}")


        except Exception as e:
            print(f"Error: {e}")
        conn.close()


app = QApplication(sys.argv)
window = WeatherApp()
window.show()
sys.exit(app.exec())

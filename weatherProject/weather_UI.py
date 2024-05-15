import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.uic import loadUi
from request_weather import *
from date_weather import *
from currentLocation import get_city

API_KEY = "<API KEY>"

class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("weather.ui", self)  # Load the UI file into the QMainWindow
        self.setWindowTitle("Weather Program")
        self.cityName.setStyleSheet("color: black; font-weight: bold; font-size: 20px;")
        self.citySearch.setStyleSheet("color:black; font-size: 18px0;")
        self.searchButton.setStyleSheet("background-color: #5372F0; border-radius: 10px;")
        self.currLocation.setStyleSheet("background-color: rgb(168, 168, 168); border-radius: 10px;")
        self.weatherDate.setStyleSheet("color: #ffffff; font-weight: bold; font-size:18px;")
        self.weatherDate.setText(f"Tbilisi({today_date()})")
        self.set_icon("Icons/weather.png")
        self.mainIcon.setFixedSize(50, 35)
        self.searchButton.clicked.connect(self.set_temperature)
        self.searchButton.clicked.connect(self.set_wind_speed)
        self.searchButton.clicked.connect(self.set_humidity)
        self.searchButton.clicked.connect(self.set_cityName)
        self.searchButton.clicked.connect(self.tomorrow_forecast)
        self.searchButton.clicked.connect(self.twoday_forecast)
        self.searchButton.clicked.connect(self.threeday_forecast)
        self.searchButton.clicked.connect(self.fourday_forecast)
        self.currLocation.clicked.connect(self.currentLoc)
        self.initialize_default()
    def set_icon(self, path):
        pixmap = QPixmap(path)
        self.mainIcon.setPixmap(pixmap)

    def initialize_default(self):
        weather_data = self.fetch_weather("Tbilisi")
        if weather_data:
            self.weatherTemp.setText(f'Temperature: {get_temperature(weather_data)}°C')
            self.weatherWind.setText(f'Wind Speed: {get_wind_speed(weather_data)}')
            self.weatherHum.setText(f'Humidity: {get_humidity(weather_data)}')

            icon_code = weather_data['weather'][0]['icon']
            set_ic = get_local_icon(icon_code)
            self.set_todayIcon(set_ic)
            self.set_tomorrowIcon(set_ic)
            self.set_twoday_icon(set_ic)
            self.set_threeday_icon(set_ic)
            self.set_fourday_icon(set_ic)
    def set_todayIcon(self, path):
        pixmap = QPixmap(path)
        return self.todayIcon.setPixmap(pixmap)

    def set_twoday_icon(self, path):
        pixmap = QPixmap(path)
        return self.twodayIcon.setPixmap(pixmap)

    def set_threeday_icon(self, path):
        pixmap = QPixmap(path)
        return self.threedayIcon.setPixmap(pixmap)

    def set_fourday_icon(self, path):
        pixmap = QPixmap(path)
        return self.fourdayIcon.setPixmap(pixmap)

    def set_tomorrowIcon(self, path):
        pixmap = QPixmap(path)
        return self.tomorrowIcon.setPixmap(pixmap)

    def search_clicked(self):
        city_name = self.citySearch.text()
        # print("City Name: " + city_name)
        return city_name

    def fetch_weather(self, city_name):
        response = fetch_weather(API_KEY, city_name)
        if response:
            return response
        else:
            print("Failed to fetch weather data.")

    def set_temperature(self):
        city_name = self.search_clicked()
        weather_data = self.fetch_weather(city_name)
        icon_code = weather_data['weather'][0]['icon']
        set_ic = get_local_icon(icon_code)
        if weather_data:
            temperature = get_temperature(weather_data)
            # print("Temperature:", temperature)
            self.weatherTemp.setText(f"Temperature: {temperature:.1f} °C")
            self.set_todayIcon(set_ic)
        else:
            print("Failed to fetch weather data.")

    def set_wind_speed(self):
        city_name = self.search_clicked()
        weather_data = self.fetch_weather(city_name)
        if weather_data:
            wind_speed = get_wind_speed(weather_data)
            print("Wind speed:", wind_speed)
            self.weatherWind.setText(f"Wind: {wind_speed} m/s")
        else:
            print("Failed to get wind speed")

    def set_humidity(self):
        city_name = self.search_clicked()
        weather_data = self.fetch_weather(city_name)
        if weather_data:
            humidity = get_humidity(weather_data)
            # print("Humidity:", humidity)
            self.weatherHum.setText(f"Humidity: {humidity} %")
        else:
            print("Failed to fetch humidity.")

    def set_cityName(self):
        city_name = self.search_clicked()
        weather_data = self.fetch_weather(city_name)
        weather = today_date()
        if weather_data:
            city_name = city_name[0].upper() + city_name[1:]
            # print(weather)
            self.weatherDate.setText(f"{city_name}({weather})")


        else:
            print("Something gone wrong")

    def tomorrow_forecast(self):
        city_name = self.search_clicked()
        weather_data = self.fetch_weather(city_name)
        tomorrow = tomorrow_date()
        get = fetch_forecast(API_KEY, city_name)
        get_tomorrow = get_tomorrow_forecast(get)
        icon_code = weather_data['weather'][0]['icon']
        set_ic = get_local_icon(icon_code)
        if weather_data:
            self.set_tomorrowIcon(set_ic)
            self.tomorrowDate.setText(f"{tomorrow}")
            self.tomorrowTemp.setText(f"Temperature: {get_tomorrow[0]}")
            self.tomorrowWind.setText(f"Wind Speed: {get_tomorrow[1]}")
            self.tomorrowHumidity.setText(f"Humidity: {get_tomorrow[2]}")

    def twoday_forecast(self):
        city_name = self.search_clicked()
        weather_data = self.fetch_weather(city_name)
        get_date = twoday_date()
        get = fetch_forecast(API_KEY, city_name)
        get_twoday = get_twoday_forecast(get)
        icon_code = weather_data['weather'][0]['icon']
        set_ic = get_local_icon(icon_code)
        if weather_data:
            self.set_twoday_icon(set_ic)
            self.twoDayForecast.setText(get_date)
            self.twodayTemp.setText(f"Temperature: {get_twoday[0]}")
            self.twodayWind.setText(f"Wind Speed: {get_twoday[1]}")
            self.twodayHumi.setText(f"Humidity: {get_twoday[2]}")

    def threeday_forecast(self):
        city_name = self.search_clicked()
        weather_data = self.fetch_weather(city_name)
        get_date = threeday_date()
        get = fetch_forecast(API_KEY, city_name)
        get_threeday = get_threeday_forecast(get)
        icon_code = weather_data['weather'][0]['icon']
        set_ic = get_local_icon(icon_code)
        if weather_data:
            self.set_threeday_icon(set_ic)
            self.threedayDate.setText(get_date)
            self.threedayTemp.setText(f"Temperature: {get_threeday[0]}")
            self.threedayWind.setText(f"Wind speed: {get_threeday[1]}")
            self.threedayHumi.setText(f"Humidity: {get_threeday[2]}")

    def fourday_forecast(self):
        city_name = self.search_clicked()
        weather_data = self.fetch_weather(city_name)
        get_date = fourthday_date()
        get = fetch_forecast(API_KEY, city_name)
        get_fourday = get_fourday_forecast(get)
        icon_code = weather_data['weather'][0]['icon']
        set_ic = get_local_icon(icon_code)
        if weather_data:
            self.set_fourday_icon(set_ic)
            self.fourdayDate.setText(get_date)
            self.fourdayTemp.setText(f"Temperature: {get_fourday[0]}")
            self.fourdayWind.setText(f"Wind speed: {get_fourday[1]}")
            self.fourdayHumi.setText(f"Humidity: {get_fourday[2]}")

    def currentLoc(self):
        # Fetch current location
        current_city = get_city()
        if current_city:
            # Call all functions with the current city
            self.citySearch.setText(current_city)
            self.set_temperature()
            self.set_wind_speed()
            self.set_humidity()
            self.set_cityName()
            self.tomorrow_forecast()
            self.twoday_forecast()
            self.threeday_forecast()
            self.fourday_forecast()
        else:
            print("Failed to fetch current location.")







app = QApplication(sys.argv)
window = WeatherApp()
window.show()
sys.exit(app.exec())

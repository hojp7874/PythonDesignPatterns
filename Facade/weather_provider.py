from datetime import datetime, timedelta
import json
import pickle
from urllib.parse import quote
from urllib.request import urlopen

from secret import OPENWEATHERMAP_API_KEY


class WeatherProvider:
    def __init__(self):
        self.api_url = (
            "http://api.openweathermap.org/data/2.5/forecast?q={},{}&appid="
            + OPENWEATHERMAP_API_KEY
        )

    def get_weather_data(self, city, country):
        city = quote(city)
        url = self.api_url.format(city, country)
        return urlopen(url).read()


class Parser:
    def parse_weather_data(self, weather_data):
        parsed = json.loads(weather_data)
        start_date = None
        result = []

        for data in parsed["list"]:
            date = datetime.strptime(data["dt_txt"], "%Y-%m-%d %H:%M:%S")
            start_date = start_date or date
            if start_date.date() != date.date():
                return result
            result.append(data["main"]["temp"])


class Cache:
    def __init__(self, filename):
        self.filename = filename

    def save(self, obj):
        with open(self.filename, "wb") as file:
            dct = {"obj": obj, "expired": datetime.utcnow() + timedelta(hours=3)}
            pickle.dump(dct, file)

    def valid(self):
        try:
            with open(self.filename, "rb") as file:
                result = pickle.load(file)
                if result["expired"] > datetime.utcnow():
                    return result["obj"]
        except IOError as e:
            print(f"Warning: {e}")


class Converter:
    def from_kelvin_to_celcius(self, kelvin):
        return kelvin - 273.15


class Weather:
    def __init__(self, data):
        result = 0
        for r in data:
            result += r
        self.temperature = result / len(data)


class Facade:
    def get_forecast(self, city, country):
        cache = Cache("temp_cache")

        cache_valid = cache.valid()

        if cache_valid:
            return cache_valid
        weather_provider = WeatherProvider()
        weather_data = weather_provider.get_weather_data(city, country)

        parser = Parser()
        parsed_data = parser.parse_weather_data(weather_data)

        weather = Weather(parsed_data)
        converter = Converter()
        temperature_celcius = converter.from_kelvin_to_celcius(weather.temperature)

        cache.save(temperature_celcius)
        return temperature_celcius


if __name__ == "__main__":
    facade = Facade()
    print(facade.get_forecast("Seoul", "KR"))

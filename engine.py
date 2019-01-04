
# -------------------------------------------------------
# Classes and Functions
# -------------------------------------------------------

class Location():
    def __init__(self, location, lat=0, lon=0):
        self.location = location
        self.lat = lat
        self.lon = lon


    def get_location_data(self):
        import requests
        endpoint = "https://api.openweathermap.org/data/2.5/weather"
        payload = {"q": self.location, "units": "metric", "appid": "8abc5d58f8bc6938127c1aa207676c26"}
        response = requests.get(endpoint, params=payload)
        data = response.json()
        if response.status_code == 200 :
            return self.fetch_weather(data)
        else:
            return response.status_code


    def get_ip_data(self):
        import requests
        endpoint = "https://api.openweathermap.org/data/2.5/weather"
        payload = {"lat": self.lat, "lon": self.lon, "units": "metric", "appid": "8abc5d58f8bc6938127c1aa207676c26"}
        response = requests.get(endpoint, params=payload)
        data = response.json()
        return self.fetch_weather(data)


    def fetch_weather(self, data):
        forecast = dict()

        forecast['temperature'] = round(data['main']['temp'])
        forecast['location'] = data['name']
        forecast['weather'] = self.convert_weather(data['weather'][0]['description'])
        forecast['icon'] = data['weather'][0]['icon']

        forecast['min'] = data['main']['temp_min']
        forecast['max'] = data['main']['temp_max']

        from datetime import datetime
        sunrise = data['sys']['sunrise']
        sunset = data['sys']['sunset']
        forecast['sunrise'] = datetime.fromtimestamp(int(sunrise)).strftime('%H:%M')
        forecast['sunset'] = datetime.fromtimestamp(int(sunset)).strftime('%H:%M')

        return forecast


    def convert_weather(self, description):
        """
        Using a dictionary to create a switch statement alternative
        """
        conditions = {
            'clear sky': 'clear',
            'few clouds': 'clouds with some sunshine',
            'scattered clouds': 'cloudy',
            'broken clouds': 'cloudy',
            'shower rain': 'showers',
            'thunderstorm': 'thunder and lightning',
            'mist': 'fog'
        }

        if description in conditions:
            return conditions.get(description, "Look out of the window.")
        else:
            return description

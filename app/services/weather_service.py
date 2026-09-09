import requests
import os
from datetime import datetime

class WeatherService:
    BASE_URL = 'https://api.openweathermap.org/data/2.5'
    
    @classmethod
    def get_current_weather(cls):
        """Fetch current weather from OpenWeatherMap"""
        api_key = os.getenv('OPENWEATHER_API_KEY')
        city = os.getenv('OPENWEATHER_CITY', 'Colombo,LK')
        
        if not api_key:
            return cls._get_mock_weather()
        
        try:
            # Current weather
            url = f"{cls.BASE_URL}/weather"
            params = {
                'q': city,
                'appid': api_key,
                'units': 'metric'
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                'condition': data['weather'][0]['description'].capitalize(),
                'temp': data['main']['temp'],
                'wind_speed': data['wind']['speed'],
                'humidity': data['main']['humidity'],
                'updated_at': datetime.utcnow().isoformat()
            }
        except Exception as e:
            print(f"Weather API error: {e}")
            return cls._get_mock_weather()
    
    @classmethod
    def get_forecast(cls):
        """Fetch 5-day forecast from OpenWeatherMap"""
        api_key = os.getenv('OPENWEATHER_API_KEY')
        city = os.getenv('OPENWEATHER_CITY', 'Colombo,LK')
        
        if not api_key:
            return cls._get_mock_forecast()
        
        try:
            url = f"{cls.BASE_URL}/forecast"
            params = {
                'q': city,
                'appid': api_key,
                'units': 'metric',
                'cnt': 5  # 5 data points (3-hour intervals)
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            forecast = []
            for item in data['list'][:5]:  # Take first 5 entries
                forecast.append({
                    'day': datetime.fromtimestamp(item['dt']).strftime('%a'),
                    'temp': round(item['main']['temp']),
                    'condition': item['weather'][0]['description'].capitalize()
                })
            return forecast
        except Exception as e:
            print(f"Forecast API error: {e}")
            return cls._get_mock_forecast()
    
    @staticmethod
    def _get_mock_weather():
        """Fallback mock data when API fails"""
        return {
            'condition': 'Sunny',
            'temp': 26,
            'wind_speed': 12,
            'humidity': 60,
            'updated_at': datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def _get_mock_forecast():
        return [
            {'day': 'Mon', 'temp': 25, 'condition': 'Sunny'},
            {'day': 'Tue', 'temp': 22, 'condition': 'Cloudy'},
            {'day': 'Wed', 'temp': 24, 'condition': 'Partly cloudy'},
            {'day': 'Thu', 'temp': 26, 'condition': 'Sunny'},
            {'day': 'Fri', 'temp': 23, 'condition': 'Rainy'}
        ]
import requests

API_KEY = open('api_weather', 'r').read()
base_url = 'http://api.openweathermap.org/data/2.5/weather?'

def get_data(city):
    url = base_url + 'appid=' + API_KEY + '&q=' + city

    try:
        response = requests.get(url).json()
    except requests.exceptions.RequestException as e:
        return f'Ошибка запроса: {e}'

    if response.get('cod') == 200:
        temperatures = response['main']['temp'] - 273.15
        feels = response['main']['feels_like'] - 273.15
        humidity = response['main']['humidity']
        wind_speed = response['wind']['speed']
        wind_deg = response['wind']['deg']
        clouds = response['clouds']['all']
        return f'Температура: {int(temperatures)}°C, ощущается как: {int(feels)}°C'
    
    elif response.get('cod') == '404' or response.get('message') == 'city not found':
        return 'Город не найден. Проверьте название.'
    
    else:
        return f"Ошибка: {response.get('message', 'Неизвестная ошибка')}"
import requests

def get_weather(city_name):
    OWKey = ""
    geoCodingURL = "http://api.openweathermap.org/geo/1.0/direct?q={}&appid={}".format(city_name, OWKey)
    response = requests.get(geoCodingURL)
    responseDict = response.json()

    if response.status_code == 200:
        lat = responseDict[0]['lat']
        lon = responseDict[0]['lon']
        currentWeatherURL = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(lat, lon, OWKey)
        responseWeather = requests.get(currentWeatherURL)
        responseWeatherDict = responseWeather.json()

        if responseWeather.status_code == 200:
            weatherDescription = responseWeatherDict['weather'][0]['description']
            return weatherDescription
            #print(weatherDescription)
        else:
            print('[!] HTTP {0} calling [{1}]'.format(response.status_code, currentWeatherURL))
    else:
        print('[!] HTTP {0} calling [{1}]'.format(response.status_code, geoCodingURL))
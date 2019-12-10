import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime

currentDate = datetime.date.today()
stringDate = currentDate.strftime("%d %b %Y")

thePage = requests.get("http://www.bahrainweather.gov.bh/")
newSoup = BeautifulSoup(thePage.content, "html.parser")
today = newSoup.find(id= "hourly")
box = today.find_all(class_="i")

weather_times = [item.find(class_="time j-time with-zeros").get_text() for item in box] #This gets the time
weather_status = []
for item in box:
    a = item.find(class_="status").get_text()
    b = list(a)
    b.pop(-1)
    c = "".join(b)
    weather_status.append(c)
weather_temperatures = [i['data-temp'] for i in today.find_all('div', {'class':'temperature j-temp'})] #This tells the temprature
weather_directions = [item.find(class_="direction-badge").get_text() for item in box] #This tells the wind direction
weather_kt = [i['data-wind-speed'] for i in today.find_all('div', {'class':'wind-speed j-wind-speed'})] #This tells the wind level
weather_forecast = pd.DataFrame({"Time":weather_times, "Status": weather_status, "Temperature(°C)": weather_temperatures, "Wind Direction": weather_directions, "kt": weather_kt,})

print("\nTodays Weather forecast("+stringDate+"):")
print(weather_forecast)
print("Retrieved from http://www.bahrainweather.gov.bh/")
print()
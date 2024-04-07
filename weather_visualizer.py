# https://beta.meteo.lt/?pid=archyvas

import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def date_to_str(date):
    return date.strftime('%Y-%m-%d')


def fetch_temperature_for_date(date):
    formatted_date = date_to_str(date)
    url = f'https://beta.meteo.lt/?pid=archyvas&station=vilniaus-ams&date={formatted_date}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = soup.find_all('tr')
    midday_temp = None
    for row in rows:
        cells = row.find_all('td')
        if cells and cells[0].get_text().strip() == '12:00':
            midday_temp = cells[1].text.strip()
            break

    return midday_temp

print('Only contains data from 2014-04-07 to current date')
start_date_str = input('Enter the start date (YYYY-MM-DD): ')
end_date_str = input('Enter the end date (YYYY-MM-DD): ')

start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

temp_data = {}

while start_date <= end_date:
    temp = fetch_temperature_for_date(start_date)
    if temp:
        temp_data[date_to_str(start_date)] = float(temp.replace('°C', '').replace(',', '.').strip())
    else:
        print(f"No data for {date_to_str(start_date)}")
    start_date += timedelta(days=1)

dates = list(temp_data.keys())
temperatures = list(temp_data.values())

plt.figure(figsize=(10, 5), dpi=200)
plt.plot(dates, temperatures, marker='o', linestyle='-', color='b')
plt.title('Midday Temperature in Vilnius')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

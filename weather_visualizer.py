# https://beta.meteo.lt/?pid=archyvas

import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
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

dates = [datetime.strptime(date, '%Y-%m-%d') for date in temp_data.keys()]
temperatures = list(temp_data.values())

plt.figure(figsize=(15, 7), dpi=200)
plt.plot(dates, temperatures, marker='o', linestyle='-', color='royalblue', markersize=5)

plt.title('Average Midday Temperature in Vilnius', fontsize=16, fontweight='bold')
plt.xlabel('Year', fontsize=14)
plt.ylabel('Temperature (°C)', fontsize=14)

plt.grid(True, which='both', linestyle='--', linewidth=0.5)

plt.gca().xaxis.set_major_locator(mdates.YearLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.gca().xaxis.set_minor_locator(mdates.MonthLocator())

plt.gca().tick_params(axis='x', which='major', labelsize=12)
plt.gca().tick_params(axis='x', which='minor', labelsize=8)
plt.setp(plt.gca().get_xticklabels(), rotation=45, ha="right")

plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True, nbins=10))

plt.tight_layout()
plt.savefig('C:/Users/aivar/Desktop/temperature_plot.png', dpi=300)
plt.show()

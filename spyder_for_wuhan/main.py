import requests
from bs4 import BeautifulSoup
import pandas as pd
import folium
import re


def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        raise Exception('Error fetching data from the URL')


def extract_data(soup):
    data = {'country': [], 'total_cases': [], 'new_cases': [], 'total_deaths': [], 'new_deaths': [],
            'total_recovered': [], 'active_cases': []}
    table = soup.find('table', {'id': 'main_table_countries_today'})

    for row in table.tbody.find_all('tr'):
        cells = row.find_all('td')
        country = cells[1].get_text().strip()
        if country == 'China':
            data['country'].append(country)
            data['total_cases'].append(cells[2].get_text().strip())
            data['new_cases'].append(cells[3].get_text().strip())
            data['total_deaths'].append(cells[4].get_text().strip())
            data['new_deaths'].append(cells[5].get_text().strip())
            data['total_recovered'].append(cells[6].get_text().strip())
            data['active_cases'].append(cells[8].get_text().strip())

    df = pd.DataFrame(data)
    return df


def visualize_data(df, location: list):  # 根据地址和数据进行在地图上进行标记
    map = folium.Map(location=location, zoom_start=5)  # Wuhan's coordinates

    for index, row in df.iterrows():
        country = row['country']
        total_cases = row['total_cases']
        total_deaths = row['total_deaths']
        total_recovered = row['total_recovered']
        active_cases = row['active_cases']

        popup_text = f"<b>Country:</b> {country}<br><b>Total Cases:</b> {total_cases}<br><b>Total Deaths:</b> {total_deaths}<br><b>Total Recovered:</b> {total_recovered}<br><b>Active Cases:</b> {active_cases}"
        folium.Marker([30.5928, 114.3055], popup=folium.Popup(popup_text, max_width=300)).add_to(map)

    map.save('epidemic_map.html')


if __name__ == '__main__':
    url = 'https://www.worldometers.info/coronavirus/'
    soup = fetch_data(url)
    df = extract_data(soup)
    visualize_data(df, [30.5928, 114.3055])

    print("Epidemic map has been created successfully.")

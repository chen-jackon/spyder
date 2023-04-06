import requests
from bs4 import BeautifulSoup
import pandas as pd
import folium
from branca.element import Figure

DATA_SOURCE_URL = 'https://www.worldometers.info/coronavirus/'


def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        raise Exception('Error fetching data from the URL')


def extract_data(soup):
    data = {'street': [], 'date': [], 'daily_cases': [], 'latitude': [], 'longitude': []}
    # Modify the following lines based on the structure of your data source
    for row in soup.find_all('some_element'):
        data['street'].append(row.some_attribute)
        data['date'].append(row.some_attribute)
        data['daily_cases'].append(row.some_attribute)
        data['latitude'].append(row.some_attribute)
        data['longitude'].append(row.some_attribute)

    df = pd.DataFrame(data)
    return df


def visualize_data(df):
    fig = Figure()
    map = folium.Map(location=[30.5928, 114.3055], zoom_start=12)
    fig.add_child(map)

    date_picker_html = '''
    <link rel="stylesheet" href="https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
    <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
    <div style="position:fixed; top:10px; left:50px; width:180px; z-index:9999; background:white; padding:5px; border:1px solid black;">
    <input type="text" id="datepicker" style="width:100%;">
    </div>
    <script>
    $("#datepicker").datepicker({
        dateFormat: "yy-mm-dd",
        onSelect: function(date) {
            let selected_date = date.replaceAll('-', '');
            displayMarkers(selected_date);
        }
    });
    </script>
    '''
    fig.add_child(folium.Element(date_picker_html))

    marker_data = {}
    for _, row in df.iterrows():
        date = row['date'].replace('-', '')
        if date not in marker_data:
            marker_data[date] = []
        marker_data[date].append({
            'street': row['street'],
            'daily_cases': row['daily_cases'],
            'latitude': row['latitude'],
            'longitude': row['longitude'],
        })
    display_markers_js = f'''
    <script>
    let marker_data = {marker_data};
    let markers = {{}};
    function displayMarkers(date) {{
        for (let group in markers) {{
            markers[group].remove();
        }}
        if (date in marker_data) {{
            markers[date] = L.featureGroup();
            for (let i = 0; i < marker_data[date].length; i++) {{
                let lat = marker_data[date][i].latitude;
                let lon = marker_data[date][i].longitude;
                let street = marker_data[date][i].street;
                let daily_cases = marker_data[date][i].daily_cases;
                let popup_text = `<b>Street:</b> ${{street}}<br><b>Date:</b> ${{date}}<br><b>Daily Cases:</b> ${{daily_cases}}`;
                let marker = L.marker([lat, lon], {{}}).bindPopup(popup_text);
                markers[date].addLayer(marker);
            }}
            markers[date].addTo(map);
        }}
    }}
    </script>
    '''

    fig.add_child(folium.Element(display_markers_js))

    fig.save('street_level_map_with_date.html')


if __name__ == '__main__':
    soup = fetch_data(DATA_SOURCE_URL)
    df = extract_data(soup)
    visualize_data(df)
    print("Street-level epidemic map with date picker has been created successfully.")

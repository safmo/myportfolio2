import pandas as pd
import folium
import json
import requests
import webbrowser

def main():
    sensors = []
    with open('sensors.csv', 'r') as f:
        csv_file = pd.read_csv(f)
        for _, row in csv_file.iterrows():
            sensors.append([row['latitude'], row['longitude'], row['sensor_name'], row['app_id'], row['dev_id'], row['status'], row['additional_details']])

    # Skapa karta
    m = folium.Map(location=[60.48746, 15.409658], zoom_start=6)

    # Sensorfärger
    colors = {
        'Elsys ELT2': 'blue',
        'Elsys ERS CO2': 'red',
        'ESP32': 'orange',
        'Arduino': 'purple'
    }

    # Lägg till sensorer på kartan
    for sensor in sensors:
        color = colors.get(sensor[2], 'gray')
        tooltip = f'app_id: {sensor[3]}, dev_id: {sensor[4]}'
        popup = folium.Popup(f'Status: {sensor[5]}, Sensors: {sensor[6]}', max_width=250)

        folium.Marker(
            location=sensor[:2],
            tooltip=tooltip,
            popup=popup,
            icon=folium.Icon(color=color, icon='info-sign')
        ).add_to(m)

    # **Första TTN API**: Gateways i hela Sverige
    url_sweden = 'https://www.thethingsnetwork.org/api/v2/gateways?country=SE'
    response_sweden = requests.get(url_sweden)

    if response_sweden.status_code == 200:
        sweden_data = response_sweden.json()
        for gateway in sweden_data:
            lat, lng = gateway['location']['latitude'], gateway['location']['longitude']
            folium.Marker(
                location=[lat, lng],
                tooltip=f"Gateway ID: {gateway['id']}",
                popup=f"Latitude: {lat}, Longitude: {lng}",
                icon=folium.Icon(color='green', icon='wifi')
            ).add_to(m)
    else:
        print("Fel vid hämtning av gateways i Sverige")

    # **Andra TTN API**: Gateways inom 200 km från Borlänge
    url_borlange = 'https://www.thethingsnetwork.org/gateway-data/location?latitude=60.48746&longitude=15.40965&distance=200000'
    response_borlange = requests.get(url_borlange)

    if response_borlange.status_code == 200:
        borlange_data = response_borlange.json()
        for gateway_id, data in borlange_data.items():
            lat, lng = data['location']['latitude'], data['location']['longitude']
            folium.Marker(
                location=[lat, lng],
                tooltip=f'Gateway ID: {gateway_id}',
                popup=f'Latitude: {lat}, Longitude: {lng}',
                icon=folium.Icon(color='darkblue', icon='wifi')
            ).add_to(m)
    else:
        print("Fel vid hämtning av gateways nära Borlänge")

    # **Legend**
    legend_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; width: 200px; height: 220px; border:2px solid grey; z-index:9999;padding: 10px;">
        <b>Legend</b><br>
        <i class="fa fa-wifi fa-2x" style="color:green"></i> Gateways<br>
        <i class="fa fa-map-marker fa-2x" style="color:blue"></i> Elsys ELT2<br>
        <i class="fa fa-map-marker fa-2x" style="color:red"></i> Elsys ERS CO2<br>
        <i class="fa fa-map-marker fa-2x" style="color:orange"></i> ESP32<br>
        <i class="fa fa-map-marker fa-2x" style="color:purple"></i> Arduino<br>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # **Spara och öppna kartan**
    m.save('sensors_gateways.html')
    webbrowser.open_new_tab('sensors_gateways.html')

if __name__ == "__main__":
    main()

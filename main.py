from flask import Flask, jsonify, render_template
import requests
import math
app=Flask(__name__)
@app.route('/')
def root():
   return render_template('index.html')
@app.route('/markers')
def generateMarkers():
   url = "https://radar.joshdouch.me/data/aircraft.json" # aircraft.json
   response = requests.get(url)
   data = response.json()

   markers=[]

   for aircraft in data['aircraft']:
      # Check if the aircraft has both 'lat' and 'lon' values
      if 'lat' in aircraft and 'lon' in aircraft and 'track' in aircraft and 'flight' in aircraft:
         image_url_data = requests.get("https://hexdb.io/hex-image-thumb?hex=" + aircraft['hex'])
         image_url = image_url_data.text
         aircraft_info = requests.get("https://hexdb.io/api/v1/aircraft/" + aircraft['hex'])
         aircraft_data = aircraft_info.json()
         route_info = requests.get("https://hexdb.io/api/v1/route/iata/" + aircraft['flight'].strip())
         route_data = route_info.json()
         if image_url == "n/a":
            image_url = "/static/img/image-unavailable.png"
         if "flight" in route_data:
            route_list = route_data['route'].split("-")
            if len(route_list) == 2:
               route_origin = route_list[0]
               route_destination = route_list[1]
            else:
               route_origin = route_list[0]
               route_destination = "N/A"
         else:
            route_origin = "N/A"
            route_destination = "N/A"
         # Create a new marker with the required data
         marker = {
            'lat': aircraft['lat'],
            'lon': aircraft['lon'],
            'hex': aircraft['hex'],
            'callsign': aircraft.get('flight', 'N/A').strip(),
            'squawk': aircraft.get('squawk', 'N/A').strip(),
            'track': aircraft['track'],
            'image': image_url,
            'airline': aircraft_data.get('RegisteredOwners', 'N/A'),
            'type': aircraft_data.get('Type', 'N/A'),
            'typeshort': aircraft_data.get('ICAOTypeCode', 'N/A'),
            'reg': aircraft_data.get('Registration', 'N/A'),
            'speed': aircraft.get('gs', 'N/A'),
            'altitude': aircraft.get('alt_baro', 'N/A'),
            'origin': route_origin,
            'destination': route_destination,
         }
         # Append the marker to the markers list
         markers.append(marker)
   return jsonify(markers)
if __name__ == '__main__':
   app.run(host="localhost", port=8080, debug=True)
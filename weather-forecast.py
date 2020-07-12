import requests
import re

locations = []
forecast_urls = []
temperatures = []
input_file = 'locations.txt'
output_file = 'Wednesday_night_temperatures.txt'

# read data from input file
with open(input_file, encoding='utf-8') as f: # decode file as utf-8
    for line in f:
        line = line.strip() # remove end of line whitespace characters like \n
        # validate string is non-empty and matches desired format for preprocessing
        if line and re.match('^(\d{1,2}([.]\d+)?°\s*[N,S]),\s*(\d{1,3}([.]\d+)?°\s*[E,W])$', line):
            print(line)
            lat_long = line.split(',')
            locations.append(lat_long)

# clean and preprocess data
for location in locations:
    latitude = location[0].split('°')
    longitude = location[1].split('°')

    # convert latitude and longitude to degree decimal format with postive and negative values
    if 'N' in latitude[1]:
        location[0] = float(latitude[0])
    else:
        location[0] = -1 * float(latitude[0])

    if 'E' in longitude[1]:
        location[1] = float(longitude[0])
    else:
        location[1] = -1 * float(longitude[0])

# send requests to weather API to retrieve forecast urls
for location in locations:
    url = 'https://api.weather.gov/points/{0},{1}'.format(location[0], location[1])
    response = requests.get(url)
    if response.ok:
        json_response = response.json()
        forecast_urls.append(json_response['properties']['forecast'])

# extract temperature for wednesday night
def extract_temperature(forecast_data):
    for dictionary in forecast_data:
        if 'Wednesday Night' in dictionary.values():
            return dictionary['temperature']
    return None

# send requests to weather API to retrieve forecast data
for url in forecast_urls:
    response = requests.get(url)
    if response.ok:
        json_response = response.json()
        temperatures.append(extract_temperature(json_response['properties']['periods']))

# write temperature data to text file
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(', '.join(str(i) for i in temperatures))
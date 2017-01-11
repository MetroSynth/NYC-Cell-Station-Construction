import urllib.request
import json
import csv
import pandas as pd
import numpy as np

class ReverseGeocoder:
    def __init__(self):
        """
        Converts Building Street and Borough entries into GPS coordinates.
        Uses Google GeoCode API
        """
    def setAPI(self,api):
        self.apiKey = api
        
    def sendQuery(self,address_string):
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'\
        .format(address_string,self.apiKey)
        print("\nAttempting to Query",url)
        response = urllib.request.urlopen(url)
        json_geocode = response.read().decode('utf-8')
        parsed_json = json.loads(json_geocode)
        lat = parsed_json['results'][0]['geometry']['location']['lat']
        long = parsed_json['results'][0]['geometry']['location']['lng']
        print(parsed_json['results'][0]['geometry'])
        print(lat,long)
        if "ZERO RESULTS" in parsed_json['results']:
            coords = ['invalid','invalid']
        else:
            coords = [lat,long]
        return coords

class CSVhandler:
    def __init__(self):
        """
        Handles the CSV dataset. Geocodes from addresses strings
        and resaves a file with a Lat and Long column added
        """
        self.borough_keys = {
        '1' : 'MANHATTAN',
        '2' : 'BRONX',
        '3' : 'BROOKLYN',
        '4' : 'QUEENS',
        '5' : 'STATEN+ISLAND',
        }
    
    def process(self,filename):
        """
        This is the core function of the CSV handler class
        """
        df = pd.read_csv(filename,header=0,error_bad_lines=False)
        geocode = ReverseGeocoder()
        #user needs to pass in their API-key as this function's argument
		geocode.setAPI()
        latitudes = []
        longitudes = []
        for i in df.index:
            borough = self.borough_keys[str(df['Borough'].iloc[i])]
            building = (df['House #'].iloc[i]).strip()
            street = (df['Street Name'].iloc[i]).strip()
            address = ('{}+{},+{},+NY').format(building,street,borough)
            address = address.replace(' ','+')
            coords = geocode.sendQuery(address)
            print("ROW NUMBER:",i,"ADDRESS:",(address.replace('+',' ')),"COORDINATES:",coords)
            latitudes.append(coords[0])
            longitudes.append(coords[1])
        df.insert(0,'Lat',latitudes)
        df.insert(1,'Long',longitudes)
        print('Coordinate Generation Complete')
        df.to_csv('./outfile.csv', sep=',')
    
def main():
    c = CSVhandler()
    c.process('./full_test.csv')

if __name__ == '__main__': main()
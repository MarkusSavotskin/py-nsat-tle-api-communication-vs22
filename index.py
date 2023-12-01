from flask import Flask
import requests
import ephem
import datetime
import json

# The API endpoint
host = "https://tle.ivanstanojevic.me/api/tle/"

app = Flask(__name__)

@app.route("/id/<satellite_id>")
def get_satelitte_by_id(satellite_id):
        
    # The API endpoint
    url = f"{host}{satellite_id}"


    # A GET request to the API
    response = requests.get(url)

    # Print the response
    response_json = response.json()
    print(response_json)
    
    try:
    
        tle_rec = ephem.readtle(response_json["name"], response_json["line1"], response_json["line2"])
        tle_rec.compute()
    
        print(response_json["name"] +  ":\n" + "Longitude: " + str(tle_rec.sublong) + "\nLatitude: " + str(tle_rec.sublat) + "\n")
    
        data = {"date": response_json["date"], "name": response_json["name"], "id": response_json["satelliteId"], "long": tle_rec.sublong, "lat": tle_rec.sublat}
    
        print(data)
        
    except:
        
        data = {"message": f"Unable to find record with id {satellite_id}"}            
    
    return data

@app.route("/all")
def get_satelittes():
    
    json = []

    # A GET request to the API
    response = requests.get(host)

    # Print the response
    response_json = response.json()
    print(response_json)
    
    try:

        for item in response_json["member"]:
            
            tle_rec = ephem.readtle(item["name"], item["line1"], item["line2"])
            tle_rec.compute()

            print(item["name"] +  ":\n" + "Longitude: " + str(tle_rec.sublong) + "\nLatitude: " + str(tle_rec.sublat) + "\n")
        
            data = {"date": item["date"], "name": item["name"], "id": item["satelliteId"], "long": tle_rec.sublong, "lat": tle_rec.sublat}
            json.append(data)
            
    except:
        
        json = {"message": "Something went wrong"} 
       
    print(json)
    
    return json

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8008)

from flask import Flask, jsonify
from flask_cors import CORS
import json
import ChripstackSimulator

app = Flask(__name__)
CORS(app)  # ALLOWS CORS TO EVERY ROUTES

dailyDataRoute='dailyElectric.txt' #route for the file that contains last day data only
historicDataRoute= 'dataHistoric.txt' #route for the file that contain all the historic data

parsedDataRoute= 'dataParsed.txt' #route for the file that contains last day data only, in a completly legible Json format

def proccesFile(currentRoute): #This function will save a parsed copy of the txt file parameter (could be historic or daily) into the parsed txt file
  ChripstackSimulator.simulateChirpstack() #neccesary if is electric data, this will fill the electric txt files from the UtilityDailyRegister
  with open(currentRoute, 'r') as dataFile:
    measurementsSTR = dataFile.read() 
    measurementsSTR = '[' + measurementsSTR[0:-2] + ']'  #change the format, adding the items into a list (represented by "[]") and deleting the final comma. This is neccesary to make the Json legible for angular
    dataFile.close()
  with open (parsedDataRoute, 'w') as parsedFile:
     parsedFile.write (measurementsSTR) #file.write cleans the entire parsedFile and write the measurementsSTR varaible only
     parsedFile.close()

def get_data(): #
    """This function will use the dataParsed file (that have been changed before in the proccesfile function to have 
    daily or historic data) to get data and then return a json with only the needed information for angular,  
     also, this function will be group the measurements per device, to return a list of devices with its measurements insteand
      of  a list of measurements only """

    devices=[]

    with open('dataParsed.txt', 'r') as file:
      measurements = json.load(file) #measurements has now the content of the dataParsedFile
    
    for currentMeasurement in measurements:
      currentDevEUI = currentMeasurement["devEUI"]
      json_obj = json.loads(currentMeasurement["objectJSON"])

      if not any(device["id"] == currentDevEUI for device in devices):
          # this add the device of the current measurement only if the current measurement is from a device that isn't in the list
          
          measurementsAuxiliar=[] #this auxiliar list of diccionaries will help us to  add all measurements
          i=1
          for key, value in json_obj.items():
             if key != "gpsLocation":
                measurementsAuxiliar.append({"measurementsName": key, 
                                             "measurementsValues":[{  "name": currentMeasurement["publishedAt"],
                                                                      "value": value[str(i)]  }]
                                              })
                i+=1

          devices.append( {"id": currentDevEUI, 
                          "name": currentMeasurement["deviceName"],
                          "latitude": json_obj["gpsLocation"][str(i)]["latitude"],
                          "longitude": json_obj["gpsLocation"][str(i)]["longitude"],
                          "icon": "http://maps.google.com/mapfiles/ms/icons/red-dot.png",
                          "allMeasurements": measurementsAuxiliar  
                            }
                          )
          
      else: #if the device is already in the list, we add only the measurement's data (not the device's data)
         for device in devices:
            if device["id"]== currentDevEUI:
               nameMeasurementExist= False
               for key, value in json_obj.items():
                  i=1
                  j=0
                  while j< len(device["allMeasurements"]):
                     if key==device["allMeasurements"][j]["measurementsName"]:
                      nameMeasurementExist= True
                      device["allMeasurements"][j]["measurementsValues"].append({
                                                        "name": currentMeasurement["publishedAt"],
                                                        "value": value[str(j+1)]
                                                        })
                     j+=1
                  if nameMeasurementExist==False:
                     device["allMeasurements"].append({"measurementsName": key, 
                                             "measurementsValues":[{  "name": currentMeasurement["publishedAt"],
                                                                      "value": value[str(i)]  }]
                                              })
                  i+=1

    return jsonify(devices)

@app.route('/daily', methods=['GET'])
def get_daily_data():
   proccesFile(dailyDataRoute)
   return get_data()

@app.route('/historic', methods=['GET']) 
def get_historic_data():
   proccesFile(historicDataRoute) 
   return get_data()
   

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')

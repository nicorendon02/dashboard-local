from datetime import datetime
import json 

def simulateChirpstack():
    
    with open('UtilityDailyRegisters.txt', 'r') as file: #open the file
        with open( 'dailyElectric.txt', 'a') as targetFile:

            while(True): 
                from datetime import datetime

                firstLine = file.readline()  # read date and skip
                if firstLine == '':
                    break

                date = firstLine
                # Next lines parse the date into an ISO format
                date = date[:22] + date[26+1:]
                date = date.strip().replace("p.", "PM")
                date = date.strip().replace("Â", "")

                # Try different formats
                formats = ["%d-%b-%y %I:%M:%S %p", "%m/%d/%Y %I:%M:%S %p"]
                parsed_date = None

                for fmt in formats:
                    try:
                        parsed_date = datetime.strptime(date, fmt)
                        break
                    except ValueError:
                        continue

                if parsed_date:
                    date = parsed_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                else:
                    print("Error: Date format does not match any known formats.")
        
                activePower=file.readline() # read active power
                activePower=activePower.split ("=") #this line and the following 2 lines are going to get de int value from the text
                activePower= activePower[1].split("\n")
                activePower= (float(activePower[0].strip().replace(",", ".")))

                #The same with the other variables, this  is repeated code, but is just for quickly test purposes :)
                reactivePower=file.readline() # read the next line, in this case will be active power
                reactivePower=reactivePower.split ("=") 
                reactivePower= reactivePower[1].split("\n")
                reactivePower= (float(reactivePower[0].strip().replace(",", ".")))

                current=file.readline() 
                current=current.split ("=") 
                current= current[1].split("\n")
                current= (float(current[0].strip().replace(",", ".")))

                voltage=file.readline()
                voltage=voltage.split ("=") 
                voltage= voltage[1].split("\n")
                voltage= (float(voltage[0].strip().replace(",", ".")))

                # Power Factor
                power_factor = file.readline()  
                power_factor = power_factor.split("=") 
                power_factor = power_factor[1].split("\n")
                power_factor=  power_factor[0].strip().replace(",", ".")
                power_factor = float(power_factor)

                # Apparent Power
                apparent_power = file.readline() 
                apparent_power = apparent_power.split("=") 
                apparent_power = apparent_power[1].split("\n")
                apparent_power = float(apparent_power[0].strip().replace(",", "."))
            
                file.readline() #skip quadrant for the moment

                # Analog Voltage
                analog_voltage = file.readline() 
                analog_voltage = analog_voltage.split("=") 
                analog_voltage = analog_voltage[1].split("\n")
                analog_voltage= analog_voltage[0].strip().replace(",", ".")
                analog_voltage = float(analog_voltage)

                # Thermistor Temperature
                thermistor_temperature = file.readline()  
                thermistor_temperature = thermistor_temperature.split("=") 
                thermistor_temperature = thermistor_temperature[1].split("\n")
                thermistor_temperature = float(thermistor_temperature[0].strip().replace(",", "."))

                # Active Energy Import
                active_energy_import = file.readline() 
                active_energy_import = active_energy_import.split("=") 
                active_energy_import = active_energy_import[1].split("\n")
                active_energy_import = float(active_energy_import[0].strip().replace(",", "."))

                # Active Energy Export
                active_energy_export = file.readline()
                active_energy_export = active_energy_export.split("=") 
                active_energy_export = active_energy_export[1].split("\n")
                active_energy_export = float(active_energy_export[0].strip().replace(",", "."))

                # Reactive Energy Import
                reactive_energy_import = file.readline()
                reactive_energy_import = reactive_energy_import.split("=") 
                reactive_energy_import = reactive_energy_import[1].split("\n")
                reactive_energy_import = float(reactive_energy_import[0].strip().replace(",", "."))

                # Reactive Energy Export
                reactive_energy_export = file.readline()  
                reactive_energy_export = reactive_energy_export.split("=") 
                reactive_energy_export = reactive_energy_export[1].split("\n")
                reactive_energy_export = float(reactive_energy_export[0].strip().replace(",", "."))

                # Minimum 1
                minimum_1 = file.readline() 
                minimum_1 = minimum_1.split("=") 
                minimum_1 = minimum_1[1].split("\n")
                minimum_1 = float(minimum_1[0].strip().replace(",", "."))

                # Maximum 1
                maximum_1 = file.readline() 
                maximum_1 = maximum_1.split("=") 
                maximum_1 = maximum_1[1].split("\n")
                maximum_1 = float(maximum_1[0].strip().replace(",", "."))

                # Minimum 2
                minimum_2 = file.readline()  
                minimum_2 = minimum_2.split("=") 
                minimum_2 = minimum_2[1].split("\n")
                minimum_2 = float(minimum_2[0].strip().replace(",", "."))

                # Maximum 2
                maximum_2 = file.readline() 
                maximum_2 = maximum_2.split("=") 
                maximum_2 = maximum_2[1].split("\n")
                maximum_2 = float(maximum_2[0].strip().replace(",", "."))

                newData= {"deviceName":"Walter Farm","devEUI":"JLOn7lPpYn9=" ,
                        "objectJSON":{"activePower": {"1": activePower},
                                        "reactivePower": {"2": reactivePower},
                                        "current": {"3": current},
                                        "voltage": {"4": voltage},
                                        "powerFactor": {"5": power_factor},
                                        "apparentPower": {"6": apparent_power},
                                        "analogVoltage": {"7": analog_voltage},
                                        "thermistorTemperature": {"8": thermistor_temperature},
                                        "activeEnergyImport": {"9": active_energy_import},
                                        "activeEnergyExport": {"10": active_energy_export},
                                        "reactiveEnergyImport": {"11": reactive_energy_import},
                                        "reactiveEnergyExport": {"12": reactive_energy_export},
                                        "minimum1": {"13": minimum_1},
                                        "maximum1": {"14": maximum_1},
                                        "minimum2": {"15": minimum_2},
                                        "maximum2": {"16": maximum_2},
                                        "gpsLocation":{"17":{"latitude":40.4376,"longitude":-86.9215,"altitude":0}},
                                    },
                        "publishedAt":date}
                
                newData["objectJSON"]= json.dumps(newData["objectJSON"])
                targetFile.write(json.dumps(newData) + "," + "\n")
                
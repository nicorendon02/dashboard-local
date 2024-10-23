import datetime
import time
import ChripstackSimulator

"""IMPORTANT
we have 2 formats for the txt files that contains data, we can call
the first "pre parsed" and the second is the "parsed" the diferences 
are that the preparsed has always one comma at the end, doesn´t hace
the "[]" that indicates that is a list and the value of json object is between
quotes (so python thinks that is a string) the parsed is completely legible
for python.

pre parsed example: {..."objectJson":"{...}"...},{..."objectJson":"{...}"...},
parsed example:     [{..."objectJson":{...}...} ,{..."objectJson":"{...}"...}]

the daily data is always in pre parsed format, for the moment 
the historic data is always in pre parsed format, but is desirable to change this
to be in parsed format everytime (making the api efficiently) 
"""
#IMPORTANT PARAMETERS: 
unsaveInterval= 5 #This means, for example, that we are going to delete 10 measurements, save 1, delete 10, save one, etc. Higher for better memory use, lower for keep more data
sleepTime=30 #frequency in seconds to do the clean and backup, some hours or daily recommended, but could be any time you want. In this case 21600 is 6 hours

dailyDataRoute='dailyElectric.txt' #route for the file that contains last day data only
historicDataRoute= 'dataHistoric.txt' #rute for the file that contain all the historic data
historicBackUpRoute= 'backUp' #route fro the backup files
utilityDailyRegistersRoute= 'UtilityDailyRegisters.txt' #Route where utility saves the files 

dailyBackUp=''
historicData= ''


while True:
    ChripstackSimulator.simulateChirpstack()
    #Save the daily data into a variable
    with open (dailyDataRoute, 'r') as dailyFile:
     with open (historicDataRoute, 'a') as historicDataFile:
        currentLine= dailyFile.readline()
        while currentLine!='': 
            for i in range (unsaveInterval-1):
               currentLine=dailyFile.readline()
               if currentLine=='':
                  break
               
            historicDataFile.write(currentLine)

    
    #clean the daily file
    with open (dailyDataRoute, 'w') as dailyBackUpFile:
     dailyBackUpFile.write ('') #file.write cleans the entire file and write the new varaible, in this case, an empty string

    #clean the daily file
    with open (utilityDailyRegistersRoute, 'w') as utilityFile:
     utilityFile.write ('') #file.write cleans the entire file and write the new varaible, in this case, an empty string

   #this part make a backUp,  saving one file per day in the folder setted before
    currentDate = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    newRoute = f"{historicBackUpRoute}/{currentDate}.txt"
    with open (newRoute, 'w') as historicBackUpfile:  #save a .txt file with the name of the current time
        historicBackUpfile.write(dailyBackUp)
        historicBackUpfile.close()

    print ("backup done")
    time.sleep (sleepTime) #Sleep for 86400 seconds, this is 24 hours


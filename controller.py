
import requests
import requests.auth
import time
import ssdp
from getImages import downloadImages
import keyboard
import re
import json

class Remote:
    def __init__(self):
        self.protocol = "http://"
        self.ip = "192.168.1.103"
        self.port = ":8060/"
        self.url = self.protocol + self.ip + self.port
    
    def scan(self):
        done = False
        while (not done):
            #scans the network for all roku tvs
            tvs = (ssdp.discover("roku:ecp"))
            counter = 0

            #empty dict intialized to dump to JSON later
            tvDict = {}

            #prints out all TVs found
            for tv in tvs:
                #regex to only have the IP adress of the TV
                tvIPaddr = re.search(r"[/]\d{3}.\d{3}.\d.\d*", str(tvs[counter]))
                tvIPaddr = tvIPaddr.group().strip("/")

                #GET request that receives lots of information but im only interested in the device name.
                deviceInfo = requests.get("http://"+tvIPaddr+":8060/query/device-info")
                #regex to single out the device name line
                deviceName = re.search(r"[u][s][e][r].*>\w*", str(deviceInfo.text))
                deviceName = deviceName.group()

                #find the index that is essentially the end of the device name
                endIndex   = deviceName.find("<")
                deviceName = deviceName[17:endIndex]

                #writes the name & ip addr to the dict
                tvDict[deviceName] = tvIPaddr


                counter += 1


            #dumps to json file
            with open(r'C:\Users\Chip\Documents\personalProjects\personalProjects\rokuController\tvNameAndIP.txt', 'w') as json_file:
                    json.dump(tvDict, json_file, indent=2)
            done = True
        


    def pressButton(self, button):
        requests.post(self.url + "/keypress/" + button)
    
    #gets all apps installed on the TV and dumps to JSON
    def getApps(self):
        #empty dict to dump to json file later
        appIDandName = {}
        
        apps  = requests.get(self.url+"/query/apps")
        #writes request to text file because its easier to parse the data line by line
        with open (r'C:\Users\Chip\Documents\personalProjects\personalProjects\rokuController\appInfo.txt', 'w') as f:
            f.write(apps.text)
            f.close()

        #opens text file to grab the appID and Name
        f = open(r"C:\Users\Chip\Documents\personalProjects\personalProjects\rokuController\appInfo.txt" , 'r')
        for line in f:
            appID = re.search(r'<app id="\d*"', line)
            appName = re.search(r">\w*\s?\w*", line)
            if(appID and appName):
                appID = appID.group()
                #starts at the correct index of the regex result and deletes quotation marks
                appID = appID[8:].replace('"', "")
                appName = appName.group().strip(">")
                appIDandName[appName] = appID
        
        with open (r"C:\Users\Chip\Documents\personalProjects\personalProjects\rokuController\appIDsAndNames.txt", 'w') as json_file:
            json.dump(appIDandName, json_file, indent=2)
    
    def getImages(self):
        with open(r'C:\Users\Chip\Documents\personalProjects\rokuController\appIDsAndNames.txt') as json_file:
            appIDsAndNames = json.load(json_file)
        for name, appID in appIDsAndNames.items():
            downloadImages(appID, name)


    def launchApp(self, appID):
        appID = appID
        requests.post(self.url+"/launch/"+appID)


import requests
import shutil

def downloadImages(appID, outfilename):
    response = requests.get('http://192.168.1.103:8060/query/icon/'+str(appID), stream=True)
    with open(fr"C:\Users\Chip\Documents\personalProjects\personalProjects\rokuController\appImages\{outfilename}.png", 'wb') as outfile:
        shutil.copyfileobj(response.raw, outfile)
    del response



import pytesseract
from PIL import Image
from os import listdir, path
from os.path import isfile, join
import json
import pprint
import glob


mypath = '/path/to/directory/'

def extract_rawData_image(imageFolderPath):
    files = list(filter(path.isfile, glob.glob(mypath + "*")))
    files.sort(key=lambda x: path.getmtime(x))
    files.reverse()
    return [(path, Image.open(path) , pytesseract.image_to_string(Image.open(path), lang = 'fra')) for path in files]


def is_firstname_lastname_with_x(obj):
    return obj["firstName"].endswith('x') and obj["lastName"].endswith('x')


def clean_data(dataObj, rawdata):
    print( f"is_firstname_lastname_with_x(dataObj) =  {is_firstname_lastname_with_x(dataObj)}")
    newObj = {}
    if(is_firstname_lastname_with_x(dataObj)):
        newObj["expiration"] = dataObj["expiration"].split(' ')[-1:]
        newObj["dob"] = dataObj["dob"].split(' ')[-1:]
        newObj["firstName"] = dataObj["firstName"].split(' ')[:-1]
        newObj["lastName"] = dataObj["lastName"].split(' ')[:-1]
        newObj["nationality"] = dataObj["nationality"]
        
        return newObj
    else:
        print([d for d in rawdata if d.strip()])
        return dataObj
    

def extract_data(rawdata):
    temp_data = [d for d in rawdata.split('\n') if d.strip()][-11:]
    temp_result = {
            "expiration": temp_data[0],
            "lastName": temp_data[2],
            "firstName": temp_data[3],
            "nationality": temp_data[6],
            "dob": temp_data[7]
        }
    return clean_data(temp_result, rawdata.split('\n'))

def entry_function(pathToDir):
    pp = pprint.PrettyPrinter(indent=4)
    for path, imageObj, rawData in extract_rawData_image(pathToDir):
        print("-"*100)
        print(path)
        print("-"*100)
        pp.pprint(extract_data(rawData))
        display(imageObj)
        print("-"*100)
        print("-"*100)
        


entry_function(mypath)
    

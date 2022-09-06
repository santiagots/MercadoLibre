from cmath import log
from configparser import ConfigParser
from datetime import datetime
import glob
import logging
import shutil
import json
import sys
import pandas as pd

config = ConfigParser()
config.read("config.ini")

def tryParseInt(s, val=None):
    try:
        return int(s)
    except ValueError:
        return val 

def tryParseFloat(s, val=None):
    try:
        return float(s)
    except ValueError:
        return val 

def getFilesNames(expresion):
    return glob.glob(expresion)

def moveFiles(filePath, destination):
    shutil.move(filePath, destination)

def getDataFormExcelFile(excelFilePath, sheetName):
    sheetsNames = pd.ExcelFile(excelFilePath).sheet_names
    hasSheet = sheetName  in sheetsNames

    if hasSheet:
        df = pd.read_excel(excelFilePath, sheet_name=sheetName, skiprows=4)
        df = df.fillna("")
        return df.values

    return []

def toJSON(object):
    return json.dumps(object, default=lambda o: o.__dict__, sort_keys=True, indent=4)

def getConfiguration(section, key):
    return config[section][key]

def SetConfiguration(section, key, value):
    config[section][key] = value
    with open("config.ini", "w") as configfile:
        config.write(configfile)

def LogInfo(message):
    print(message)
    logging.info(message)

def LogError(message):
    print(message)
    logging.error(message)

#Creating a handler
def handle_unhandled_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
                #Will call default excepthook
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
        #Create a critical level log message with info from the except hook.
    logging.critical("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))
#Assign the excepthook to the handler
sys.excepthook = handle_unhandled_exception

logging.basicConfig(filename=datetime.now().strftime(getConfiguration("App","logFile")), level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
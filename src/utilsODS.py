import json
import os
#from verbalizer.graph2text.utils import *

"""
saves data structure to path and makes underlining folder structure if this is missing

Parameters:
Data: the data which should be exported
path (str): the path to which the data gets exported
messageText (str): a text which is printed at the end of the function
doPrint (Boolean): defines if messageText gets printed or not

Returns: 
None
"""
def saveToJson(Data, path, messageText = 'saved', doPrint = True):
    data = json.dumps(Data, indent='\t')
    for i in range(2, len(path.split('/'))):
        dirPath = '/'.join(path.split('/')[:i]) + '/'
        if not os.path.exists(dirPath):
            print('mkdir:', dirPath)
            os.mkdir(dirPath)
    with open(path, 'w') as json_file:
        json_file.write(data)
    if doPrint: print(f"{messageText} {path}")
"""
imports a json file from a path

Parameters:
path (str): the path to the json

Returns: 
data inside the path file
"""
def importFromJson(path):
    with open(path, 'r') as json_file:
        data = json.load(json_file)
    return data
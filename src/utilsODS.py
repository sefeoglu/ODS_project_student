import json
import os
#from verbalizer.graph2text.utils import *

def saveToJson(List, path, messageText = 'saved', doPrint = True):
    data = json.dumps(List, indent='\t')
    for i in range(2, len(path.split('/'))):
        dirPath = '/'.join(path.split('/')[:i]) + '/'
        if not os.path.exists(dirPath):
            print('mkdir:', dirPath)
            os.mkdir(dirPath)
    with open(path, 'w') as json_file:
        json_file.write(data)
    if doPrint: print(f"{messageText} {path}")

def importFromJson(path):
    with open(path, 'r') as json_file:
        data = json.load(json_file)
    return data
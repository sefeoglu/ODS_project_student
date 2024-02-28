import json
from verbalizer.Prompt_generator2.graph2text.utils import *

def saveToJson(List, path, messageText = 'saved', doPrint = True):
    data = json.dumps(List, indent='\t')
    dirPath = '/'.join(path.split('/')[:-1]) + '/'
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
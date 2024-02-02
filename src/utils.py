import json

def saveToJson(List, path, messageText = 'saved'):
    data = json.dumps(List, indent='\t')
    with open(path, 'w') as json_file:
        json_file.write(data)
    print(f"{messageText} {path}")

def importFromJson(path):
    with open(path, 'r') as json_file:
        data = json.load(json_file)
    return data
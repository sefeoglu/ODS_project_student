import json


def importConfigODS(configODSPath):
    with open(configODSPath, 'r') as json_file:
        data = json.load(json_file)
    return data

def exportConfigODS(configODS, configODSPath):
    data = json.dumps(configODS, indent='\t')
    with open(configODSPath, 'w') as json_file:
        json_file.write(data)

def reformatConfigODS(configODSPath):
    configODS = importConfigODS(configODSPath)
    configODS.update({'reformatThisFile' : False})
    exportConfigODS(configODS, configODSPath)
    print(f'reformatig {configODSPath} done.')

def resetConfigODS(configODSPath):
    configODS = {'reformatThisFile' : False,
                 'resetThisFile' : False,
                 'runRandomWalk' : True,
                 'runRandomTree' : False,
                 'saveAlignmentsToJson' : True,
                 'alignmentPath' : '../results/result_alignments/conference/alignments.json'
                 }
    exportConfigODS(configODS, configODSPath)
    print(f'restting {configODSPath} done.')

def getConfigODS(configODSPath = './configODS.json'):
    configODS = importConfigODS(configODSPath)
    if configODS.get('reformatThisFile') == True:
        reformatConfigODS(configODSPath)
    if configODS.get('resetThisFile') == True:
        resetConfigODS(configODSPath)
    return configODS

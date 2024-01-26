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
                 'exportAlignmentsToJson' : True,
                 'exportRandomWalkTriples' : True,
                 'exportRandomTreeTriples' : True,
                 'exportWalkPromptsToJson': True,
                 'exportTreePromptsToJson': True,
                 'promptsFoExportToJson': [0],
                 'alignmentPath' : '../results/result_alignments/conference/alignments.json',
                 "walkTriplesPath": "../results/result_triples/triples_randomWalk.json",
                 "treeTriplesPath": "../results/result_triples/triples_randomTree.json",
                 'verbalizedWalkTriplesPath' : '../results/result_triples_verbalized/triples_randomWalk_verbalized_out.json',
                 'verbalizedTreeTriplesPath' : '../results/result_triples_verbalized/triples_randomTree_verbalized_out.json',
                 'promptsPath' : '../results/result_prompts/',
                 }
    exportConfigODS(configODS, configODSPath)
    print(f'resetting {configODSPath} done.')

def getConfigODS(configODSPath = './configODS.json'):
    configODS = importConfigODS(configODSPath)
    if configODS.get('reformatThisFile') == True:
        reformatConfigODS(configODSPath)
    if configODS.get('resetThisFile') == True:
        resetConfigODS(configODSPath)
        configODS = importConfigODS(configODSPath)
    return configODS

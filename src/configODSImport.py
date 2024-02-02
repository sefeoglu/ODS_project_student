import utils

def reformatConfigODS(configODSPath):
    configODS = utils.importFromJson(configODSPath)
    configODS.update({'reformatThisFile' : False})
    utils.saveToJson(configODS, configODSPath)
    print(f'reformatig {configODSPath} done.')

def resetConfigODS(configODSPath):
    configODS = {'reformatThisFile' : False,
                 'resetThisFile' : False,
                 'exportCrossProductAsAlignments': True,
                 'exportAlignmentsToJson' : False,
                 'exportRandomWalkTriples' : True,
                 'exportRandomTreeTriples' : True,
                 'exportWalkPromptsToJson': True,
                 'exportTreePromptsToJson': True,
                 'promptsFoExportToJson': [0, 1, 2, 3],
                 'alignmentPath' : '../results/result_alignments/',
                 "walkTriplesPath": "../results/result_triples/triples_randomWalk.json",
                 "treeTriplesPath": "../results/result_triples/triples_randomTree.json",
                 'verbalizedWalkTriplesPath' : '../results/result_triples_verbalized/triples_randomWalk_verbalized_out.json',
                 'verbalizedTreeTriplesPath' : '../results/result_triples_verbalized/triples_randomTree_verbalized_out.json',
                 'promptsPath' : '../results/result_prompts/',
                 }
    utils.saveToJson(configODS, configODSPath)
    print(f'resetting {configODSPath} done.')

def getConfigODS(configODSPath = './configODS.json'):
    configODS = utils.importFromJson(configODSPath)
    if configODS.get('reformatThisFile') == True:
        reformatConfigODS(configODSPath)
    if configODS.get('resetThisFile') == True:
        resetConfigODS(configODSPath)
        configODS = utils.importFromJson(configODSPath)
    return configODS
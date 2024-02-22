import utils

"""
reformats the json configODS file nicely, saves it to configODSPath
the configODS file is usually named "configODS.json"

Parameters:
configODSPath (str): the path to the configODS file

Returns: 
None
"""
def reformatConfigODS(configODSPath):
    configODS = utils.importFromJson(configODSPath)
    configODS.update({'reformatThisFile' : False})
    utils.saveToJson(configODS, configODSPath)
    print(f'reformatig {configODSPath} done.')


"""
resets the json configODS file to a working standard, saves it to configODSPath
the configODS file is usually named "configODS.json"

Parameters:
configODSPath (str): the path to the configODS file

Returns: 
None
"""
def resetConfigODS(configODSPath):
    configODS = {'reformatThisFile' : False,
                 'resetThisFile' : False,
                 'importOntologies' : True,
                 'computeSimilaritiesExportAsAlignments': True,
                 'matchExactMatches': True,
                 'runRandomWalkAlgorithm' : True,
                 'runRandomTreeAlgorithm' : True,
                 'randomTreeConfig' : {'breadth' : 2, 'path_depth' : 3, 'parent_prob' : 28, 'child_prob' : 28, 'equivalent_prob' : 28, 'object_prob' : 16},
                 'verbalizeAvailableTriples' : True,
                 'exportWalkPromptsToJson': True,
                 'exportTreePromptsToJson': True,
                 'runPromptsOnLLM' : True,
	             'generateMaximumBipartiteMatching': True,
                 'neighborhoodRange' : 2,
                 'exportFinalMatchingsToRDF': True,
                 'promptsFoExportToJson': [0, 1, 2, 3],
                 'alignmentPath' : '../results/result_alignments/conference/',
                 'exactMatchPath': '../results/result_exactMatches/conference/',
                 'triplesPath': '../results/result_triples/conference/',
                 'triplesVerbalizedPath': '../results/result_triples_verbalized/conference/',
                 'llmMatchedPath': '../results/result_llm_matched/conference/',
                 'bipartiteMatchingPath': '../results/result_bipartiteMatching/conference/',
                 'rdfPath': '../results/result_RDF/conference/',
                 'verbalizedWalkTriplesPath' : '../results/result_triples_verbalized/triples_randomWalk_verbalized_out.json',
                 'verbalizedTreeTriplesPath' : '../results/result_triples_verbalized/triples_randomTree_verbalized_out.json',
                 'promptsPath' : '../results/result_prompts/',
                 }
    utils.saveToJson(configODS, configODSPath)
    print(f'resetting {configODSPath} done.')


"""
loads the json configODS file and maintains it when needed

Parameters:
configODSPath (str): the path to the configODS file

Returns: 
the configODS files data
"""
def getConfigODS(configODSPath = './configODS.json'):
    #load configODS
    configODS = utils.importFromJson(configODSPath)
    #Maintenance
    if configODS.get('reformatThisFile') == True:
        reformatConfigODS(configODSPath)
    if configODS.get('resetThisFile') == True:
        resetConfigODS(configODSPath)
        #reload because of resetting
        configODS = utils.importFromJson(configODSPath)
    return configODS
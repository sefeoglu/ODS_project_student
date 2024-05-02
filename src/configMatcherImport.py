import utilsODS

"""
reformats the json configODS file nicely, saves it to configODSPath
the configODS file is usually named "configODS.json"

Parameters:
configODSPath (str): the path to the configODS file

Returns: 
None
"""
def reformatConfigODS(configODSPath):
    configODS = utilsODS.importFromJson(configODSPath)
    configODS.update({'reformatThisFile' : False})
    utilsODS.saveToJson(configODS, configODSPath)
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
                 'computeSimilarities': True,
                 'matchExactMatches': True,
                 'thresholdForExactMatches': 0.95,
                 'runRandomWalkAlgorithm' : True,
                 'runRandomTreeAlgorithm' : True,
                 'randomTreeConfig' : {'breadth' : 2, 'path_depth' : 3, 'parent_prob' : 28, 'child_prob' : 28, 'equivalent_prob' : 28, 'object_prob' : 16},
                 'verbalizeAvailableTriples' : True,
                 'promptVersions': [0, 1, 2, 3],
                 'generateWalkPrompts': True,
                 'generateTreePrompts': True,
                 'runAllPromptsOnLLM' : False,
	             'runMissingPromptsOnDemandAndMatch': True,
                 'thresholdForConsideration' : 0.4,
                 'neighborhoodRange' : 2,
                 'exportFinalMatchingsToRDF': True,
                 'track': 'conference', 
                 'similarityPath' : '../results/result_similarities/conference/',
                 'exactMatchPath': '../results/result_exactMatches/conference/',
                 'triplesPath': '../results/result_triples/conference/',
                 'triplesVerbalizedPath': '../results/result_triplesVerbalized/conference/',
                 'promptsPath' : '../results/result_prompts/conference/',
                 'llmOutcomePath': '../results/result_llmOutcome/conference/',
                 'bipartiteMatchingPath': '../results/result_bipartiteMatching/conference/',
                 'rdfPath': '../results/result_RDF/conference/',
                 }
    utilsODS.saveToJson(configODS, configODSPath)
    print(f'resetting {configODSPath} done.')


"""
loads the json configODS file and maintains it when needed

Parameters:
configODSPath (str): the path to the configODS file

Returns: 
the configODS files data
"""
def getConfig(configODSPath = './configMatcher.json'):
    #load configODS
    configODS = utilsODS.importFromJson(configODSPath)
    #Maintenance
    if configODS.get('reformatThisFile') == True:
        reformatConfigODS(configODSPath)
    if configODS.get('resetThisFile') == True:
        resetConfigODS(configODSPath)
        #reload because of resetting
        configODS = utilsODS.importFromJson(configODSPath)
    return configODS
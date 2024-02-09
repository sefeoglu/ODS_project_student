import utils
import configODSImport
from prompt_generator import generatePromptTemplates
from track import Track
import os
from batch_loaders.random_walk import *
import sys
sys.path.append('./verbalizer/Prompt_generator2/')
from verbalizer.Prompt_generator2 import generatePrompt
from maximum_bipartite_matching import generateMaximumBipartiteMatching
from AlignmentFormat import serialize_mapping_to_file
from alternative_approaches.llm_prompting import LLM

"""
runs functions according to the tasks in configODS
prepares configs, metrics for original project by FrancisGosselin

Parameters:
None

Returns: 
None
"""

def main():
    configODS = configODSImport.getConfigODS()

    #to stuff like in original project
    from train import train
    #get configFile from original project
    config = utils.importFromJson('config.json')
    #configure loader according to original project
    loader_config = {
        "iir":0.8, 
        "inter_soft_r":0.0, 
        "intra_soft_r":0.0, 
        "negative_sampling_strategy": "ontologic_relation",
        "no_hard_negative_samples":False,
        "epoch_over_alignments": False,
        "A": 5,
        "batch_size":32, 
        "n_alignments_per_batch":4
    }

    #pre align all possible classes by cross products as candidates
    if (configODS.get('exportCrossProductAsAlignments') == True):
        #configure metric according to original project
        metrics_config={"results_files_path": "./result_alignments",
            "write_rdf": False,
            "write_tsv": False,
            "write_ranking": False,
            "hits":[1, 3, 5, 10], 
            "debug_files_path": "./debug"}
        
        #load ontologies
        name = "conference"
        t = Track(name, config, metrics_config=metrics_config)
        ontos = {onto.get_name() : onto for onto in t.ontologies}

        #get which ontology maps to which one
        for ontoName1, ontoName2 in t.toBeMatchedOntologies:
            onto1 = ontos.get(ontoName1)
            onto2 = ontos.get(ontoName2)
            if onto1 and onto2:
                crossProduct = [[onto1.get_name() + '#' + class1, onto2.get_name() + '#' + class2, 'no score'] for class1 in onto1.get_classes() for class2 in onto2.get_classes()]
                path = configODS.get('alignmentPath') + ontoName1 + '-' + ontoName2 + '.json'
                utils.saveToJson(crossProduct, path, messageText=f'exported crossProduct ({ontoName1} X {ontoName2}) to ')

    #export alignment candidates by original project
    if (configODS.get('exportAlignmentsToJson') == True):
        path = configODS.get('alignmentPath') + "conference" + '/alignments' + '.json'
        infer_walk_WALK = RandomWalkConfig(walk_type = 'randomWalk', saveTriplesToJson = False, strategy=WalkStrategy.ONTOLOGICAL_RELATIONS, n_branches=5)
        train(["conference"], pretrained=config["General"]["model"], saveAlignmentsToJson = True, alignmentsPath = path, test_size=1.0, consider_train_set=False, loader_config=loader_config, train_walks=infer_walk_WALK, inference_walks=infer_walk_WALK)
        print(f"exported alignments to '{path}'")
    #match exact matches
    if configODS.get('matchExactMatches'):
        for file_path in os.listdir(configODS.get('alignmentPath')):
            if file_path.endswith('.json'):
                alignmentFilePath = configODS.get('alignmentPath') + file_path
                triples = utils.importFromJson(alignmentFilePath)
                exactMatches = []
                for key1, key2, _ in triples:
                    onto1, class1 = key1.split('#')
                    onto2, class2 = key2.split('#')
                    class1Clean = cleanAndLowerString(class1)
                    class2Clean = cleanAndLowerString(class2)
                    if (class1Clean == class2Clean):
                        alreadyIn = False
                        for classA, classB, _ in exactMatches:
                            if classA == class1 or classB == class2:
                                alreadyIn = True
                        if not alreadyIn: exactMatches.append([onto1 + '#' + class1, onto2 + '#' + class2, 1])
                #print(exactMatches)
                utils.saveToJson(exactMatches, configODS.get('exactMatchPath') + file_path, messageText='exported exact matches to')


    #run randomWalk Algorithm
    if configODS.get('runRandomWalkAlgorithm'):
        infer_walk_WALK = RandomWalkConfig(walk_type = 'randomWalk', strategy=WalkStrategy.ONTOLOGICAL_RELATIONS, n_branches=5)
        if ontos:
            for ontoName in ontos.keys():
                onto = ontos.get(ontoName)
                triples = {}
                for class1 in onto.get_classes():
                    triples.update(RandomWalk(onto, class1, infer_walk_WALK).triples)
                path = configODS.get('triplesPath') + "triples_randomWalk_" + onto.get_name() + '.json'
                utils.saveToJson(triples, path, f'exported random walk triples of {onto.get_name()} to')
    #run randomTree Algorithm
    if configODS.get('runRandomTreeAlgorithm'):
        randomTreeConfig = configODS.get('randomTreeConfig')
        if ontos and randomTreeConfig:
            for ontoName in ontos.keys():
                onto = ontos.get(ontoName)
                triples = {}
                for class1 in onto.get_classes():
                    tree = doRandomTree(onto, class1, randomTreeConfig)
                    if tree != None:
                        triplesOfClass1 = []
                        for classA in tree.keys():
                            for relation, classB in tree.get(classA):
                                classA = classA.replace('_', ' ')
                                relation = relation.replace('_', ' ')
                                classB = classB.replace('_', ' ')
                                triplesOfClass1.append([classA, relation, classB])
                        triples[onto.get_name() + '#' + class1] = triplesOfClass1
                path = configODS.get('triplesPath') + "triples_randomTree_" + onto.get_name() + '.json'
                utils.saveToJson(triples, path, f'exported random tree triples of {onto.get_name()} to')
                    

    
    #export triples generated by the random walk algorithm
    if configODS.get('exportRandomWalkTriples') == True:
        infer_walk_WALK = RandomWalkConfig(walk_type = 'randomWalk', saveTriplesToJson = True, triplesPath = configODS.get('walkTriplesPath'), strategy=WalkStrategy.ONTOLOGICAL_RELATIONS, n_branches=5)
        train(["conference"], pretrained=config["General"]["model"], saveAlignmentsToJson = False, test_size=1.0, consider_train_set=False, loader_config=loader_config, train_walks=infer_walk_WALK, inference_walks=infer_walk_WALK)
        print(f"exported random walk triples to '{configODS.get('walkTriplesPath')}'")

    #export triples generated by the random tree algorithm
    if configODS.get('exportRandomTreeTriples') == True:
        infer_walk_TREE = RandomWalkConfig(walk_type = 'randomTree', saveTriplesToJson = True, triplesPath = configODS.get('treeTriplesPath'), strategy=WalkStrategy.ONTOLOGICAL_RELATIONS, n_branches=5)
        train(["conference"], pretrained=config["General"]["model"], saveAlignmentsToJson = False, test_size=1.0, consider_train_set=False, loader_config=loader_config, train_walks=infer_walk_TREE, inference_walks=infer_walk_TREE)
        print(f"exported random tree triples to '{configODS.get('treeTriplesPath')}'")
    
    #export prompts generated by generatePromptTemplates.py with alignment candidates and context triples extracted by random algorithms
    #promptVersions: list of integers indicating which prompt versions to use
    promptVersion = configODS.get('promptsFoExportToJson')
    if promptVersion:
        #print(f"promptVersions: {promptVersion}")
        for i in promptVersion:
            for file_path in os.listdir(configODS.get('alignmentPath')):
                #print(f"processing '{file_path}'")
                if file_path.endswith('.json'):
                    alignmentFilePath = configODS.get('alignmentPath') + file_path
                    if configODS.get('exportWalkPromptsToJson'):
                        if not os.path.exists(configODS.get('promptsPath') + f"walkPromptVersion{i}/"):
                            os.mkdir(configODS.get('promptsPath') + f"walkPromptVersion{i}/")
                        contextPaths = [configODS.get('triplesVerbalizedPath') + 'verbalized_triples_randomWalk_' + ontoName + '.json' for ontoName in file_path.replace('.json', '').split('-')]
                        promptList = generatePromptTemplates.getPrompt(alignmentFilePath, contextPaths, promptVersion = i, promptCounter = -1, skipIfNoContext = True)
                        utils.saveToJson(promptList, configODS.get('promptsPath') + f"walkPromptVersion{i}/"+ file_path, f"exported 'walkPromptVersion{i}' with alignments '{alignmentFilePath} and context '{contextPaths}' to")
                    if configODS.get('exportTreePromptsToJson'):
                        if not os.path.exists(configODS.get('promptsPath') + f"treePromptVersion{i}/"):
                            os.mkdir(configODS.get('promptsPath') + f"treePromptVersion{i}/")
                        contextPaths = [configODS.get('triplesVerbalizedPath') + 'verbalized_triples_randomTree_' + ontoName + '.json' for ontoName in file_path.replace('.json', '').split('-')]
                        promptList = generatePromptTemplates.getPrompt(alignmentFilePath, contextPaths, promptVersion = i, promptCounter = -1, skipIfNoContext = True)
                        utils.saveToJson(promptList, configODS.get('promptsPath') + f"treePromptVersion{i}/"+ file_path, f"exported 'treePromptVersion{i}' with alignments '{alignmentFilePath} and context '{contextPaths}' to")
    if configODS.get('verbalizeAvailableTriples'):
        for file_path in os.listdir(configODS.get('triplesPath')):
            if file_path.endswith('.json'):
                tripleFilePath = configODS.get('triplesPath') + file_path
                tripleVerbalizedFilePath = configODS.get('triplesVerbalizedPath') + 'verbalized_' + file_path
                generatePrompt.verbaliseFile(tripleFilePath, tripleVerbalizedFilePath)
    llm = LLM()
    if configODS.get('runPromptsOnLLM'):
        for dir_path in os.listdir(configODS.get('promptsPath')):
            #print(f"processing '{file_path}'")
            for file_path in os.listdir(configODS.get('promptsPath') + dir_path):
                if file_path.endswith('.json'):
                    promptsPath = configODS.get('promptsPath') + dir_path + '/' + file_path
                    llmMatchedFilePath = configODS.get('llmMatchedPath') + dir_path
                    if not os.path.exists(llmMatchedFilePath):
                        os.mkdir(llmMatchedFilePath + '/')
                    llmMatchedFilePath += '/llm_' + file_path
                    promptDict = utils.importFromJson(promptsPath)
                    promptResult = {}
                    for promptKey in promptDict:
                        prompt = promptDict.get(promptKey)
                        yesOrNo = llm.predict(prompt)
                        if yesOrNo == 'yes':
                            promptResult[promptKey] = yesOrNo
                    utils.saveToJson(promptResult, llmMatchedFilePath)
    if configODS.get('generateMaximumBipartiteMatching'):
        for dir_path in os.listdir(configODS.get('llmMatchedPath')):
            #print(f"processing '{file_path}'")
            for file_path in os.listdir(configODS.get('llmMatchedPath') + dir_path):
                if file_path.endswith('.json'):
                    llmMatchedFilePath = configODS.get('llmMatchedPath') + dir_path + '/' + file_path
                    bipartiteMatchingPath = configODS.get('bipartiteMatchingPath') + dir_path
                    if not os.path.exists(bipartiteMatchingPath):
                        os.mkdir(bipartiteMatchingPath + '/')
                    bipartiteMatchingPath += '/' + file_path
                    llmMatchedClasses = utils.importFromJson(llmMatchedFilePath)
                    verticesL = set()
                    verticesR = set()
                    edges = {}
                    alreadyMatched = {}
                    exactMatches = utils.importFromJson(configODS.get('exactMatchPath') + file_path)
                    for key1, key2, _ in exactMatches:
                        alreadyMatched[key1] = key2
                        edges[key1] = [key2]
                        verticesL.add(key1)
                        verticesR.add(key2)
                    for key in llmMatchedClasses.keys():
                        if llmMatchedClasses.get(key):
                            onto1HASHclass1, onto2HASHclass2 = key.split(';')
                            verticesL.add(onto1HASHclass1)
                            verticesR.add(onto2HASHclass2)
                            if not edges.get(onto1HASHclass1):
                                edges[onto1HASHclass1] = []
                            if not alreadyMatched.get(onto1HASHclass1):
                                edges[onto1HASHclass1].append(onto2HASHclass2)
                    matching = generateMaximumBipartiteMatching.findMaximumBipartiteMatching(list(verticesL), list(verticesR), edges)
                    utils.saveToJson(matching, bipartiteMatchingPath)
    if configODS.get('exportFinalMatchingsToRDF'):
        for dir_path in os.listdir(configODS.get('bipartiteMatchingPath')):
            for file_path in os.listdir(configODS.get('bipartiteMatchingPath') + dir_path):
                if file_path.endswith('.json'):
                    bipartiteMatchingPath = configODS.get('bipartiteMatchingPath') + dir_path + '/' + file_path
                    rdfPath = configODS.get('rdfPath') + dir_path
                    if not os.path.exists(rdfPath):
                        os.mkdir(rdfPath + '/')
                    rdfPath += '/' + file_path.replace('.json', '') + '.rdf'
                    bipartiteMatchedClasses = utils.importFromJson(bipartiteMatchingPath)
                    t = [('http://' + key1, 'http://' + key2, '=', 1.0) for key1, key2 in bipartiteMatchedClasses]
                    serialize_mapping_to_file(rdfPath, t)
                    print('exported ' + rdfPath)

def cleanAndLowerString(string):
    import re
    string = re.sub(r'\s+', ' ', string)  # Replace multiple whitespace characters with a single space
    string = re.sub(r'[;.:_\-#]', '', string)  # Remove specified special characters
    string = string.lower()
    return string


main()

#for preparing fake llmMatched file
# configODS = configODSImport.getConfigODS()
# path = configODS.get('llmMatchedPath')
# path += 'cmt-conference.json'
# print(path)
# data = utils.importFromJson(path)
# r = {}
# for key in data.keys():
#     r[key] = True if random.randint(0, 1) == 1 else False
# utils.saveToJson(r, path)
import json
import configODSImport
from prompt_generator import generatePromptTemplates

def main():
    configODS = configODSImport.getConfigODS()

    #to stuff like in original project
    from train import train
    from batch_loaders.random_walk import RandomWalkConfig, WalkStrategy
    #get configFile from original project
    with open("config.json", 'r') as f:
        config = json.load(f)
    #configure loader
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
    #define different walk configs
    if (configODS.get('exportAlignmentsToJson') == True):
        infer_walk_WALK = RandomWalkConfig(walk_type = 'randomWalk', saveTriplesToJson = False, strategy=WalkStrategy.ONTOLOGICAL_RELATIONS, n_branches=5)
        train(["conference"], pretrained=config["General"]["model"], saveAlignmentsToJson = True, alignmentsPath = configODS.get('alignmentPath'), test_size=1.0, consider_train_set=False, loader_config=loader_config, train_walks=infer_walk_WALK, inference_walks=infer_walk_WALK)
        print(f"exported alignments to '{configODS.get('alignmentPath')}'")
    if configODS.get('exportRandomWalkTriples') == True:
        infer_walk_WALK = RandomWalkConfig(walk_type = 'randomWalk', saveTriplesToJson = True, triplesPath = configODS.get('walkTriplesPath'), strategy=WalkStrategy.ONTOLOGICAL_RELATIONS, n_branches=5)
        train(["conference"], pretrained=config["General"]["model"], saveAlignmentsToJson = False, test_size=1.0, consider_train_set=False, loader_config=loader_config, train_walks=infer_walk_WALK, inference_walks=infer_walk_WALK)
        print(f"exported random walk triples to '{configODS.get('walkTriplesPath')}'")
    if configODS.get('exportRandomTreeTriples') == True:
        infer_walk_TREE = RandomWalkConfig(walk_type = 'randomTree', saveTriplesToJson = True, triplesPath = configODS.get('treeTriplesPath'), strategy=WalkStrategy.ONTOLOGICAL_RELATIONS, n_branches=5)
        train(["conference"], pretrained=config["General"]["model"], saveAlignmentsToJson = False, test_size=1.0, consider_train_set=False, loader_config=loader_config, train_walks=infer_walk_TREE, inference_walks=infer_walk_TREE)
        print(f"exported random tree triples to '{configODS.get('treeTriplesPath')}'")
    promptVersion = configODS.get('promptsFoExportToJson')
    if promptVersion:
        for i in promptVersion:
            if configODS.get('exportWalkPromptsToJson'):
                promptList = generatePromptTemplates.getPrompt(configODS.get('alignmentPath'), configODS.get('verbalizedWalkTriplesPath'), promptVersion = i, promptCounter = -1, skipIfNoContext = True)
                generatePromptTemplates.savePromptToJson(promptList, configODS.get('promptsPath') + f"walkPromptVersion{i}.json")
                print(f"exported 'walkPromptVersion{i}.json' with alignments '{configODS.get('alignmentPath')} and context '{configODS.get('verbalizedWalkTriplesPath')}' to '{configODS.get('promptsPath')}'")
            if configODS.get('exportTreePromptsToJson'):
                promptList = generatePromptTemplates.getPrompt(configODS.get('alignmentPath'), configODS.get('verbalizedTreeTriplesPath'), promptVersion = i, promptCounter = -1, skipIfNoContext = True)
                generatePromptTemplates.savePromptToJson(promptList, configODS.get('promptsPath') + f"treePromptVersion{i}.json")
                print(f"exported 'treePromptVersion{i}.json' with alignments '{configODS.get('alignmentPath')} and context '{configODS.get('verbalizedWalkTriplesPath')}' to '{configODS.get('promptsPath')}'")
        
main()

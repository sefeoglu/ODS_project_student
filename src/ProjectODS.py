import json
import configODSImport

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

    if configODS.get('runRandomWalk') == True:
        infer_walk_WALK = RandomWalkConfig(walk_type = 'randomWalk', strategy=WalkStrategy.ONTOLOGICAL_RELATIONS, n_branches=5)
        train(["conference"], pretrained=config["General"]["model"], saveAlignmentsToJson = configODS.get('saveAlignmentsToJson'), alignmentsPath = configODS.get('alignmentPath'), test_size=1.0, consider_train_set=False, loader_config=loader_config, train_walks=infer_walk_WALK, inference_walks=infer_walk_WALK)
    if configODS.get('runRandomTree') == True:
        infer_walk_TREE = RandomWalkConfig(walk_type = 'randomTree', strategy=WalkStrategy.ONTOLOGICAL_RELATIONS, n_branches=5)
        train(["conference"], pretrained=config["General"]["model"], saveAlignmentsToJson = configODS.get('saveAlignmentsToJson'), alignmentsPath = configODS.get('alignmentPath'), test_size=1.0, consider_train_set=False, loader_config=loader_config, train_walks=infer_walk_TREE, inference_walks=infer_walk_TREE)
main()

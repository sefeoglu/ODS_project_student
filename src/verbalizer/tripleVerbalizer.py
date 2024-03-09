"""
modified by author: Julian Sampels
"""
from tqdm import tqdm
from verbalisation_module import VerbModule
import sys
sys.path.append('..')
from src import utilsODS

verb_module = None

def verbalise(tripleList, verbModule):
    ans = "translate Graph to English: "
    #print(tripleList)
    #predicateSet = set([])
    for item in tripleList:
             ans += f"<H> {item[0]} <R> {item[1]} <T> {item[2]} "

    return verbModule.verbalise(ans)

"""
modified by author: Julian Sampels
"""
def verbaliseFile(FILENAME, outputFile):
    #load module only once
    global verb_module
    if not verb_module:
        verb_module = VerbModule()
    results = {}
    data = utilsODS.importFromJson(FILENAME)
    i = 0
    print(f'start generating "{outputFile}"')
    #only for progressbar
    #for key, value in data.items():
    for key, value in tqdm(data.items(), desc="Verbalizing", unit="item"):
        #compute verbalization
        triples = value
        verbalised_text = verbalise(triples, verb_module)
        results.update({key: verbalised_text})
    utilsODS.saveToJson(results, outputFile)

if __name__ == "__main__":
    #for this path run from cd src/verbalizer/Prompt_generator2
    FILENAME = "../../../results/result_triples/conference/triples_randomTree_cmt.json"
    outputFile = "hello1.json"
    verbaliseFile(FILENAME, outputFile)
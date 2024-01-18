import json
from tqdm import tqdm
from verbalisation_module import VerbModule

def verbalise(tripleList, verbModule):
    ans = "translate Graph to English: "
    print(tripleList)
   # predicateSet = set([])
    for item in tripleList:
             ans += f"<H> {item[0]} <R> {item[1]} <T> {item[2]} "

    return verbModule.verbalise(ans)


def verbaliseFile(FILENAME, outputFile):
    results = []
    with open(FILENAME, "r") as f:
        data = json.loads(f.read())

    for key, value in data.items():
        triples = value
        verbalised_text = verbalise(triples, verb_module)
        results.append({key: verbalised_text})

    json_object = json.dumps(results, indent=4)
    with open(outputFile, "w") as outfile:
        outfile.write(json_object)

if __name__ == "__main__":
    verb_module = VerbModule()
    FILENAME = "triples_randomTree.json"
    outputFile = "Hello/hello1.json"
    verbaliseFile(FILENAME, outputFile)
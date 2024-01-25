import json

problemDefinition = 'In this task, we are given two concepts along with their definitions from two ontologies.'
objective = 'Our objective is to provide ontology mapping for the provided ontologies based on their semantic similarities.'
#importing data1
def importTriples(json_file_path = './result_alignments/conference/alignments.json'):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data

def importContext(json_file_path = './triples_randomWalk_verbalized_out/RandomWalk_verbalized_out.json'):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data

def formatContext():
    data = importContext()
    context = {}
    for i in data:
        key = list(i.keys())[0]
        context.update({key : i.get(key)})
    return context

def groupTriples():
    data = importTriples()
    tuples = []
    for triple in data:
        onto, node1 = triple[0].split('#')
        onto, node2 = triple[1].split('#')
        tuples.append((node1, node2))
    return tuples

#promptCounter is the index of the desired prompt, if promptCounter < 0 all prompts are returned as a list
def getPrompt1(promptCounter = -1, skipIfNoContext = True):
    triples = importTriples()
    context = formatContext()

    #skipIfNoContext
    if (skipIfNoContext):
        tmpTriples = []
        for i, (key1, key2, _) in enumerate(triples):
            cont1 = context.get(key1)
            cont2 = context.get(key2)
            if (cont1 != None and cont2 != None):
                tmpTriples.append(triples[i])
        triples = tmpTriples

    #generate one or all prompts
    if (promptCounter < 0 or promptCounter >= len(triples)):
        prompt = []
        for i in range(len(triples)):
            p = getPrompt1(i, skipIfNoContext)
            if (len(p) > 0):
                prompt.append(p)
    else:
        prompt = problemDefinition + '\n' + objective + '\n'
        key1 = triples[promptCounter][0]
        key2 = triples[promptCounter][1]
        onto1, node1 = key1.split("#")
        onto2, node2 = key2.split("#")
        
        #add context
        cont1 = context.get(key1)
        cont2 = context.get(key2)
        
        prompt += f'{key1}: {cont1}\n' if (cont1 != None) else ''
        prompt += f'{key2}: {cont2}\n' if (cont2 != None) else ''
            
        prompt += f'Does the concept "{node1}" correspond to the concept "{node2}"? yes or no:'
        #workaround
        if (onto1 == onto2):
            return ''
        
    return prompt


p = getPrompt1()
#p = getPrompt1(4)
print('\n\n'.join(p) if (type(p) == type([])) else p)

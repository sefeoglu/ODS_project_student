import json

problemDefinition = 'In this task, we are given two concepts along with their definitions from two ontologies.'
#objective = 'Our objective is to provide ontology mapping for the provided ontologies based on their semantic similarities.'
#importing data1
def importTriples(json_file_path = 'alignments.json'):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data

def importContext(json_file_path = 'triples_randomWalk_out.json'):
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
def JPrompt(promptCounter = -1):
    triples = importTriples()
    if (promptCounter < 0 or promptCounter >= len(triples)):
        prompt = []
        for i in range(len(triples)):
            prompt.append('\n' + JPrompt(i))
    else:
        prompt = problemDefinition + '\n'
        key1 = triples[promptCounter][0]
        key2 = triples[promptCounter][1]
        onto1, node1 = key1.split("#")
        onto2, node2 = key2.split("#")
        
        #add context
        context = formatContext()
        cont1 = context.get(key1)
        cont2 = context.get(key2)
        prompt += f'{cont1}\n' if (cont1 != None) else ''
        prompt += f'{cont2}\n' if (cont2 != None) else ''
            
        prompt += f'Is the concept "{node1}" the same as the concept "{node2}"? Answer: yes or no'
        
    return prompt

"""
def JPrompt2(promptCounter = -1):
    tuples = groupTriples()
    prompt = ''
    if (promptCounter < 0 or promptCounter >= len(tuples)):
        for i in range(len(tuples)):
            prompt += JPrompt(i)
            prompt += '\n----------------------------------------------\n'
    else: 
        prompt = 'I will give you a Tuple in the form of (Class/Object from Ontology1, Class/Object from Ontology2).\n\n'
        prompt += f"({tuples[promptCounter][0]}, {tuples[promptCounter][1]})"
        prompt += '\n\n' + objective
    return prompt

"""

"""
#prepare some prompts from GPT paper: https://disi.unitn.it/~pavel/om2023/papers/om2023_STpaper1.pdf
def prompt1():
    data1Keys, data1 = importTriples()
    prompt = problemDefinition + '\nOntology 1:\n'
    for key in data1Keys:
        tmpHelp = lambda input_list : ', '.join(' '.join(item) for item in input_list)
        prompt += tmpHelp(data1[key])
    prompt += '\n' + objective
    return prompt

def prompt2():
    data1Keys, data1 = importTriples()
    prompt1 = problemDefinition + '\nOntology 1:\n'
    for key in data1Keys:
        tmpHelp = lambda input_list : ', '.join(' '.join(item) for item in input_list)
        prompt1 += tmpHelp(data1[key])
    prompt2 = 'Provide a complete and comprehensive matching of the ontologies'
    return prompt1, prompt2

def prompt7():
    data1Keys, data1 = importTriples()
    prompt1 = problemDefinition + '\nOntology 1:\n'
    for key in data1Keys:
        tmpHelp = lambda input_list : ', '.join(' '.join(item) for item in input_list)
        prompt1 += tmpHelp(data1[key])
    prompt2 = 'For a class/property in the first ontology, which class/property in ontology 2 is the best match?'
    prompt2 += '\nOntology 2:\n'
    return prompt1, prompt2

#print(prompt1())
#print('\n'.join(prompt2()))
#print('\n'.join(prompt7()))
"""


p = JPrompt()
#p = JPrompt(4)
print('\n'.join(p) if (type(p) == type([])) else p)

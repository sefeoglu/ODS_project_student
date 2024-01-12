import json

problemDefinition = 'In this task, we are given two ontologies in the form of <Subject> is <relation> of <Object>, which consist of classes and properties.'
objective = 'Our objective is to provide ontology mapping for the provided ontologies based on their semantic similarities.'
#importing data1
def importTriples (json_file_path = 'triples_randomWalk_verbalized.json'):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    global data1Keys
    dataKeys = list(data.keys())
    return dataKeys, data

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
print('\n'.join(prompt2()))
#print('\n'.join(prompt7()))

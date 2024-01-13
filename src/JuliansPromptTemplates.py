import json

problemDefinition = 'In this task, we are given two ontologies in the form of <Subject> is <relation> of <Object>, which consist of classes and properties.'
objective = 'Our objective is to provide ontology mapping for the provided ontologie based on their semantic similarities.'
#importing data1
def importTriples(json_file_path = 'alignments.json'):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data

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
    tuples = groupTriples()
    if (promptCounter < 0 or promptCounter >= len(tuples)):
        prompt = []
        for i in range(len(tuples)):
            prompt.append(JPrompt(i))
    else: 
        prompt = f'Is the concept "{tuples[promptCounter][0]}" the same as the concept "{tuples[promptCounter][1]}" yes or no?'
    return prompt

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

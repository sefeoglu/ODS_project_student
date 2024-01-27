# Definition of the prompt templates
## prompt 0:
Full explanation of the task with comprehensive explanation with context, mentioning the concepts twice.
e.g.:
> In this task, we are given two concepts along with their definitions from two ontologies.  
> Our objective is to provide ontology mapping for the provided ontologies based on their semantic similarities.  
> _{ontology1}_#_{concept1}_: _{context1}_  
> _{ontology2}_#_{concept2}_: _{context2}_
> Does the concept "_{concept1}_" correspond to the concept "_{concept2}_"? yes or no:

## prompt 1:
Short task description at the start with context and question at the end.
e.g.:
> Classify if two concepts refer to the same real word entity.  
> This is the context for the first concept "_{concept1}_":  
> _{context1}_
>   
> This is the context for the second concept "_{concept2}_":  
> _{context2}_
> Do these concepts "_{concept1}_" and "_{concept2}_" refer to the same real word entity? yes or no:

## prompt 2:
Short task description with context
e.g.:
> Classify if the following two concepts are the same.  
> \###First concept _{concept1}_:  
> _{context2}_
> \###Second concept _{concept2}_:  
> _{context2}_
> Answer yes or no:

## prompt 3:
Basic prompt without any definition about concepts.
e.g.:
> Is _{concept1}_ and _{concept2}_ the same?
> The answer which can be yes or no is:

from Util import Cust
from select import read_specific_line
# Placeholder for the selected line variable
#selected_line =  read_specific_line('treePromptVersion0.json', 3)
line_content = read_specific_line('treePromptVersion0.json', 15)
#print(f"line_content = {line_content}")
llm = Cust(endpoint="https://340e-34-125-82-134.ngrok-free.app", verbose=False)
#a= print(f"line_content = {line_content}")
# Use the selected line as the input to the llm function
result = llm(line_content)
print(result)

#def categorize_response(response):
    # Define simple positive and negative keywords
  #  positive_keywords = ['yes', 'positive', 'correct', 'true', 'agree']
  #  negative_keywords = ['no', 'negative', 'incorrect', 'false', 'disagree']
    
    # Lowercase the response for case-insensitive matching
  #  response_lower = response.lower()
    
    # Check for positive or negative keywords in the response
 #   if any(keyword in response_lower for keyword in positive_keywords):
 #       return 1  # Positive response
  #  elif any(keyword in response_lower for keyword in negative_keywords):
 #       return 0  # Negative response
 #   else:
 #       return -1  # Unclear or neutral response

# Example usage with the LLM result
#result = llm(line_content)
#print(f"Original LLM Response: {result}")

# Process the LLM response
#categorized_result = categorize_response(result)
#print(f"Categorized Result: {categorized_result}")

def categorize_response(response):
    positive_keywords = ['yes', 'positive', 'correct', 'true', 'agree']
    negative_keywords = ['no', 'negative', 'incorrect', 'false', 'disagree']
    
    response_lower = response.lower()
    
    if any(keyword in response_lower for keyword in positive_keywords):
        return "yes"  # Positive response
    elif any(keyword in response_lower for keyword in negative_keywords):
        return "no"  # Negative response
    else:
        return "unclear"  # Unclear or neutral response

# Using the LLM result
#result = llm(line_content)
#print(f"LLM Response: {result}")

# Process and categorize the LLM response
#categorized_result = categorize_response(result)
#print(f"Categorized Result: {categorized_result}")

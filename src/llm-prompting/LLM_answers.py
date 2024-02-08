from Util2 import CustomLLM
import json

def load_alignments(file_path):
    with open(file_path, 'r') as file:
        alignments = json.load(file)
    return alignments

def load_all_lines(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def categorize_response(response):
    positive_keywords = ['yes', 'positive', 'correct', 'true', 'agree']
    negative_keywords = ['no', 'negative', 'incorrect', 'false', 'disagree']
    response_lower = response.lower()
    if any(keyword in response_lower for keyword in positive_keywords):
        return "yes"
    elif any(keyword in response_lower for keyword in negative_keywords):
        return "no"
    else:
        return "unclear"

def process_lines(all_lines, alignments):
    results = {}
    for index, line_content in enumerate(all_lines, start=1):
        if (index - 1) < len(alignments):
            result = llm(line_content)
            categorized_result = categorize_response(result)
            # Construct the key from the alignment pair
            key = f"{alignments[index - 1][0]};{alignments[index - 1][1]}"
            if categorized_result == "yes":
                results[key] = True
            else:
                # If you want  to include non-matching pairs as false, uncomment the next line
                # results[key] = False
                pass
    return results

def save_results_to_json(results, output_file_path):
    with open(output_file_path, 'w') as file:
        json.dump(results, file, indent=4)

# Initialize the CustomLLM
llm = CustomLLM(endpoint="https://461a-34-31-158-201.ngrok-free.app", verbose=False)

#  Load alignments and all lines
alignments_path = 'cmt-conference_alig.json'  # Make sure to update this path
input_file_path = 'cmt-conference.json'  # Update this path accordingly
all_lines = load_all_lines(input_file_path)
alignments = load_alignments(alignments_path)

# Process all lines and get results
results = process_lines(all_lines, alignments)

# Save the results to a JSON file
output_file_path = 'all_ontology_results.json'  # Update this path as needed
save_results_to_json(results, output_file_path)

print(f"All ontology results have been saved to {output_file_path}")

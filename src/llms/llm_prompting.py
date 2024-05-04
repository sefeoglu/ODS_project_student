
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

class LLM():

    """Code provided by the supervisor to use the T5 model for generating responses to prompts.
    Note: those codes and results do not subject to the evaluation of the project, namely grading.
    """

    def __init__(self, model_id="google/flan-t5-xl"):

        self.model_id = model_id
        self.model, self.tokenizer = self.get_model(model_id)

    def get_model(self, model_id="google/flan-t5-xl"):

        """Get the model and tokenizer for the given model_id.
        """
        
        tokenizer = T5Tokenizer.from_pretrained(model_id)

        model = T5ForConditionalGeneration.from_pretrained(model_id, 
                                                    device_map="auto", 
                                                    load_in_8bit=False, 
                                                    torch_dtype=torch.float16)
        return model,tokenizer

    def get_prediction(self, prompt, length=30):
        """Get the response to the prompt.
        """
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        inputs = self.tokenizer(prompt, add_special_tokens=True, max_length=1000,return_tensors="pt").input_ids.to(device)
        
        outputs = self.model.generate(inputs, max_new_tokens=length,do_sample=True,top_k=50,top_p=0.9)
        
        response = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        
        return response


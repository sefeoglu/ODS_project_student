import requests
import json
from typing import Any, List, Mapping, Optional
from colorama import Fore

from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM

class CustomLLM(LLM):
    endpoint: str
    verbose: bool = False

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
                
        if self.endpoint[-1] == "/":
            self.endpoint = self.endpoint[:-1]
        
        """Call the LLM."""
        response = requests.get(f"{self.endpoint}/prompt", params={"text": prompt, "stop": json.dumps(stop)})

        if response.status_code != 200:
            raise ValueError(f"Request failed with status code {response.status_code}")
        
        # Print the response if verbose
        if self.verbose:
            print(Fore.MAGENTA + f"\n{response.text}\n" + Fore.RESET)
        
        return response.text

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"endpoint": self.endpoint, "verbose": self.verbose}
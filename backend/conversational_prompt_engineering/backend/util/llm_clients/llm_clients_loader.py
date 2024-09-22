import os
from conversational_prompt_engineering.backend.util.llm_clients.abst_llm_client import AbstLLMClient

from langchain_core.messages import HumanMessage

import langchain_google_genai
import langchain_openai
import langchain_ibm

class_mappings = {
    'langchain_google_genai.ChatGoogleGenerativeAI': langchain_google_genai.ChatGoogleGenerativeAI,
    'langchain_openai.ChatOpenAI': langchain_openai.ChatOpenAI,
    'langchain_ibm.WatsonxLLM': langchain_ibm.WatsonxLLM,
}

# example_client_config =  {
#     "short_name": "gemini-1.5-flash",
#     "class_name": "langchain_goole_genai.ChatGoogleGenerativeAI",
#     "api_key_env_var": "GOOGLE_API_KEY",
#     "kwargs": {
#     "model": "gemini-1.5-flash"
#     }
# }

def init_llm_client(client_config):
    _class = class_mappings[client_config['class_name']]
    if 'api_key_env_var' in client_config:
        api_key = os.getenv(client_config['api_key_env_var'], None)
        client_config['kwargs']['api_key'] = api_key
    # end if
    llm = _class(**client_config['kwargs'])
    return LLMClient(llm)
# end def

class LLMClient(AbstLLMClient):
    def __init__(self, llm, *args, **kwargs):
        super(LLMClient, self).__init__()
        self.llm    = llm
        self.args   = args
        self.kwargs = kwargs

        self.model_id = None
    # end def

    @classmethod
    def credentials_params(cls):
        return {}
    # end def

    @classmethod
    def display_name(self):
        return "Default"
    # end def

    def prompt_llm(self, conversation, max_new_tokens=None):
        # NOTE: max_new_tokens not supported at inference time currently

        # prepend human message to avoid Gemini error
        if isinstance(conversation, str):
            generated_text = self.llm.invoke(conversation).content
            return [generated_text]
        # end if

        if not(isinstance(conversation[0], HumanMessage)):
            conversation = [HumanMessage('You are a helpful assistant (system).')] + conversation
        # end if
        generated_text = self.llm.invoke(conversation).content

        return [generated_text]
    # end def
# end class
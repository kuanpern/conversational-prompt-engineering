import os
from glob import glob
from conversational_prompt_engineering.backend.util.llm_clients.bam_client import BamClient
from conversational_prompt_engineering.backend.util.llm_clients.watsonx_client import WatsonXClient
from conversational_prompt_engineering.backend.util.llm_clients.abst_llm_client import AbstLLMClient

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from openai import OpenAI

llm_classes = {
    "google/gemini-1.5-flash": ChatGoogleGenerativeAI,
}

class DefaultClient(AbstLLMClient):
    def __init__(self, api_endpoint=None, model_params=None):
        super(DefaultClient, self).__init__()
        self.parameters   = model_params
        self.api_endpoint = api_endpoint

        if self.parameters is None:
            self.parameters = {}
        # end if
        self.model_id = self.parameters['model_id']

        self.llm = None
        self.vllm_client = None
        if self.api_endpoint is None: # vendor api
            llm_class = llm_classes[self.model_id]
            model_name = self.model_id.split("/")[-1]
            self.llm   = llm_class(model=model_name) # TODO: support more model_params
        else:
            self.llm = ChatOpenAI(
                model    = self.model_id,
                api_key  = os.getenv('VLLM_API_KEY', 'EMPTY'),
                base_url = self.api_endpoint,
            )
        # end if
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
        print('conversation:')
        print(conversation)

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


def get_client_classes(llm_clients_list):
    all_models = [DefaultClient, BamClient, WatsonXClient]
    name_to_models = {x.__name__: x for x in all_models}
    return [name_to_models[x] for x in llm_clients_list]
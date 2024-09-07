import os
from glob import glob
from conversational_prompt_engineering.backend.util.llm_clients.bam_client import BamClient
from conversational_prompt_engineering.backend.util.llm_clients.watsonx_client import WatsonXClient
from conversational_prompt_engineering.backend.util.llm_clients.abst_llm_client import AbstLLMClient


import google.generativeai as genai


class DefaultClient(AbstLLMClient):
    def __init__(self, api_endpoint=None, model_params=None):
        super(DefaultClient, self).__init__()
        self.parameters = model_params
        self.api_endpoint = api_endpoint
        self.api_key = self._get_env_var("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)

        # TODO: support model params
    # end def

    @classmethod
    def credentials_params(cls):
        return {"GOOGLE_API_KEY": "Watsonx API key"}



#    def __init__(self, api_endpoint, model_params):
#        super(GeminiClient, self).__init__()

    @classmethod
    def display_name(self):
        return "Default"
    # end def

    def prompt_llm(self, conversation, max_new_tokens=None):
        # TODO: remove hardcoding
        model = genai.GenerativeModel("gemini-1.5-flash")

        print('type(conversation):', type(conversation))
        print('conversation')
        print(conversation)

        kwargs = {
            'contents': conversation
        }
        # TODO: support more parameters
        if max_new_tokens is not None:
            kwargs['generation_config'] = genai.types.GenerationConfig(
                max_output_tokens = max_new_tokens,
            )
        # end if

        response = model.generate_content(**kwargs)
        print('response')
        print(response)
        return response.text.strip()
    # end def
# end class


def get_client_classes(llm_clients_list):
    all_models = [DefaultClient, BamClient, WatsonXClient]
    name_to_models = {x.__name__: x for x in all_models}
    return [name_to_models[x] for x in llm_clients_list]
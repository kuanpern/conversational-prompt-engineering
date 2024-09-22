# (c) Copyright contributors to the conversational-prompt-engineering project

# LICENSE: Apache License 2.0 (Apache-2.0)
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import time
import os
import json

import pandas as pd

from conversational_prompt_engineering.backend.prompt_building_util import TargetModelHandler, LLAMA_END_OF_MESSAGE, \
    _get_llama_header, LLAMA_START_OF_INPUT

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, merge_message_runs

def extract_delimited_text(txt, delims):
    try:
        if type(delims) is str:
            delims = [delims]
        for delim in delims:
            if delim in txt:
                begin = txt.index(delim) + len(delim)
                end = begin + txt[begin:].index(delim)
                return txt[begin:end]
        return txt  # delims not found in text
    except ValueError:
        return txt
    # end try
# end def

def format_chat(chat, model_id):
    # TODO: default to using langchain
    if any([name in model_id for name in ['mixtral', 'prometheus']]):
        bos_token = '<s>'
        eos_token = '</s>'
        chat_for_mixtral = []
        prev_role = None
        for m in chat:
            if m["role"] == prev_role:
                chat_for_mixtral[-1]["content"] += "\n" + m["content"]
            else:
                chat_for_mixtral.append(m)
            prev_role = m["role"]

        for m in chat_for_mixtral:
            if m["role"] == 'user':
                m["content"] = 'user: ' + m["content"]
            elif m["role"] == 'system':
                m["role"] = 'user'
                m["content"] = 'system: ' + m["content"]

        prompt = bos_token
        for m in chat_for_mixtral:
            if m['role'] == 'user':
                prompt += '[INST] ' + m['content'] + ' [/INST] '
            else:
                prompt += m['content'] + eos_token + ' '
        return prompt
    elif 'llama' in model_id:
        msg_str = LLAMA_START_OF_INPUT
        for m in chat:
            msg_str += _get_llama_header(m['role']) + "\n\n" + m['content'] + LLAMA_END_OF_MESSAGE
        msg_str += _get_llama_header('assistant')
        return msg_str
    else: # use langchain
        messages = []
        for m in chat:
            if m["role"] == 'user':
                messages.append( HumanMessage(content=m['content']))
            elif m["role"] == 'assistant':
                messages.append(    AIMessage(content=m['content']))
            elif m["role"] == 'system':
                messages.append( HumanMessage(content=m['content']))
            else:
                raise ValueError('unknown role: ' + m['role'])
            # end if
        # end for
        return merge_message_runs(messages)
    # end if
# end def

class ChatManagerBase:
    def __init__(self, llm_client, target_llm_client, output_dir, config_name) -> None:

        self.dataset_name = None
        self.state = None
        self.timing_report = []

        self.llm_client        = llm_client
        self.target_llm_client = target_llm_client

        self.model        = self.llm_client.model_id
        self.target_model = self.target_llm_client.model_id
        self.out_dir      = output_dir
        self.config_name  = config_name

        logging.info(f"selected {self.model}")
        logging.info(f"selected target {self.target_model}")
        logging.info(f"output is saved to {os.path.abspath(self.out_dir)}")
    # end def

    def save_config(self):
        chat_dir = os.path.join(self.out_dir, "chat")
        os.makedirs(chat_dir, exist_ok=True)
        with open(os.path.join(chat_dir, "config.json"), "w") as f:
            json.dump({"model": self.model,
                       "dataset": self.dataset_name,
                       "config_name": self.config_name,
                       "target_model": self.target_model}, f)
        # end with
    # end def

    def save_chat_html(self, chat, file_name):
        def _format(msg):
            role = msg['role'].upper()
            txt = msg['content']
            relevant_tags = {k: msg[k] for k in (msg.keys() - {'role', 'content', 'tooltip'})}
            tags = ""
            if relevant_tags:
                tags = str(relevant_tags)
            return f"<p><b>{role}: </b>{txt} {tags}</p>".replace("\n", "<br>")

        chat_dir = os.path.join(self.out_dir, "chat")
        os.makedirs(chat_dir, exist_ok=True)
        df = pd.DataFrame(chat)
        df.to_csv(os.path.join(chat_dir, f"{file_name.split('.')[0]}.csv"), index=False)
        with open(os.path.join(chat_dir, file_name), "w") as html_out:
            content = "\n".join([_format(x) for x in chat])
            header = "<h1>IBM Research Conversational Prompt Engineering</h1>"
            html_template = f'<!DOCTYPE html><html>\n<head>\n<title>CPE</title>\n</head>\n<body style="font-size:20px;">{header}\n{content}\n</body>\n</html>'
            html_out.write(html_template)

    def _add_msg(self, chat, role, msg):
        chat.append({'role': role, 'content': msg})

    def print_timing_report(self):
        df = pd.DataFrame(self.timing_report)
        logging.info(df)
        logging.info(f"Average processing time: {df['total_time'].mean()}")
        self.timing_report = sorted(self.timing_report, key=lambda row: row['total_time'])
        logging.info(f"Highest processing time: {self.timing_report[-1]}")
        logging.info(f"Lowest processing time: {self.timing_report[0]}")

    def _generate_output_and_log_stats(self, conversation, client, max_new_tokens=None):
        start_time = time
        generated_texts, stats_dict = client.send_messages(conversation, max_new_tokens)
        elapsed_time = time.time() - start_time.time()
        timing_dict = {"total_time": elapsed_time, "start_time": start_time.strftime("%d-%m-%Y %H:%M:%S")}
        timing_dict.update(stats_dict)
        logging.info(timing_dict)
        self.timing_report.append(timing_dict)
        return generated_texts


    def prompt_llm(self, conversation, max_new_tokens=None):
        model = self._get_model(max_new_tokens)
        res = model.generate_text(prompt=[conversation])
        texts = [x.strip() for x in res]
        return texts

    def _generate_output(self, prompt_str, client=None):
        if client is None:
            client = self.target_llm_client

        generated_texts = self._generate_output_and_log_stats(prompt_str, client=client)
        agent_response = generated_texts[0]
        logging.info(f"got response from model: {agent_response}")
        return agent_response.strip()

    def _get_assistant_response(self, chat, max_new_tokens=None):
        conversation = format_chat(chat, self.model)
        generated_texts = self._generate_output_and_log_stats(conversation, client=self.llm_client,
                                                              max_new_tokens=max_new_tokens)
        agent_response = ''
        for txt in generated_texts:
            if any([f'<|{r}|>' in txt for r in ['system', 'user']]):
                agent_response += txt[: txt.index('<|')]
                break
            agent_response += txt
        logging.info(f"got response from model: {agent_response}")
        return agent_response.strip()

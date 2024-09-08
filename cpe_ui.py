# (c) Copyright contributors to the conversational-prompt-engineering project

# LICENSE: Apache License 2.0 (Apache-2.0)
# http://www.apache.org/licenses/LICENSE-2.0

import datetime
import os
import sys
import dotenv
import logging

import streamlit as st
from genai.schema import ChatRole
from st_pages import Page, show_pages
from streamlit_js_eval import streamlit_js_eval

from configs.config_utils import load_config
from conversational_prompt_engineering.backend.util.llm_clients.llm_clients_loader import init_llm_client
from conversational_prompt_engineering.backend.callback_chat_manager import CallbackChatManager
from conversational_prompt_engineering.data.dataset_utils import load_dataset_mapping

from conversational_prompt_engineering.util.csv_file_utils import read_user_csv_file
from conversational_prompt_engineering.util.upload_csv_or_choose_dataset_component import \
    create_choose_dataset_component_train,  StartType

version = "callback manager v1.0.7"

st.set_page_config(layout="wide", menu_items={"About": f"CPE version: {version}"})

MUST_HAVE_UPLOADED_DATA_TO_START = True

dotenv.load_dotenv()

def reset_chat():
    streamlit_js_eval(js_expressions="parent.window.location.reload()")
# end def

def set_output_dir():
    output_dir = st.session_state["config"]["General"].get("output_dir", f'_out/')
    out_folder = os.path.join(output_dir, datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    os.makedirs(out_folder, exist_ok=True)
    return out_folder
# end def


def callback_cycle():
    # create the manager if necessary

    if 'existing_chat_loaded' not in st.session_state:
        st.session_state['existing_chat_loaded'] = False

    # if not st.session_state['existing_chat_loaded']:
    #     with st.popover("load existing chat (debug)"):
    #         st.markdown("Local path to an existing chat 👋")
    #         existing_chat_path = st.text_input("path")
    # else:
    #     existing_chat_path = ""

    if "manager" not in st.session_state:
        output_dir = set_output_dir()
        file_handler = logging.FileHandler(os.path.join(output_dir, "out.log"))
        logger = logging.getLogger()
        logger.addHandler(file_handler)

        llm_configs = st.session_state["config"]["LLM"]
        model_id = st.session_state.model
        llm_client = init_llm_client(llm_configs[model_id])
        llm_client.model_id = model_id

        target_model_id = st.session_state.target_model
        target_llm_client = init_llm_client(llm_configs[target_model_id])
        target_llm_client.model_id = target_model_id

        st.session_state.manager = CallbackChatManager(
            llm_client        = llm_client,
            target_llm_client = target_llm_client,
            output_dir        = output_dir,
            config_name       = st.session_state["config_name"]
        ) # end create CallbackChatManager

    manager = st.session_state.manager

    # layout reset and upload buttons in 3 columns
    if st.button("Reset chat"):
        streamlit_js_eval(js_expressions="parent.window.location.reload()")

    static_welcome_msg = \
        "Hello! I'm an IBM prompt building assistant. In the following session we will work together through a natural conversation, to build an effective instruction – a.k.a. prompt – personalized for your task and data. Note that the prompt will be created to operate on each example individually. Therefore, if your task involves multiple texts, such as multi-document summarization, a single input example should include multiple texts."

    with st.chat_message(ChatRole.ASSISTANT):
        st.write(static_welcome_msg)

    if not "csv_file_train" in st.session_state:
        st.session_state[f"csv_file_train"] = None
    start_type = create_choose_dataset_component_train(st=st, manager=manager)
    if start_type == StartType.Uploaded:
        manager.add_user_message_only_to_user_chat("Selected data")

    static_upload_data_msg = "To begin, please select a dataset from our datasets catalog above."
    with st.chat_message(ChatRole.ASSISTANT):
        st.write(static_upload_data_msg)

    if ("existing_chat_path" in st.session_state and st.session_state["existing_chat_path"] != "") and not \
            st.session_state['existing_chat_loaded']:
        manager, dataset = manager.load_chat_to_manager(st.session_state["existing_chat_path"])

        if 'selected_dataset' not in st.session_state:
            st.session_state['selected_dataset'] = dataset
        st.session_state['existing_chat_loaded'] = True

    dataset_is_selected = "selected_dataset" in st.session_state or "csv_file_train" in st.session_state
    if not MUST_HAVE_UPLOADED_DATA_TO_START or dataset_is_selected or start_type == StartType.Loaded:
        if user_msg := st.chat_input("Write your message here"):
            manager.add_user_message(user_msg)

    for msg in manager.user_chat[:manager.user_chat_length]:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'], help=msg['tooltip'] if "tooltip" in msg else None)

        # generate and render the agent response
    with st.spinner("Thinking..."):
        if start_type == StartType.Uploaded:
            manager.process_examples(read_user_csv_file(st.session_state["csv_file_train"]), st.session_state[
                "selected_dataset"] if "selected_dataset" in st.session_state else "user")
        messages = manager.generate_agent_messages()
        for msg in messages:
            with st.chat_message(msg['role']):
                if manager.example_num is not None:
                    orig = manager.examples[manager.example_num - 1].replace('\n', '\n\n')
                    tooltip = f"**Currently discussed input example (#{manager.example_num}):\n\n{orig}**"
                    manager.user_chat[-1]["tooltip"] = tooltip
                else:
                    tooltip = None
                st.markdown(msg['content'], help=tooltip)

    if manager.zero_shot_prompt is not None:
        btn = st.download_button(
            label="Download zero shot prompt",
            data=manager.zero_shot_prompt,
            file_name='zero_shot_prompt.txt',
            mime="text"
        )

    if manager.few_shot_prompt is not None:
        btn = st.download_button(
            label="Download few shot prompt",
            data=manager.few_shot_prompt,
            file_name='few_shot_prompt.txt',
            mime="text"
        )
# end def

instructions_for_user = {
    "main_instructions_for_user":
        "Welcome to Conversational Prompt Engineering (CPE) service proposed by IBM Research.\n" \
        "This service is intended to help users build an effective prompt, tailored to their specific use case, through a simple chat with an LLM.\n" \
        "To make the most out of this service, it would be best to prepare in advance at least 3 input examples that represent your use case in a simple csv file. Alternatively, you can use sample data from our data catalog.\n" \
        "For more information feel free to contact us in slack via [#foundation-models-lm-utilization](https://ibm.enterprise.slack.com/archives/C04KBRUDR8R).\n" \
        "This assistant system uses BAM or Watsonx to serve LLMs. Do not include PII or confidential information in your responses, nor in the data you share.",
}

def submit_button_clicked(model, target_model):
    st.session_state.user_confirmed_models = True
    st.session_state.model = model
    st.session_state.target_model = target_model
# end def

def OK_to_proceed_to_chat():
    return all([
        'model'            in st.session_state,
        'target_model'     in st.session_state,
        getattr(st.session_state, 'user_confirmed_models', False),
    ])
# end def


def init_set_up_page():
    st.title(":blue[Conversational Prompt Engineering]")

    configs     = st.session_state["config"]
    llm_configs = configs["LLM"]
    models      = configs['General']['supported_models']

    if OK_to_proceed_to_chat():
        return True
    else:
        st.empty()
        st.session_state.user_confirmed_models = False
        st.write(instructions_for_user.get("main_instructions_for_user"))

        model = st.radio(
            label="Select the model to coordinate conservational prompt tuning",
            options=[llm_configs[m]['short_name'] for m in models],
            key="model_radio",
            captions=models)
        target_model = st.radio(
            label="Select the target model. The prompt that you will build will be formatted for this model.",
            options=[llm_configs[m]['short_name'] for m in models],
            key="target_model_radio",
            captions=models)
        
        d = {llm_configs[m]['short_name']: m for m in models}        
        st.button("Submit", on_click=submit_button_clicked, args=[d[model], d[target_model]])
        return False
    # end if
# end def


def init_config():
    if len(sys.argv) > 1:
        logging.info(f"Loading {sys.argv[1]} config")
        config_name = sys.argv[1]
    else:
        logging.info(f"Loading default config")
        config_name = "main"

    config = load_config(config_name)
    st.session_state["config_name"] = config_name
    st.session_state["config"] = config
    st.session_state["dataset_name_to_dir"] = load_dataset_mapping(config)
    if config["UI"].get("background_color") is not None:
        st._config._set_option("theme.secondaryBackgroundColor", config["UI"]["background_color"], where_defined=None)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
    if not "config" in st.session_state:
        init_config()
        st.rerun()
    show_pages(
        [
            Page("cpe_ui.py", "Chat", ""),
            Page("conversational_prompt_engineering/pages_/faq.py", "FAQ", ""),
            Page("conversational_prompt_engineering/pages_/survey.py", "Survey", ""),
            Page("conversational_prompt_engineering/pages_/evaluation.py", "Evaluate", ""),
        ]
    )

    set_up_is_done = init_set_up_page()
    if set_up_is_done:
        callback_cycle()
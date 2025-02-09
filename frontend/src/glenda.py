import streamlit as st
from openai import OpenAI



akash_model = OpenAI(api_key=st.secrets["AKASH_API_KEY"], base_url="https://chatapi.akash.network/api/v1")
local_model = OpenAI(api_key='ollama', base_url = 'http://localhost:11434/v1')


def glenda_talk(local):

    if "openai_model" not in st.session_state:
        st.session_state.model = "qwen2.5:7b" if local == True else "Meta-Llama-3-1-405B-Instruct-FP8"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    

    placeholder = st.empty()  # Reserve space at the bottom for the input

    if prompt := placeholder.chat_input("How may I help?"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            client_model = local_model if local == True else akash_model

            stream = client_model.chat.completions.create(
                model=st.session_state.model,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})




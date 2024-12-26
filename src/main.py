import os
import json
import streamlit as st
import openai

# configure OpenAI - API key
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))

# chack if the API key is set
# print(config_data)

OpenAI_API_KEY = config_data["OPENAI_API_KEY"]
openai.api_key = OpenAI_API_KEY

# configuring Streamlit page settings
st.set_page_config(
    page_title="GPT-4o mini Chat",
    page_icon="💬",
    layout="centered",
)

# initializing chat section in streamlit if not already present
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# streamlit page title
st.title("GPT-4o mini ChatBot")

# display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# input field for user to type message
user_prompt = st.chat_input("Ask me anything...")

if user_prompt:
    # add user's message to chat and display 
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # send user's message to GPT-4o mini and get a response
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            *st.session_state.chat_history
        ]
    )

    assistant_response = response.choices[0].message["content"]
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # display GPT-4o mini's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
        
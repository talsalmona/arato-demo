from st_on_hover_tabs import on_hover_tabs
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
st.set_page_config(layout="wide")


load_dotenv()

def generate_response(txt, system_prompt, openai_api_key, arato_api_key, arato_url):
    client = OpenAI(
        api_key=arato_api_key,
        base_url=arato_url
    )
        
    completion = client.chat.completions.create(
        extra_headers={"OPENAI_API_KEY": openai_api_key},
        model="gpt-4o-mini",
        messages=[{"role":"system", "content": system_prompt}, {"role":"user","content": txt}]
    )
    message = completion.choices[0].message.content
    return message

def input_form(prompt):
    
    result = []
    with st.form('form', clear_on_submit=True):
        if ('OPENAI_API_KEY' in os.environ):
            openai_api_key = os.environ['OPENAI_API_KEY']
        else:
            openai_api_key = st.text_input('OpenAI API Key', type = 'password')

        arato_api_key = st.text_input('Arato API Key', type = 'password', value='6S6NWo92ZD7H5etgLaIHWG2NqXGozCkjCKafSoR6zqhJ2P63UT9YjTpHJOQC')        
        arato_url = st.text_input('Arato URL', value='https://demo-api.arato.io/exquisite-pink-orinoco-7702/v1/chat/completions')

        txt_input = st.text_area('Enter the text to summarize', '', height=200)
        # is_submit_disabled = not(len(txt_input) > 0 and openai_api_key.startswith('sk-') and len(arato_api_key) > 0 and arato_url.startswith('https://'))

        submitted = st.form_submit_button('Submit') #, disabled=is_submit_disabled)
        if submitted and openai_api_key.startswith('sk-'):
            with st.spinner('Thinking...'):
                response = generate_response(txt_input, prompt, openai_api_key, arato_api_key, arato_url)
                result.append(response)

        if len(result):
            st.info(response)
            st.balloons()


        # Given a URL like this: https://demo-api.arato.io/radiant-burgundy-rila-1756/v1/chat/completions
        # Remove the '-api' from the subdomain, remove the '/v1/chat/completions' from the end, and append '/flow/radiant-burgundy-rila-1756/events' where 'radiant-burgundy-rila-1756' is the project ID
        flow_id = arato_url.split('/')[-4]
        base_url = arato_url.split('/')[2].replace('-api', '')
        results_url = 'https://' + base_url + '/flow/' + flow_id + '/events'
        st.write(f'View live results in [Arato]({results_url})')

def chat_response(system_prompt):
        if ('OPENAI_API_KEY' in os.environ):
            openai_api_key = os.environ['OPENAI_API_KEY']
        else:
            openai_api_key = st.text_input('OpenAI API Key', type = 'password')

        arato_api_key = st.text_input('Arato API Key', type = 'password', value='6S6NWo92ZD7H5etgLaIHWG2NqXGozCkjCKafSoR6zqhJ2P63UT9YjTpHJOQC')        
        arato_url = st.text_input('Arato URL', value='https://demo-api.arato.io/exquisite-pink-orinoco-7702/v1/chat/completions')

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])   


        if txt_input := st.chat_input("Say something"):
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(txt_input)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": txt_input})
            with st.spinner('Thinking...'):
                response = generate_response(txt_input, system_prompt, openai_api_key, arato_api_key, arato_url)
                with st.chat_message("assistant"):
                    st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

        

        # Given a URL like this: https://demo-api.arato.io/radiant-burgundy-rila-1756/v1/chat/completions
        # Remove the '-api' from the subdomain, remove the '/v1/chat/completions' from the end, and append '/flow/radiant-burgundy-rila-1756/events' where 'radiant-burgundy-rila-1756' is the project ID
        flow_id = arato_url.split('/')[-4]
        base_url = arato_url.split('/')[2].replace('-api', '')
        results_url = 'https://' + base_url + '/flow/' + flow_id + '/events'
        st.write(f'View live results in [Arato]({results_url})')



with st.sidebar:
    tabs = on_hover_tabs(tabName=['Summarization', 'Classification', 'Chat'], 
                         iconName=['money', 'dashboard', 'economy'], default_choice=0)


if tabs =='Summarization':
    st.title(f'{tabs}')
    input_form("Summarize the following text into 2 sentences:")

elif tabs == 'Classification':
    st.title(f'{tabs}')
    input_form("Classify the following text into one of two categories [engligh, french]:")

elif tabs == 'Chat':
    st.title(f'{tabs}')
    chat_response("You are a helpful chat bot")

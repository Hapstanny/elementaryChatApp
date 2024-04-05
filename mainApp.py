from openai import OpenAI, AzureOpenAI
import streamlit as st
from dotenv import load_dotenv
import os
import requests
import config as cfg
from st_audiorec import st_audiorec
from whisper import whipser_transcribe_audio
from io import BytesIO

load_dotenv()

st.title("Elementary Chat App")
query=""


def createPrompt():
    st.session_state.systemprompt=cfg.prompt

def load_setting(setting_name, session_name,default_value):  
    """  
    Function to load the setting information from session  
    """  
    if session_name not in st.session_state:  
        if os.environ.get(setting_name) is not None:
            st.session_state[session_name] = os.environ.get(setting_name)
        else:
            st.session_state[session_name] = default_value  

def getDeployments():
    headers={"Content-Type":"application/json","api-key":st.session_state.aoaikey}
    uri = f"https://{st.session_state.aoairegion}.api.cognitive.microsoft.com/openai/deployments?api-version=2022-12-01"
    # print(uri)    
    request = requests.get(uri, headers=headers)
    response = request.json()
    st.session_state['deployments'] = []
    for i,dep in enumerate(response['data']):
        st.session_state['deployments'].append(dep['id'])
        if i==0:
            st.session_state['deployment'] = dep['id']


def getSideBar():
    
    getDeployments()

    with st.sidebar:
        with st.form("AzureOpenAI"):
            if len(st.session_state['deployments'])>0:
                st.session_state.deployment=st.selectbox('Azure OpenAI Deployment', st.session_state['deployments'],index=3,label_visibility='hidden')
            st.session_state.tokens=st.text_input("Tokens",key="txtTokens",value=st.session_state.tokens)
            st.session_state.temperature=st.slider("Temperature",min_value=0.0,max_value=1.0,value=float(st.session_state.temperature),step=.1)
            st.session_state.aoaiversion=st.text_input("API Version",key="txtVersion",value=st.session_state.aoaiversion)
            st.form_submit_button()

            
    with st.sidebar:
        with st.form("Recording"):
            st.markdown("Ask your questions")
            wav_audio_data = st_audiorec()
            if wav_audio_data is not None:
                write_byte = BytesIO(wav_audio_data)  # Bytes representing another characte
                with open("test.wav", "wb") as f:
                     f.write(write_byte.getbuffer())
                st.session_state["audio_transcription"]=whipser_transcribe_audio("test.wav")
                st.markdown(st.session_state.audio_transcription.text)
            st.session_state.submit=st.form_submit_button("Submit")   
                
        
    # with st.sidebar:
    #     with st.form("Recording"):
    #          st.markdown("Ask your questions")
    #          st.session_state.transcription = []
    #          record = st.form_submit_button("Start Recording")  
    #          if record:
    #              st.session_state.transcription=recognize_from_microphone()
    #          for val in st.session_state.transcription:
    #              st.write(val)
        

# Load Configuration
load_setting('AZURE_OPENAI_API_VERSION','aoaiversion','2023-05-15')
load_setting('REGION','aoairegion','azure')
load_setting('OPENAI_API_KEY','aoaikey','eastus')
load_setting('OPENAI_ENDPOINT','aoaiendpoint','')
load_setting('TOKENS','tokens',500)
load_setting('TEMPERATURE','temperature',0.7)
load_setting('AZ_DEFAULT_DEPLOYMENT','aoaidep','gpt35turbo')

client = AzureOpenAI(api_key=st.session_state.aoaikey, 
                     azure_endpoint=st.session_state.aoaiendpoint, 
                     api_version=st.session_state.aoaiversion)

# Creating slide bar
getSideBar()
# Create Prompt
createPrompt()


if "deployment" not in st.session_state:
    st.session_state["deployment"] = st.session_state.aoaidep

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "system", "content": st.session_state.systemprompt})

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    
def processing(prompt):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        
        stream = client.chat.completions.create(
            model=st.session_state.deployment,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            temperature=float(st.session_state.temperature),
            max_tokens=int(st.session_state.tokens),
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

prompt = st.chat_input("Enter your question here")

#Processing Main

if st.session_state.submit and st.session_state.audio_transcription is not None:
    prompt=st.session_state.audio_transcription.text
    processing(prompt)
else:
    if prompt:
        processing(prompt)
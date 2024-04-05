import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import numpy as np
 

load_dotenv()

def whipser_transcribe_audio(wav_audio_data):

    client = AzureOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),  
        api_version="2024-02-01",
        azure_endpoint = os.getenv("OPENAI_ENDPOINT")
    )
    
    deployment_id = "whisper" 
    result = client.audio.transcriptions.create(
        file=open(wav_audio_data, "rb"),      
        model=deployment_id
    )

    return result
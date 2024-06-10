import sys
sys.path.append("../vectorstore/")
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

#Langchain
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()


#---------------INIT APP------------------
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#---------------INIT DATA------------------
chat = ChatOpenAI(temperature=0.5, openai_api_key=os.environ["OPENAI_API_KEY"])

#---------------TYPES------------------
class ChatMessage(BaseModel):
    message: str


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/chat", response_model=dict)
async def getMessage(message:ChatMessage):
    print("Otrzymałem wiadomość ", message.message)
    assert message.message is not None, "Message must be provided"

    answear = "Test"
    return {"message": answear}
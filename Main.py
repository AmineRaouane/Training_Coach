import streamlit as st
from vertexai.preview.generative_models import GenerativeModel, Part, ChatSession, Content
from vertexai import generative_models
import vertexai
import os
import requests
from Prompts.Prompts import load_prompt_from_yaml ,wikipedia_search


FLASK_URL = "http://localhost:5000"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "GOOGLE_APPLICATION_CREDENTIALS.json"
vertexai.init(project="gemini3-428013", location="us-central1")
st.set_page_config(
    page_title="My Streamlit App",
    page_icon=":rocket:",
    layout="wide"
)

initial_prompt_config = load_prompt_from_yaml('./Prompts/initial_prompt.yaml')
initial_prompt = initial_prompt_config['initial_prompt'] # type: ignore

keyword_config = load_prompt_from_yaml('./Prompts/Keywords.yaml')
keyword_prompt = keyword_config['keyword_extraction'] # type: ignore



model = GenerativeModel(
        "gemini-1.5-pro",
        generation_config=generative_models.GenerationConfig(
            temperature=0.4
            )
        )

Chat = model.start_chat()
initial_response = Chat.send_message(initial_prompt) 
initial_output = initial_response.candidates[0].content.parts[0].text # type: ignore
Chat.history.append(
    Content(
        role="user",
        parts=[Part.from_text(initial_prompt)])
            )
Chat.history.append(
    Content(
        role="assistant",
        parts=[Part.from_text(initial_output)])
            )



def get_chat_history():
    response = requests.get(f"{FLASK_URL}/get_chats")
    if response.status_code == 200:
        return response.json()
    return []

def store_chat(user_message, model_response):
    data = {
        'user_message': user_message,
        'model_response': model_response
    }
    response = requests.post(f"{FLASK_URL}/append_interaction/{st.session_state.id}", json=data)
    if response.status_code != 200:
        st.error("Failed to store chat")
    else:
        st.session_state.messages.append(data)


st.html("<div class='title'>GEMINI Explorer</div>")
st.html("styles/styles.html")

chat_history = get_chat_history()

if "id" not in st.session_state:
    st.session_state.id = None

if "messages" not in st.session_state:
    st.session_state.messages = []


def handle_chat_selection(ID, messages):
    if isinstance(messages, str):
        messages = eval(messages)
    st.session_state.messages = messages
    st.session_state.id = ID



def create_new_chat():
    st.session_state.messages = []
    st.session_state.id = None


def instantiate_chat(title,interaction):
    data = {
        "title" :title,
        "messages" : [interaction]
        }
    response = requests.post(f"{FLASK_URL}/add_chat",json=data)
    if response.status_code == 201:
        Container.html(f'''<div class='user_input'>
                       <b>{interaction['user_message']}</b>
                       </div>''')
        Container.markdown(interaction["model_response"])
        return response.json()['id']
    return None

def send_message(message):
    keywords = Chat.send_message(f"{keyword_prompt}{message}")
    keywords = keywords.candidates[0].content.parts[0].text # type: ignore
    keywords = keywords.split(",") # type: ignore
    wiki_research = wikipedia_search(keywords)
    response = Chat.send_message(f"{message}\n Additional information : \n {wiki_research=}") 
    output = response.candidates[0].content.parts[0].text # type: ignore

    if st.session_state.id:
        store_chat(message, output)
        Container.html(f'''<div class='user_input'>
                       <b>{message}</b>
                       </div>''')
        Container.markdown(output)
        # with st.expander("See the reasearch"):
        #     st.markdown(wiki_research)
            
    else :
        title_response = Chat.send_message(f"give me a a small consice title based on this question {message} , give me just the title witout anything else")
        title = title_response.candidates[0].content.parts[0].text  # type: ignore
        first_interaction = {
            'user_message': message,
            'model_response': output
        }
        st.session_state.id = instantiate_chat(title,first_interaction)
        st.session_state.messages = [first_interaction]
        st.experimental_rerun()

def SideBar():
    with st.sidebar: # type: ignore
         st.button("new_chat",use_container_width=True,on_click=create_new_chat)
         st.html("<div class='title'>Previous messages<div>")
         with st.container(border=True,height=500) :
              for chat in chat_history :
                   st.button(chat["title"][:20]+"...",help=chat["title"],use_container_width=True,on_click=handle_chat_selection, args=(chat["id"], chat["messages"]))
SideBar()
                
Container = st.container(border=False,height=450)
for message in st.session_state.messages :
    if message["user_message"]:
        content1 = Content(
            role="user",
            parts=[Part.from_text(message["user_message"])])
        Chat.history.append(content1)

        Container.html(f'''<div class='user_input'>
                       <b>{message['user_message']}</b>
                       </div>''')
    if message["model_response"]:
        content2 = Content(
            role="assistant",
            parts=[Part.from_text(message["model_response"])])
        Chat.history.append(content2)

        Container.markdown(message["model_response"])



query = st.chat_input("Ask me anything", key="query")
if query:
    send_message(query)

import codecs
import os
import streamlit as st
from chromadb_utils import DB_service
from pathlib import Path

os.environ["OPENAI_API_KEY"] = st.secrets['apikey']

db_service = DB_service()
data_directory = "data"
# prepare file system
db_service.setup_folders()

st.title("Store files into a vector database, then search database using Natural language.")
st.subheader("Store files into Chroma DB. Search DB with OpenAI GPT-3-Turbo.")

with st.sidebar:
    st.title('About')
    st.markdown('''
        The goal is store your files into the vector database, Chroma DB.
        - OpenAI's GPT API queries Chroma Database
        - LangChain connects and searches Chroma DB using OpenAI' GPT-3
        This is a Proof Of Concept (POC) and is not production ready. 

     ''')
    st.title('Technology')
    st.markdown('''
        Developed by Jorge Duenas using:
        - [OpenAI GPT-3.5 API](https://openai.com/product)
        - [Streamlit.io](https://streamlit.io/)
        - [LangChain](https://python.langchain.com/en/latest/index.html)
        - [Python](https://www.python.org/)
        - [Anaconda](https://www.anaconda.com/)   
        - [Pycharm IDE](https://www.jetbrains.com/pycharm/) 
        - [Chroma Vector DB](https://docs.trychroma.com/)    

    ''')


uploaded_files = st.file_uploader("Please select file(s) to upload", [".txt"], accept_multiple_files=True)
if uploaded_files:
    print(f"jddebug77 ******************* number of files uploaded = {len(uploaded_files)}")
    for uploaded_file in uploaded_files:
        print(f"file_path = {uploaded_file}")
        with open(os.path.join(data_directory, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())

        db_service.load_text_files_to_db()

    user_input = st.text_input("what do you want to search")
    if user_input:
        print(f"jddebug ******************* user_input = :::{user_input}:::")
        returned_answer, source_used = db_service.retrieve_data(user_input)
        print(f"docs = {returned_answer}  and source document = {source_used}")
        st.write(returned_answer)
        if source_used:
            # st.write(source_used)
            print(f"in main source_used = {source_used}")
            try:
                with st.expander(f'Source: {source_used}'):
                    st.write(Path(source_used).read_text().encode(encoding="utf-8", errors='ignore'))
            except UnicodeDecodeError:
                print("jddebug ran into UnicodeDecodeError")

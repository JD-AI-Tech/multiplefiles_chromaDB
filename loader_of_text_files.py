from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_text_files_to_db():
     #print(f"data_directory = {data_directory}")
    print(f"load_text_files about to call DirectoryLoader()")
    loader = DirectoryLoader('./data/', glob = "./*.txt", loader_cls=TextLoader, show_progress=True)
    print(f"load_text_files about to call loader.load()")
    documents = loader.load()
    print(f"load_text_files loaded documents!!!!!!!!!!!!!!!!!!!!!!!!!")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    text_files = text_splitter.split_documents(documents)
    print(f"lenght of documents = {len(text_files)}")
    #create_chromadb(text_files, 'db')


load_text_files_to_db()
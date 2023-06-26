from langchain.chains import RetrievalQA
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from  langchain.llms import OpenAI

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

from file_utility import create_directory, delete_folder

class DB_service:

    vectordb = []

    def load_text_files_to_db(self):
        #loader = DirectoryLoader('./data/', glob = "./*.txt", loader_cls=TextLoader, show_progress=True)
        loader = DirectoryLoader('./data/', glob = "./*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()
        print(f"load_text_files loaded documents!!!!!!!!!!!!!!!!!!!!!!!!!")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        text_files = text_splitter.split_documents(documents)
        print(f"lenght of documents = {len(text_files)}")
        DB_service.create_chromadb(text_files, 'db')


    def create_chromadb (text_files, db_path):
        print("jddebug ***** in create_chromadb")
        embedding = OpenAIEmbeddings()
        loc_vectordb = Chroma.from_documents(documents=text_files,
                                             embedding=embedding,
                                             persist_directory=db_path)

        print("jddebug ***** in create_chromadb after creating loc_vectordb")
        # persist to file system
        loc_vectordb.persist()
        print("jddebug ***** in create_chromadb presisted loc_vectordb")
        loc_vectordb = None

    def process_llm_response(self, llm_response):
        print(llm_response['result'])
        print('\n\nSources:')
        #sources_used = '\n\nSources:'
        sources_used = ''
        for source in llm_response["source_documents"]:
            #print(source.metadata['source'])
            #sources_used = '\n' + source.metadata['source']
            sources_used = source.metadata['source']
            print(f"sources_used = {sources_used}")
        return sources_used

    def retrieve_data(self, query):
        print(f"retrieve_data() query = {query}")
        db_directory = "db"
        embedding = OpenAIEmbeddings()
        print(f"retrieve_data() after OpenAIEmbeddings() ")

        vectordb = Chroma(persist_directory=db_directory, embedding_function=embedding)

        print(f"retrieve_data() after creating vectordb ")
        retriever = vectordb.as_retriever(search_kwargs={"k": 3})
        print(f"retrieve_data() after as_retriever() ")

        # create the chain to answer questions
        qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(),
                                               chain_type="stuff",
                                               retriever=retriever,
                                               return_source_documents=True)

        lms_response = qa_chain(query)
        sources_used = self.process_llm_response(lms_response)
        answer = lms_response["result"]
        print(f"jddebug  lms_response = {lms_response}")
        print(f"jddebug ###### answer = {answer}")
        print(f"jddebug  #####  sources_used = {sources_used}")

        # return answer.join(sources_used)
        #return answer + "\n\nSource:  " + sources_used
        return answer, sources_used

    def setup_folders(self):
        data_directory = "data"
        create_directory(data_directory, True)
        db_directory = "db"
        delete_folder(db_directory)
        create_directory(db_directory, True)
        log_directory = "log"
        create_directory(log_directory, True)
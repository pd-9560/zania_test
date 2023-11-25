from django.db import connection
from langchain.document_loaders import PyPDFLoader, JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from vectordb import Memory

from integration.rag_services.constants import FileTypes


class KnowledgeBase:
    #  a class to store any given document in the knowledge store(vectordb2)
    #  the class is also used by answering service to retrive relevant context it requires
    FILE_TYPE_TO_LOADER_MAP = {
        FileTypes.JSON: JSONLoader,
        FileTypes.PDF: PyPDFLoader,
    }
    
    def __init__(self, *args, **kwargs):
        self.memory = connection.__getattr__('memory', None)
        if not self.memory:
            #  we persist the memory object in connection object
            self.memory = Memory()
            connection.__setattr__('memory', self.memory)

    def add_document(self, path, type, *args, **kwargs):
        """
        function to add a document in the knowledgebase 
        Note:
            if file type is JSON the function requires jq_schema as kwarg
        Args:
            path: path to the file
            type: type of the file options -> FileTypes
        """
        if type not in self.FILE_TYPE_TO_LOADER_MAP:
            return
        # load and split
        if type == FileTypes.JSON:
            if 'jq_schema' not in kwargs:
                return
            loader = JSONLoader(path, kwargs.get('jq_schema'))
        else:
            loader = self.FILE_TYPE_TO_LOADER_MAP.get(type)(path)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = loader.load_and_split(text_splitter)

        # store
        text = [split.page_content for split in splits]
        metadata = [split.metadata for split in splits]
        self.memory.save(text, metadata=metadata)
        
    def clean_slate(self):
        """
        function to delete all knowledge in the knowledge base.
        """
        self.memory.clear()

    def retrive(self, question, top_n):
        """
        function to retrieve relevant documents from base
        Args:
            question: a string which represents the question being sent to LLM model
            top_n: number of relevant chunks to be fetched and passed as context to LLM model
        Returns:
            a list of Document objects
        """
        return [Document(page_content=chunk['chunk'], metadata=chunk['metadata'])
                 for chunk in self.memory.search(query=question, top_n=top_n)]
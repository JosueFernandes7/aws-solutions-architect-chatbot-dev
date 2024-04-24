from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import CacheBackedEmbeddings, HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.storage import LocalFileStore


def extract_text_from_pdf():
  loader = PyPDFLoader("data/aws-overview.pdf")
  pages = loader.load_and_split()
  return pages

def ignore_table_of_contents_pages(pages, table_of_contents_final_page = 10):
    for index, page in enumerate(pages):
        if page.metadata.get('page') == table_of_contents_final_page + 1:
            break
    return pages[index:]

def split_into_chunks(pages):
  text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 3000, 
    chunk_overlap = 200, 
    length_function = len)

  return text_splitter.transform_documents(pages)

def init_embeddings_model(embed_model_id = 'sentence-transformers/all-MiniLM-L6-v2'):

 return HuggingFaceEmbeddings(model_name=embed_model_id), embed_model_id

def create_vector_store(core_embeddings_model, documents, embed_model_id):

  embedder = HuggingFaceEmbeddings(model_name='sentence-transformers/distiluse-base-multilingual-cased-v1')

  vector_store = FAISS.from_documents(documents, embedder)

  return vector_store

def save_vector_store(vector_store):
    vector_store.save_local('aws-overview-index')
  
def load_vector_store():
    return FAISS.load_local('aws-overview-index', HuggingFaceEmbeddings(model_name='sentence-transformers/distiluse-base-multilingual-cased-v1'), allow_dangerous_deserialization=True)
  
def main():
    pages = extract_text_from_pdf()
    pages = ignore_table_of_contents_pages(pages)
    documents = split_into_chunks(pages)
    
    core_embeddings_model, embed_model_id = init_embeddings_model('sentence-transformers/distiluse-base-multilingual-cased-v1')
    vector_store = create_vector_store(core_embeddings_model, documents, embed_model_id)
    
    save_vector_store(vector_store)

if __name__ == '__main__':
    main()
    
try:
  db = load_vector_store()
except Exception as e:
  print(e)
  main()
  load_vector_store()
from groq import Groq
from settings import settings
import requests
from vector_store import db

client = Groq(api_key = settings.GROQ_API_KEY)

def get_groq_response(prompt, model_id = "mixtral-8x7b-32768"):
  response = client.chat.completions.create(
      model=model_id,
      messages=[
          {
              "role": "system",
              "content": "You are a helpful assistant."
          },
          {
              "role": "user",
              "content": prompt
          }
      ],
      max_tokens=4096
  )

  return(response.choices[0].message.content)

def build_prompt(query, context):
  return f"""
    Você é um arquiteto de soluções AWS altamente qualificado, especializado em orientar clientes na escolha e implementação dos serviços da AWS para atender às suas necessidades específicas. Seu objetivo é fornecer respostas claras e precisas às dúvidas dos clientes, 
    garantindo que eles entendam como os diferentes serviços podem ser usados para resolver seus problemas de infraestrutura e aplicativos. 
    Responda, em português, com base no contexto:
    {context}
    Responda apenas se encontrar resposta no contexto. Se não encontrar, diga que não encontrou a resposta. Lembre-se de responder em português.
    Pergunta: {query}
  """
#  A resposta deve seguir o padrão:
#     Pergunta ###PERGUNTA AQUI
#     R: ###RESPOSTA AQUI
def get_query_embeddings(query):
  model_id ='sentence-transformers/distiluse-base-multilingual-cased-v1'
  
  api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
  headers = {"Authorization": f"Bearer {settings.HF_TOKEN}"}
  
  response = requests.post(api_url, headers=headers, json={"inputs": query, "options":{"wait_for_model":True}})
  return response.json()

def query_expansion(query):
  prompt = f"""Esse é minha pergunta: {query}
  Me retorne uma Lista com 5 jeitos de escrever essa mesma pergunta em portugues.
  Retorne apenas a lista sem nenhuma frase introdutória, nem nada, apenas a lista
  """
  
  return get_groq_response(prompt, 'gemma-7b-it')

def get_context(query):
  embedding_vector = get_query_embeddings(query)
  docs = db.similarity_search_by_vector(embedding_vector, k = 5)
  context = ''
  for page in docs:
    context += page.page_content

  return context

def get_answer(query, model_id = 'mixtral-8x7b-32768'):
  expanded_query = query_expansion(query)
  print(expanded_query)
  context = get_context(query)
  print(context)
  
  prompt = build_prompt(context, query)
  return get_groq_response(prompt, model_id)



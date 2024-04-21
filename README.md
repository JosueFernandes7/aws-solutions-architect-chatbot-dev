**aws-solutions-bot**

Este repositório contém uma solução básica de chatbot desenvolvida com o auxílio de um modelo de linguagem natural (LLM - Mixtral-8x7b-32768) para simular as interações com um arquiteto de soluções AWS. A solução é projetada para fornecer respostas claras e precisas às dúvidas dos usuários sobre os serviços da AWS.

**Instruções de Uso:**

1. Clone este repositório:
2. Instale as dependências listadas no arquivo requirements.txt:
'''bash
pip install -r requirements.txt
'''
3. Adicione suas credenciais da AWS conforme o modelo no arquivo .env.example e renomeie-o para .env.

4. Execute o script vector_store.py para crar o banco de dados vetorial
'''bash
python vector_store.py
'''
5. Execute o script main.py para iniciar o chatbot:



Este projeto é uma abordagem simples para explorar e interagir com os serviços da AWS por meio de um chatbot, proporcionando uma experiência de aprendizado de forma acessível e direta.

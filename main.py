from genai import get_answer
query = input('Digite sua dúvida:')
while query != "exit":
    print ("Generating")
    response = get_answer(query)
    print(response)
    query = input('Digite sua nova dúvida:')
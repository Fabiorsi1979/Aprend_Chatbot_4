from django.shortcuts import render
from django.http import JsonResponse
import requests
from langchain import LangChain

# Inicializar o LangChain
langchain = LangChain()

def chat_view(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        
        # Processar a mensagem do usuário com LangChain
        processed_message = langchain.process(user_message)
        
        # Fazer uma solicitação à API do DeepSeek
        response = requests.post(
            'https://api.deepseek.com/v1/query',
            headers={'Authorization': f'Bearer {settings.DEEPSEEK_API_KEY}'},
            json={'query': processed_message}
        )
        
        # Obter a resposta da API
        deepseek_response = response.json()
        
        return JsonResponse({'response': deepseek_response})
    
    return render(request, 'chat_app/chat.html')

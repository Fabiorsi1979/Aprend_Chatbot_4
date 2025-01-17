from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.conf import settings
import requests

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        
        if not user_message:
            return JsonResponse({'error': 'Mensagem não pode estar vazia'}, status=400)
        
        try:
            headers = {
                'Authorization': f'Bearer {settings.DEEPSEEK_API_KEY}',
                'Content-Type': 'application/json'
            }
            
            data = {
                "model": "deepseek-chat",
                "messages": [{
                    "role": "user",
                    "content": user_message
                }]
            }
            
            response = requests.post(
                DEEPSEEK_API_URL,
                headers=headers,
                json=data
            )
            response.raise_for_status()
            
            return JsonResponse({
                'response': response.json()['choices'][0]['message']['content'],
                'status': 'success'
            })
            
        except requests.exceptions.RequestException as e:
            return JsonResponse({
                'error': str(e),
                'status': 'error'
            }, status=500)
    
    return render(request, 'chat_app/chat.html')

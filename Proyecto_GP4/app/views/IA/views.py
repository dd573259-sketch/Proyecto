import os
from app.models import *
from openai import OpenAI
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")




@csrf_exempt
def chat(request):
    if request.method == 'POST':
    
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un asistente experto en mi sistema web. Responde preguntas sobre el proyecto de forma clara."
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                stream=False
            )

            reply = response.choices[0].message.content

            return JsonResponse({"response": reply})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)
    
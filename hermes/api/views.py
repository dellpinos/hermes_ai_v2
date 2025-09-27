import json
import re
from django.contrib.auth.decorators import login_required
from .decorators import api_key_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from llm.model_files.main import invoke_alma, enqueue_task, generate_summary
from llm.model_files.config import chat_config, tlw_config


# Create your views here.

@login_required
def chat_api(request):

    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed."}, status=405)
        
    user_msg = request.POST.get("message")
    chat_token = request.POST.get("token")
        
    # Validar que los datos existen
    if not user_msg or not chat_token:
        return JsonResponse({"error": "Missing required data."}, status=400)

    # Validar el formato del token del chat (de 32 caracteres alfanuméricos)
    if not re.match(r'^[0-9a-fA-F]{32}$', chat_token):
        return JsonResponse({"error": "Invalid token format."}, status=400)
    
    MAX_MESSAGE_LENGTH = 600
    
    # Validar la longitud del mensaje
    if len(user_msg) > MAX_MESSAGE_LENGTH:
        return JsonResponse({
            "error": f"The message exceeds the maximum allowed length: {MAX_MESSAGE_LENGTH}."
        }, status=400)
        
    # User data
    user = request.user
    user_id = user.id

    # Calls the model using the Queue
    ai_response = enqueue_task(invoke_alma, user_msg, chat_token, chat_config, user_id, wait=True)

    # Response
    response = JsonResponse(
        {
            "status": "success",
            "response" : ai_response["final_response"]
        }, status=200
    )

    # Calls the model using the Queue
    enqueue_task(generate_summary, ai_response, wait=False)

    return response

        
        
@csrf_exempt
@api_key_required
def default_api(request):
    pass

@csrf_exempt
@api_key_required
def tlw_api(request):
    
    # Validation
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed."}, status=405)
        
    try:
        data = json.loads(request.body)
        user_msg = data.get('message')
        chat_token = data.get('token')
        
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "Invalid data format."}, status=400)
        
    # Validates if the data exists
    if not user_msg or not chat_token:
        return JsonResponse({"error": "Missing required data."}, status=400)

    # Validates the token's format
    if not re.match(r'^[0-9a-fA-F]{32}$', chat_token):
        return JsonResponse({"error": "Invalid token format."}, status=400)
    
    # Validates msg length
    MAX_MESSAGE_LENGTH = 600
    
    if len(user_msg) > MAX_MESSAGE_LENGTH:
        return JsonResponse({
            "error": f"The message exceeds the maximum allowed length: {MAX_MESSAGE_LENGTH}."
        }, status=400)
        
    # Calls the model using the Queue
    ai_response = enqueue_task(invoke_alma, user_msg, chat_token, tlw_config, user_id=None, wait=True)

    # Response
    response = JsonResponse(
        {
            "status": "success",
            "response" : ai_response["final_response"]
        }, status=200
    )

    # Calls the model using the Queue
    enqueue_task(generate_summary, ai_response, wait=False)

    return response
    

@csrf_exempt
@api_key_required
def porfolio_api(request):
    pass

@csrf_exempt
@api_key_required
def dellpinos_api(request):
    pass

@csrf_exempt
@api_key_required
def stuff_api(request):
    pass



